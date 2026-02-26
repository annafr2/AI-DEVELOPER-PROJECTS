# Git Upload Instructions 📤

## מבנה התיקיות שנוצר:

```
temperature-conversion-nn/
├── README.md                           # מדריך ראשי
├── .gitignore                          # קבצים להתעלם מהם
├── temp_conversion_nn.py              # הקוד הראשי
├── notebooks/
│   └── temperature_conversion_nn.ipynb # Jupyter Notebook
├── images/
│   ├── loss_curve.png                 # גרף עקומת למידה
│   └── prediction_comparison.png      # השוואת תחזיות
└── docs/
    └── PRD.md                         # מסמך דרישות מוצר
```

---

## שיטת העבודה שלך ב-VSC:

### שלב 1: פתיחת התיקייה ב-VS Code

1. פתחי VS Code
2. File → Open Folder
3. בחרי את התיקייה `temperature-conversion-nn`

### שלב 2: אתחול Git (אם עדיין לא עשית)

פתחי טרמינל ב-VSC (Ctrl+`) והריצי:

```bash
git init
```

### שלב 3: בדיקת הקבצים

בחלון ה-Source Control (Ctrl+Shift+G), תראי את כל הקבצים החדשים:
- ✓ README.md
- ✓ temp_conversion_nn.py
- ✓ .gitignore
- ✓ notebooks/temperature_conversion_nn.ipynb
- ✓ images/loss_curve.png
- ✓ images/prediction_comparison.png
- ✓ docs/PRD.md

### שלב 4: Commit ראשון

בטרמינל או ב-Source Control panel:

```bash
git add .
git commit -m "Initial commit: Temperature conversion neural network project"
```

או ב-UI של VSC:
1. לחצי על הפלוס ליד "Changes" (stage all)
2. כתבי הודעת commit למעלה
3. לחצי על ה-✓ (Commit)

### שלב 5: יצירת Repository ב-GitHub

1. פתחי https://github.com
2. לחצי על "+" → "New repository"
3. שם: `temperature-conversion-nn`
4. תיאור: `Neural network that learns Celsius to Fahrenheit conversion`
5. Public/Private (לפי בחירתך)
6. **אל** תסמני "Initialize with README" (כבר יש לנו)
7. לחצי "Create repository"

### שלב 6: חיבור ל-Remote

GitHub יציג לך פקודות. העתיקי והריצי בטרמינל של VSC:

```bash
git remote add origin https://github.com/YOUR-USERNAME/temperature-conversion-nn.git
git branch -M main
git push -u origin main
```

**החליפי `YOUR-USERNAME` בשם המשתמש שלך ב-GitHub!**

---

## אלטרנטיבה - דרך ה-UI של VSC:

### אם יש לך GitHub extension ב-VSC:

1. Ctrl+Shift+P
2. חפשי: "GitHub: Publish to GitHub"
3. בחרי שם: `temperature-conversion-nn`
4. Public/Private
5. סמני את כל הקבצים
6. לחצי OK

זהו! זה יעלה הכל אוטומטית.

---

## אחרי ההעלאה - בדיקה:

1. פתחי את ה-repo ב-GitHub
2. ודאי שאת רואה:
   - ✓ README עם התמונות
   - ✓ התיקייה `images` עם שתי התמונות
   - ✓ התיקייה `notebooks` עם ה-notebook
   - ✓ התיקייה `docs` עם ה-PRD
   - ✓ קובץ ה-Python הראשי

3. בדקי שהתמונות מוצגות ב-README (GitHub יציג אותן אוטומטית)

---

## שינויים עתידיים:

אם תרצי לעדכן משהו:

```bash
git add .
git commit -m "תיאור השינוי"
git push
```

או דרך ה-Source Control panel ב-VSC:
1. Stage changes (לחצי על +)
2. כתבי commit message
3. לחצי על ✓ (Commit)
4. לחצי על ☁️ (Push) או Sync Changes

---

## טיפים:

### תמונות ב-README:
- GitHub יציג אוטומטית תמונות שנמצאות ב-repo
- הנתיב `images/loss_curve.png` יעבוד מושלם
- אם התמונות לא מופיעות, תקני את הנתיב ל-`./images/...`

### Jupyter Notebook:
- GitHub מציג notebooks באופן יפה אוטומטית
- אפשר לפתוח את `notebooks/temperature_conversion_nn.ipynb` ישירות ב-GitHub

### Clone בעתיד:
```bash
git clone https://github.com/YOUR-USERNAME/temperature-conversion-nn.git
```

---

## בעיות נפוצות:

### התמונות לא מוצגות ב-README:
- ודאי שהנתיבים נכונים: `images/loss_curve.png`
- ודאי שהתמונות הועלו לגיט
- נסי נתיב מלא: `https://github.com/YOUR-USERNAME/temperature-conversion-nn/raw/main/images/loss_curve.png`

### "Permission denied":
```bash
git remote set-url origin https://YOUR-USERNAME@github.com/YOUR-USERNAME/temperature-conversion-nn.git
```

### קבצים גדולים מדי:
- הקבצים שלנו קטנים (התמונות ~200KB)
- אם בעתיד תצטרכי להעלות קבצים גדולים, תשתמשי ב-Git LFS

---

**מוכנה להעלאה! 🚀**
