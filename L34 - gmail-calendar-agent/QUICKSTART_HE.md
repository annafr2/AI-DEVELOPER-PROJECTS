# מדריך התחלה מהירה - עברית
## אוטומציה Gmail לקלנדר

---

## סיכום מהיר

הפרויקט סורק מיילים ב-Gmail ויוצר אירועים בקלנדר באופן אוטומטי.

**מה שקיבלת:**
- ✅ 6 קבצי Python (כל אחד מתחת ל-150 שורות)
- ✅ תיעוד מלא באנגלית (README, PRD, TASKS)
- ✅ מדריך הקמת Google Cloud מפורט
- ✅ דוגמאות שימוש
- ✅ הכל מוכן לשימוש

---

## התקנה מהירה - 5 דקות

### 1. הורידי את הקבצים
```bash
unzip gmail_calendar_sync.zip
cd gmail_calendar_sync
```

### 2. התקיני תלויות
```bash
pip install -r requirements.txt
```

### 3. הקימי פרויקט ב-Google Cloud
**עקבי אחרי הקובץ: `GOOGLE_CLOUD_SETUP.md`**

סיכום צעדים:
1. צרי פרויקט חדש ב-Google Cloud Console
2. הפעילי Gmail API
3. הפעילי Calendar API
4. צרי OAuth credentials (Desktop app)
5. הורידי credentials.json
6. שימי אותו בתיקיית הפרויקט

### 4. הגדירי קונפיגורציה
```bash
cp .env.example .env
nano .env  # או כל עורך טקסט
```

הגדרה בסיסית:
```env
RUN_MODE=once
SEARCH_MODE=config
SEARCH_QUERY=is:unread subject:meeting
```

### 5. הריצי
```bash
python main.py
```

בהרצה הראשונה:
- ייפתח דפדפן לאישור הרשאות
- תאשרי גישה ל-Gmail ול-Calendar
- הקובץ token.pickle ייווצר אוטומטית

---

## ניסוי מהיר - בואי נבדוק שזה עובד!

### שלב 1: שלחי לעצמך מייל בדיקה

**מאת:** המייל הרגיל שלך  
**אל:** המייל שהגדרת בפרויקט  
**נושא:** `Team Meeting - AI`  
**תוכן:**
```
Hi,

Let's discuss the AI development course project.

See you!
```

### שלב 2: וודאי שה-.env מוגדר

```env
RUN_MODE=once
SEARCH_MODE=config
SEARCH_QUERY=is:unread subject:meeting
```

### שלב 3: הריצי

```bash
python main.py
```

### שלב 4: בדקי תוצאות

1. **בקונסול** - אמורה להופיע הודעה "✓ Event created"
2. **ב-Gmail** - המייל אמור להפוך ל-"נקרא" (לא bold)
3. **ב-Google Calendar** - אמור להופיע אירוע חדש "Team Meeting - AI"

![תוצאה בקלנדר](calendar_screenshot.png)

### רוצה לנסות שוב?

1. סמני את המייל כ-"לא נקרא" ב-Gmail
2. הריצי `python main.py` שוב
3. זה יעבד אותו מחדש!

---

## שני מצבי הרצה

### מצב 1: הרצה חד-פעמית
```env
RUN_MODE=once
```
- רץ פעם אחת
- סורק מיילים
- יוצר אירועים
- נגמר

### מצב 2: הרצה רציפה
```env
RUN_MODE=continuous
SCAN_INTERVAL=10
```
- רץ כל הזמן
- סורק כל 10 שניות
- Ctrl+C כדי לעצור

---

## שני מצבי חיפוש

### מצב 1: קונפיג (חיפוש רגיל)
```env
SEARCH_MODE=config
SEARCH_QUERY=is:unread subject:meeting
```

דוגמאות חיפוש:
- `is:unread from:boss@company.com`
- `subject:(meeting OR appointment)`
- `label:important is:unread`

### מצב 2: LLM (חיפוש בשפה טבעית + חילוץ חכם)
```env
SEARCH_MODE=llm
OPENAI_API_KEY=sk-proj-xxxxx
LLM_SEARCH_PROMPT=Find unread emails about meetings this week
```

**למה להשתמש ב-LLM?**
- 🎯 מחלץ תאריכים ושעות אמיתיים מגוף המייל
- 🎯 מוצא מיקום (Zoom, חדר ישיבות וכו')
- 🎯 מבין הקשר ולא רק מילות חיפוש
- 🎯 עובד עם שפה טבעית (גם עברית!)

**דוגמת מייל מפורט:**
```
Subject: Project Review Meeting
Body:
Hi Anna,

Let's meet to discuss the Gmail Calendar project.

Date: Thursday, January 30th
Time: 2:00 PM - 3:30 PM
Location: Conference Room B

Agenda:
- Review progress
- Discuss next steps

Best regards
```

**מה ה-LLM עושה:**
1. ממיר את הפרומפט שלך לחיפוש Gmail
2. מוצא את המיילים
3. **מחלץ מהמייל:**
   - תאריך מדויק: 30 בינואר 2025
   - שעות מדויקות: 14:00-15:30 (לא ברירת המחדל 10:00!)
   - מיקום: Conference Room B
   - תיאור מפורט: כולל סדר יום

**התוצאה:**
אירוע בקלנדר עם **תאריך/שעה/מיקום אמיתיים** במקום ברירת מחדל!

**מתי כדאי להשתמש:**
- ✅ מיילים עם תאריכים ושעות ספציפיים
- ✅ הזמנות לפגישות מפורטות  
- ✅ כשצריך לחלץ מיקום אוטומטית
- ❌ לא כדאי למיילים פשוטים → תשתמשי ב-config (חינם!)

**עלות:** ~₪0.10-0.20 למייל (רק כשמשתמשים ב-LLM mode)

---

## מבנה הפרויקט

```
gmail_calendar_sync/
├── main.py                 # נקודת כניסה ראשית
├── config.py              # ניהול הגדרות
├── auth.py                # התחברות ל-Google
├── gmail_scanner.py       # סריקת Gmail
├── calendar_manager.py    # יצירת אירועי קלנדר
├── llm_helper.py          # אינטגרציה עם OpenAI
├── .env                   # ההגדרות שלך (צרי מ-.env.example)
├── credentials.json       # מ-Google Cloud (הורידי)
└── token.pickle           # נוצר אוטומטית בהרצה ראשונה
```

---

## דוגמאות שימוש מהירות

### דוגמה 1: פגישות מהבוס
```env
RUN_MODE=once
SEARCH_MODE=config
SEARCH_QUERY=is:unread from:boss@company.com subject:meeting
```

### דוגמה 2: ניטור רציף של מיילים חשובים
```env
RUN_MODE=continuous
SCAN_INTERVAL=30
SEARCH_MODE=config
SEARCH_QUERY=is:unread is:important
```

### דוגמה 3: AI חכם
```env
RUN_MODE=once
SEARCH_MODE=llm
OPENAI_API_KEY=sk-proj-xxxxx
LLM_SEARCH_PROMPT=Find unread emails about appointments this week
```

---

## פתרון בעיות נפוצות

### "credentials.json not found"
- ✅ וודאי שהקובץ נקרא בדיוק `credentials.json`
- ✅ נמצא בתיקיית הפרויקט (ליד main.py)

### "Access blocked"
- ✅ לכי ל-OAuth consent screen ב-Google Cloud
- ✅ וודאי שאת ב-Test users
- ✅ מחקי token.pickle ונסי שוב

### "No emails found"
- ✅ בדקי את ה-query ב-Gmail (אותיות חיפוש)
- ✅ וודאי שיש מיילים לא קרואים שמתאימים

### הדפדפן לא נפתח
- ✅ העתיקי את הקישור מהטרמינל
- ✅ פתחי ידנית בדפדפן

---

## עבודת הבית - Checklist

לפני הגשה:
- [ ] כל הקבצים מתחת ל-150 שורות ✅ (כבר בדקתי!)
- [ ] יש README באנגלית ✅
- [ ] יש PRD באנגלית ✅
- [ ] יש TASKS באנגלית ✅
- [ ] הקוד עובד במצב config ✅
- [ ] הקוד עובד במצב llm ✅ (אם יש API key)
- [ ] שני מצבי הרצה עובדים ✅
- [ ] המיילים מסומנים כנקראו ✅
- [ ] האירועים נוצרים בקלנדר ✅

להדגמה:
- הראי הרצה במצב config
- הראי הרצה במצב llm (אופציונלי)
- הראי שהמייל סומן כנקרא
- הראי את האירוע שנוצר בקלנדר

---

## טיפים חשובים

### 1. בטיחות
- **לעולם לא** תעלי credentials.json לגיטהאב!
- **לעולם לא** תשתפי OPENAI_API_KEY
- השתמשי ב-.gitignore (כבר מוכן)

### 2. חיסכון
- מצב config: חינם לגמרי
- מצב LLM: עולה כסף (~$0.03 למייל)
- תחילי עם config, עברי ל-LLM רק אם צריך

### 3. בדיקות
- תמיד תריצי `RUN_MODE=once` קודם
- וודאי שהכל עובד
- רק אז עברי ל-continuous

### 4. קריאת חומר
- `GOOGLE_CLOUD_SETUP.md` - הקמה מפורטת
- `README.md` - תיעוד מלא
- `EXAMPLES.md` - דוגמאות שימוש
- `PRD.md` - דרישות מוצר
- `TASKS.md` - פירוק משימות

---

## תמיכה

בעיות עם:
- **Google APIs**: Google Cloud Console
- **OpenAI**: OpenAI Platform  
- **קוד**: בדקי הודעות שגיאה

**הצלחה בעבודה!** 🎉

---

## קישורים מועילים

- [Google Cloud Console](https://console.cloud.google.com/)
- [Gmail API Docs](https://developers.google.com/gmail/api)
- [Calendar API Docs](https://developers.google.com/calendar/api)
- [OpenAI Platform](https://platform.openai.com/)

---

**גרסה:** 1.0  
**תאריך:** ינואר 2026
