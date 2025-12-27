import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

# *** ספרייה חדשה ***
from google import genai
from google.genai import types

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deepfake_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- API Key Configuration ---
# אופציה 1: שימוש ב-.env file (מומלץ)
try:
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
except:
    GOOGLE_API_KEY = None


if not GOOGLE_API_KEY :
    raise ValueError("❌ חסר GOOGLE_API_KEY - הדביקי את המפתח בשורה 30")

# Initialize Gemini Client
client = genai.Client(api_key=GOOGLE_API_KEY)

# --- Configuration ---
MODEL_NAME = 'gemini-3-flash-preview'  
MAX_RETRIES = 3
TIMEOUT_SECONDS = 300

@dataclass
class AnalysisResult:
    video_name: str
    is_deepfake: str
    fakeness_score: int
    artifacts: List[str]
    reasoning: str
    analysis_time: float
    timestamp: str
    error: Optional[str] = None

# --- Detection Prompt ---
DETECTION_PROMPT = """
You are an expert digital forensics AI agent specializing in detecting deepfakes.
Analyze the video for BOTH visual and audio anomalies.

**Critical Analysis Points:**
1. **Facial Micro-Expressions**: Unnatural smoothness, rigidity, or AI-generated movement patterns
2. **Blinking Patterns**: Irregular frequency, unnatural timing, or absence
3. **Lip-Sync Quality**: Audio-visual mismatch, mouth blurring, unnatural tongue/teeth
4. **Temporal Consistency**: Frame-to-frame flickering, morphing, or warping
5. **Lighting & Shadows**: Inconsistent lighting on face vs background, impossible shadow angles
6. **Hair & Edges**: Blurring at hair boundaries, inconsistent edge definition
7. **Background Artifacts**: Unnatural background behavior when person moves
8. **Audio Anomalies**: Robotic voice quality, breathing inconsistencies
9. **Eye Movement**: Unnatural gaze patterns, lack of micro-saccades
10. **Skin Texture**: Over-smoothed skin, lack of pores, unnatural texture

**Scoring Guide:**
- 0-30: Likely authentic (minor compression artifacts acceptable)
- 31-60: Suspicious (multiple minor artifacts or 1-2 major ones)
- 61-85: High suspicion (clear AI generation indicators)
- 86-100: Almost certainly synthetic (multiple obvious artifacts)

**OUTPUT FORMAT (JSON ONLY):**
{
    "analysis_target": "filename",
    "is_deepfake_suspicion": "High/Medium/Low",
    "fakeness_score": 0-100,
    "key_artifacts_detected": ["specific artifact 1", "specific artifact 2"],
    "reasoning": "Technical explanation with details",
    "confidence_level": "High/Medium/Low"
}
"""

class DeepfakeDetector:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.client = client
        self.results: List[AnalysisResult] = []
        logger.info(f"🤖 Deepfake Detector initialized with model: {model_name}")

    def analyze_video(self, video_path: str) -> Optional[AnalysisResult]:
        """Main analysis function with retry logic"""
        video_path = Path(video_path)
        
        if not video_path.exists():
            logger.error(f"❌ File not found: {video_path}")
            return None
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🎬 Analyzing: {video_path.name}")
        logger.info(f"{'='*60}")
        
        start_time = time.time()
        
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"📤 Upload and analyze attempt {attempt}/{MAX_RETRIES}")
                
                # קריאת הוידאו
                with open(video_path, 'rb') as f:
                    video_data = f.read()
                
                # יצירת Part עם הוידאו
                video_part = types.Part.from_bytes(
                    data=video_data,
                    mime_type="video/mp4"
                )
                
                # שליחת הבקשה
                logger.info("🔍 Analyzing video with AI agent...")
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=[DETECTION_PROMPT, video_part],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.1
                    )
                )
                
                # Parse תשובה
                analysis_data = self._validate_json_response(response.text)
                
                # Create result
                analysis_time = time.time() - start_time
                result = AnalysisResult(
                    video_name=video_path.name,
                    is_deepfake=analysis_data["is_deepfake_suspicion"],
                    fakeness_score=analysis_data["fakeness_score"],
                    artifacts=analysis_data["key_artifacts_detected"],
                    reasoning=analysis_data["reasoning"],
                    analysis_time=analysis_time,
                    timestamp=datetime.now().isoformat()
                )
                
                self.results.append(result)
                self._display_result(result)
                
                return result
                
            except Exception as e:
                logger.error(f"❌ Attempt {attempt} failed: {str(e)}")
                if attempt == MAX_RETRIES:
                    logger.error(f"💀 All {MAX_RETRIES} attempts failed for {video_path.name}")
                    return AnalysisResult(
                        video_name=video_path.name,
                        is_deepfake="Unknown",
                        fakeness_score=-1,
                        artifacts=[],
                        reasoning="Analysis failed",
                        analysis_time=time.time() - start_time,
                        timestamp=datetime.now().isoformat(),
                        error=str(e)
                    )
                time.sleep(2 ** attempt)
        
        return None

    def _validate_json_response(self, response_text: str) -> Dict:
        """Validate and parse JSON response"""
        try:
            data = json.loads(response_text)
            
            required_fields = ["analysis_target", "is_deepfake_suspicion", 
                             "fakeness_score", "key_artifacts_detected", "reasoning"]
            
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            if not (0 <= data["fakeness_score"] <= 100):
                raise ValueError(f"Invalid fakeness_score: {data['fakeness_score']}")
            
            return data
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON response: {e}")
            logger.debug(f"Response text: {response_text}")
            raise

    def _display_result(self, result: AnalysisResult):
        """Pretty print analysis result"""
        print(f"\n{'='*60}")
        print(f"📊 ANALYSIS RESULTS: {result.video_name}")
        print(f"{'='*60}")
        print(f"🎯 Deepfake Suspicion: {result.is_deepfake}")
        print(f"📈 Fakeness Score: {result.fakeness_score}/100")
        print(f"⏱️  Analysis Time: {result.analysis_time:.2f}s")
        print(f"\n🔍 Artifacts Detected:")
        for artifact in result.artifacts:
            print(f"   • {artifact}")
        print(f"\n💭 Reasoning:\n   {result.reasoning}")
        print(f"{'='*60}\n")

    def save_report(self, output_file: str = "deepfake_report.json"):
        """Save analysis results to JSON file"""
        report = {
            "analysis_date": datetime.now().isoformat(),
            "model_used": self.model_name,
            "total_videos_analyzed": len(self.results),
            "results": [
                {
                    "video_name": r.video_name,
                    "is_deepfake": r.is_deepfake,
                    "fakeness_score": r.fakeness_score,
                    "artifacts": r.artifacts,
                    "reasoning": r.reasoning,
                    "analysis_time": r.analysis_time,
                    "timestamp": r.timestamp,
                    "error": r.error
                }
                for r in self.results
            ]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, indent=4, ensure_ascii=False, fp=f)
        
        logger.info(f"📄 Report saved to: {output_file}")

# --- Main Execution ---
if __name__ == "__main__":
    print("🤖 Deepfake Detection Bot")
    print("=" * 60)
    
    # Initialize detector
    detector = DeepfakeDetector()
    
    # רשימת הסרטונים לניתוח - שני כאן את שמות הקבצים שלך!
    videos = [
        "f5.mp4"
    ]
    
    # Analyze all videos
    for video in videos:
        detector.analyze_video(video)
    
    # Save comprehensive report
    detector.save_report("deepfake_analysis_report.json")
    
    logger.info("\n✅ All analyses complete!")
    print("\n🎉 Done! Check deepfake_analysis_report.json for full results")