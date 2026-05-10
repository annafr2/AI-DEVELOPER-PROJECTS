"""Yahoo Finance data client with gatekeeper and 3-tier fallback (cache → live → CSV)."""
import os
import time
import threading
import logging
from datetime import datetime

import pandas as pd
import yfinance as yf

import config

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

REQUIRED_COLS = ["Open", "High", "Low", "Close", "Volume"]


class ApiGatekeeper:
    """Token-bucket rate limiter: enforces per-minute, per-hour, and burst limits."""

    def __init__(self):
        self._lock           = threading.Lock()
        self._minute_calls   = []
        self._hour_calls     = []
        self._burst_calls    = []
        self._semaphore      = threading.Semaphore(config.MAX_CONCURRENT)

    def _prune(self, call_list, window_sec):
        cutoff = time.time() - window_sec
        while call_list and call_list[0] < cutoff:
            call_list.pop(0)

    def acquire(self):
        """Block until a request slot is available, then mark it used."""
        self._semaphore.acquire()
        with self._lock:
            now = time.time()
            self._prune(self._minute_calls, 60)
            self._prune(self._hour_calls,   3600)
            self._prune(self._burst_calls,  config.BURST_WINDOW_SEC)

            if len(self._burst_calls) >= config.BURST_LIMIT:
                sleep = config.BURST_WINDOW_SEC - (now - self._burst_calls[0])
                log.info("Burst limit — sleeping %.1fs", sleep)
                time.sleep(max(sleep, 0))

            if len(self._minute_calls) >= config.RATE_LIMIT_PER_MIN:
                sleep = 60 - (now - self._minute_calls[0])
                log.info("Minute limit — sleeping %.1fs", sleep)
                time.sleep(max(sleep, 0))

            if len(self._hour_calls) >= config.RATE_LIMIT_PER_HOUR:
                sleep = 3600 - (now - self._hour_calls[0])
                log.info("Hour limit — sleeping %.1fs", sleep)
                time.sleep(max(sleep, 0))

            ts = time.time()
            self._minute_calls.append(ts)
            self._hour_calls.append(ts)
            self._burst_calls.append(ts)

    def release(self):
        self._semaphore.release()


class YFinanceDataClient:
    """Fetch OHLCV data with Parquet cache → live yfinance → CSV fallback."""

    _gatekeeper = ApiGatekeeper()   # shared across all instances

    def _cache_path(self, ticker, start, end):
        fname = f"{ticker}_{start}_{end}.parquet"
        return os.path.join(config.DATA_DIR, fname)

    def _csv_path(self, ticker):
        return os.path.join(config.DATA_DIR, f"{ticker}.csv")

    def _validate(self, df, ticker):
        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        if missing:
            raise ValueError(f"{ticker}: missing columns {missing}")
        df = df[REQUIRED_COLS].dropna()
        if len(df) < config.WINDOW_SIZE + 1:
            raise ValueError(f"{ticker}: only {len(df)} rows — need >{config.WINDOW_SIZE}")
        return df

    def fetch(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """Return validated OHLCV DataFrame. Raises on all-tier failure."""
        cache = self._cache_path(ticker, start, end)

        # Tier 1 — Parquet cache
        if os.path.exists(cache):
            log.info("Cache hit: %s", cache)
            return pd.read_parquet(cache)

        # Tier 2 — live yfinance
        for attempt in range(1, config.MAX_RETRIES + 1):
            try:
                self._gatekeeper.acquire()
                log.info("Fetching %s %s→%s (attempt %d)", ticker, start, end, attempt)
                raw = yf.download(ticker, start=start, end=end,
                                  interval="1d", progress=False, auto_adjust=True)
                self._gatekeeper.release()
                if raw.empty:
                    raise ValueError("Empty response from yfinance")
                # flatten multi-level columns if present
                if isinstance(raw.columns, pd.MultiIndex):
                    raw.columns = raw.columns.get_level_values(0)
                df = self._validate(raw, ticker)
                df.to_parquet(cache, compression="snappy")
                log.info("Saved cache: %s (%d rows)", cache, len(df))
                return df
            except Exception as exc:
                self._gatekeeper.release()
                log.warning("Attempt %d failed: %s", attempt, exc)
                if attempt < config.MAX_RETRIES:
                    time.sleep(config.RETRY_DELAY_SEC)

        # Tier 3 — CSV fallback
        csv = self._csv_path(ticker)
        if os.path.exists(csv):
            log.info("CSV fallback: %s", csv)
            df = pd.read_csv(csv, index_col="Date", parse_dates=True)
            df = df[(df.index >= start) & (df.index <= end)]
            return self._validate(df, ticker)

        raise RuntimeError(f"All data tiers failed for {ticker} [{start} → {end}]")
