# Google Cloud Setup Guide
## Complete Step-by-Step Instructions

This guide will walk you through setting up Google Cloud project and credentials for the Gmail to Calendar Automation project.

---

## Prerequisites

- Google account (Gmail)
- Web browser
- 15-20 minutes

---

## Step 1: Create Google Cloud Project

### 1.1 Access Google Cloud Console
1. Go to https://console.cloud.google.com/
2. Sign in with your Google account
3. Accept terms of service if prompted

### 1.2 Create New Project
1. Click the **project dropdown** at the top of the page
   - It says "Select a project" or shows current project name
2. Click **"NEW PROJECT"** button (top right of dialog)
3. Fill in project details:
   - **Project name:** `gmail-calendar-automation` (or your choice)
   - **Organization:** Leave as "No organization" (unless you have one)
   - **Location:** Leave as default
4. Click **"CREATE"**
5. Wait 10-30 seconds for project creation
6. You'll see a notification when ready
7. Click **"SELECT PROJECT"** in the notification

**✓ Checkpoint:** You should see your project name in the top bar

---

## Step 2: Enable Required APIs

### 2.1 Navigate to API Library
1. In the left sidebar, click **"APIs & Services"**
2. Click **"Library"**
3. You'll see the API Library with search bar

### 2.2 Enable Gmail API
1. In the search bar, type: `Gmail API`
2. Click on **"Gmail API"** from results
3. Click the blue **"ENABLE"** button
4. Wait for activation (10-20 seconds)
5. You'll see "API enabled" message

### 2.3 Enable Google Calendar API
1. Click the **back arrow** or **"Go to Library"**
2. In the search bar, type: `Google Calendar API`
3. Click on **"Google Calendar API"** from results
4. Click the blue **"ENABLE"** button
5. Wait for activation

**✓ Checkpoint:** Both APIs should show "Manage" button instead of "Enable"

---

## Step 3: Configure OAuth Consent Screen

This tells users what your application will access.

### 3.1 Navigate to OAuth Consent Screen
1. In left sidebar: **APIs & Services** → **OAuth consent screen**
2. You'll see the consent screen configuration page

### 3.2 Choose User Type
1. Select **"External"**
   - Choose this unless you have Google Workspace organization
   - "Internal" is only for Google Workspace domains
2. Click **"CREATE"**

### 3.3 Fill OAuth App Information

**Page 1: App Information**

Required fields:
- **App name:** `Gmail Calendar Sync` (or your choice)
- **User support email:** Your email address (select from dropdown)
- **App logo:** Skip (optional)

Developer contact information:
- **Email addresses:** Your email address

Click **"SAVE AND CONTINUE"**

**Page 2: Scopes**
- Click **"SAVE AND CONTINUE"** (we'll add scopes in code)

**Page 3: Test Users**
1. Click **"+ ADD USERS"**
2. Enter your Gmail address
3. Click **"ADD"**
4. Click **"SAVE AND CONTINUE"**

**Page 4: Summary**
- Review information
- Click **"BACK TO DASHBOARD"**

**✓ Checkpoint:** OAuth consent screen shows "External" and "Testing" status

---

## Step 4: Create OAuth Credentials

### 4.1 Navigate to Credentials
1. In left sidebar: **APIs & Services** → **Credentials**
2. Click **"+ CREATE CREDENTIALS"** (top of page)
3. Select **"OAuth client ID"**

### 4.2 Configure OAuth Client

1. **Application type:** Select **"Desktop app"**
2. **Name:** `Gmail Calendar Desktop Client` (or your choice)
3. Click **"CREATE"**

### 4.3 Download Credentials

1. A dialog appears with **"OAuth client created"**
2. You'll see:
   - Client ID
   - Client secret
3. Click **"DOWNLOAD JSON"** button
4. Save the file to your computer

**IMPORTANT:** Rename the downloaded file to `credentials.json`

**✓ Checkpoint:** You have a file named `credentials.json` downloaded

---

## Step 5: Place Credentials in Project

### 5.1 Locate Your Project Directory
Find where you downloaded/cloned the project:
```
gmail_calendar_sync/
├── main.py
├── config.py
├── ...
└── (credentials.json goes here)
```

### 5.2 Move credentials.json
1. Move the downloaded `credentials.json` file
2. Place it in the **root** of the `gmail_calendar_sync` directory
3. It should be in the same folder as `main.py`

**✓ Checkpoint:** Run `ls` or check folder - you should see `credentials.json`

---

## Step 6: Verify Setup

### 6.1 Check File Structure
Your project should look like:
```
gmail_calendar_sync/
├── credentials.json          ← You added this
├── main.py
├── config.py
├── auth.py
├── gmail_scanner.py
├── calendar_manager.py
├── llm_helper.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── PRD.md
└── TASKS.md
```

### 6.2 Verify APIs are Enabled
1. Go back to Google Cloud Console
2. Navigate to: **APIs & Services** → **Dashboard**
3. You should see both:
   - Gmail API (with usage graphs)
   - Google Calendar API (with usage graphs)

**✓ Checkpoint:** Both APIs show in dashboard

---

## Step 7: First Authentication

### 7.1 Install Dependencies
```bash
pip install -r requirements.txt
```

### 7.2 Configure .env File
```bash
cp .env.example .env
```

Edit `.env` with your preferred settings (RUN_MODE, SEARCH_MODE, etc.)

### 7.3 Run First Time
```bash
python main.py
```

**What happens:**
1. Application starts
2. Browser window opens automatically
3. You see Google sign-in page

### 7.4 Grant Permissions

**In the browser:**

1. **Choose account:** Select your Google account
2. **Warning screen appears:**
   - "Google hasn't verified this app"
   - This is normal for testing apps!
3. Click **"Advanced"** (bottom left)
4. Click **"Go to Gmail Calendar Sync (unsafe)"**
5. **Permission screen:**
   - "Gmail Calendar Sync wants to access your Google Account"
   - You'll see requested permissions:
     - "See, edit, create, and delete all your Google Calendar events"
     - "Read, compose, send, and permanently delete all your email from Gmail"
6. Scroll down and click **"Continue"**
7. You'll see "The authentication flow has completed"
8. **Close the browser tab**

### 7.5 Check Authentication Success

**In your terminal:**
- You should see: "Authentication successful!"
- A new file `token.pickle` is created in your project folder
- The application continues running

**✓ Checkpoint:** Application is running and processing emails

---

## Troubleshooting Common Issues

### Issue 1: "credentials.json not found"

**Solution:**
- Check file name is exactly `credentials.json` (not `credentials (1).json`)
- Ensure it's in project root (same folder as main.py)
- Path should be: `gmail_calendar_sync/credentials.json`

### Issue 2: "Access blocked: This app's request is invalid"

**Solutions:**
1. Go to OAuth consent screen in Google Cloud
2. Check "Test users" includes your email
3. Ensure app is in "Testing" mode
4. Delete `token.pickle` and try again

### Issue 3: "The caller does not have permission"

**Solutions:**
1. Verify APIs are enabled:
   - Go to API Library
   - Search for Gmail API and Calendar API
   - Both should show "Manage" not "Enable"
2. Check OAuth scopes in consent screen
3. Delete `token.pickle` and re-authenticate

### Issue 4: "redirect_uri_mismatch"

**Solutions:**
1. Ensure you selected "Desktop app" type
2. Not "Web application"
3. Re-create OAuth credentials if needed

### Issue 5: Browser doesn't open

**Solutions:**
1. Copy the URL from terminal
2. Paste in browser manually
3. Continue authentication there
4. Check firewall settings

### Issue 6: "OAuth consent screen shows as published but shouldn't be"

**Solution:**
- This is fine for testing
- Your app stays in testing mode
- Only you (test users) can access it

---

## Security Best Practices

### ✅ DO:
- Keep `credentials.json` secret
- Add `credentials.json` to `.gitignore`
- Never commit to GitHub
- Only share with trusted team members
- Use test users list for limited access

### ❌ DON'T:
- Share credentials publicly
- Commit to version control
- Email credentials
- Screenshot and post online
- Use in production without review

---

## API Quotas and Limits

### Gmail API Quota
- **Per day:** 1,000,000,000 quota units
- **Per user per second:** 250 quota units
- **Typical usage:** 5-10 units per email processed
- **Your limit:** Effectively unlimited for this project

### Calendar API Quota
- **Per day:** 1,000,000 quota units
- **Per user per second:** 10 quota units
- **Typical usage:** 5 units per event created
- **Your limit:** Hundreds of thousands of events per day

### Monitor Usage
1. Go to Google Cloud Console
2. **APIs & Services** → **Dashboard**
3. Click on specific API
4. View "Quotas & System Limits"

---

## Cost Information

### Google APIs
- **Free tier:** Generous limits
- **This project:** Completely FREE
- **Billing:** Not required for these APIs
- **Limits:** More than enough for personal use

---

## Next Steps

After completing this setup:

1. ✅ You have working credentials
2. ✅ APIs are enabled
3. ✅ OAuth is configured
4. ✅ First authentication completed
5. ✅ `token.pickle` created

**You can now:**
- Run the application anytime
- No browser window needed (token saved)
- Token auto-refreshes when expired
- Modify configuration in `.env` file

---

## Reference Links

- [Google Cloud Console](https://console.cloud.google.com/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Calendar API Documentation](https://developers.google.com/calendar/api)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)

---

## Getting Help

If you encounter issues:

1. **Check this guide** - Most issues are covered
2. **Review error messages** - They usually indicate the problem
3. **Google Cloud Console** - Check API dashboard for errors
4. **Delete token.pickle** - Try re-authenticating
5. **Re-create credentials** - If all else fails

---

## Summary Checklist

Setup completion checklist:

- [ ] Created Google Cloud project
- [ ] Enabled Gmail API
- [ ] Enabled Google Calendar API
- [ ] Configured OAuth consent screen
- [ ] Added yourself as test user
- [ ] Created OAuth client ID (Desktop app)
- [ ] Downloaded credentials.json
- [ ] Placed credentials.json in project folder
- [ ] Installed Python dependencies
- [ ] Configured .env file
- [ ] Ran first authentication
- [ ] Granted permissions in browser
- [ ] Confirmed token.pickle created
- [ ] Application running successfully

**When all checked:** You're ready to use the application! 🎉

---

**Version:** 1.0  
**Last Updated:** January 2026
