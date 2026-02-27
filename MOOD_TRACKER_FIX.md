# Mood Tracker Error: Troubleshooting Guide

## Problem
When clicking "Log Mood for Today", you get an error message: **"Failed to log mood"**

---

## Quick Fix Steps

### Step 1: Check if Backend is Running ⚠️ MOST COMMON ISSUE

**Open a PowerShell terminal and run:**
```powershell
cd C:\Users\savit\Hackathon\NIT\NeuraLife+\NeuraLife+\backend
python run.py
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**If you see errors instead:**
- Missing module errors → Run: `pip install -r requirements.txt`
- Port already in use → Another backend is running, close it first
- Python not found → Make sure Python 3.7+ is installed

**⚠️ Leave this terminal open!** The backend must keep running while you use the app.

---

### Step 2: Run the Diagnostic Script

**In a NEW PowerShell terminal:**
```powershell
cd C:\Users\savit\Hackathon\NIT\NeuraLife+\NeuraLife+\backend
python check_mood_endpoint.py
```

**Expected output if everything is OK:**
```
TEST 1: Checking if backend is running...
✅ Backend is running on http://localhost:8000

TEST 2: Testing mood endpoint without authentication...
✅ Endpoint exists and requires authentication (expected)

TEST 3: Checking if mood_entries table exists...
✅ mood_entries table exists
   Columns: id, user_id, mood, intensity, notes, activities, date, created_at
```

**If you see errors:**
- ❌ Backend is NOT running → Go back to Step 1
- ❌ mood_entries table does NOT exist → The database wasn't initialized properly

---

### Step 3: Check Frontend Error Details

**I've updated the frontend to show better error messages.** Now when you try to log a mood:

1. **Open the browser console** (Press F12)
2. **Go to the Console tab**
3. **Try submitting a mood again**
4. **Look for red error messages** - they will now tell you exactly what's wrong:

**Possible errors and fixes:**

| Error Message | Cause | Fix |
|--------------|-------|-----|
| "Server not responding. Make sure backend is running..." | Backend is off | Start backend (Step 1) |
| "Failed to log mood: Unauthorized" | Token expired | Log out and log back in |
| "Failed to log mood: 500 Internal Server Error" | Backend crash | Check backend terminal for Python errors |
| "Network Error" / CORS error | Wrong API URL | Backend must be on localhost:8000 |

---

## Step 4: Verify Database Tables Were Created

**If the diagnostic script says tables are missing:**

```powershell
cd C:\Users\savit\Hackathon\NIT\NeuraLife+\NeuraLife+\backend
python -c "from app.database import Base, engine; from app import models; Base.metadata.create_all(bind=engine); print('Tables created successfully!')"
```

Then **restart the backend server** (Step 1).

---

## Step 5: Test with Fresh Login

**Sometimes the authentication token expires.** Try this:

1. **Log out** from NeuraLife+ (click your profile → Logout)
2. **Close the browser** completely
3. **Reopen browser** and go to http://localhost:5173
4. **Log back in** with your credentials
5. **Try logging a mood again**

---

## Step 6: Check Browser Network Tab

**If the error message still isn't clear:**

1. **Open browser DevTools** (F12)
2. **Go to the "Network" tab**
3. **Try submitting a mood**
4. **Look for a red entry** called `log` or `mood`
5. **Click on it** and check:
   - **Status**: Should be 200. If 401 → auth issue, if 500 → backend crash, if 0/failed → backend not running
   - **Response**: Shows the actual error from the server

---

## Common Issues and Solutions

### Issue 1: "ERR_CONNECTION_REFUSED"
**Cause:** Backend is not running  
**Fix:** Run `python run.py` in backend folder

### Issue 2: "401 Unauthorized"
**Cause:** Authentication token is invalid/expired  
**Fix:** Log out and log back in

### Issue 3: "500 Internal Server Error"
**Cause:** Python error in backend (likely database issue)  
**Fix:** 
1. Check the backend terminal for Python error traceback
2. Make sure all models are imported correctly
3. Try recreating database tables (Step 4)

### Issue 4: "CORS Error"
**Cause:** CORS not configured properly  
**Fix:** Backend main.py should have:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 5: Missing Python Packages
**Cause:** Dependencies not installed  
**Fix:**
```powershell
cd backend
pip install -r requirements.txt
```

---

## Testing the Fix

Once you've followed the steps above, **test the mood tracker**:

1. ✅ Backend running in terminal
2. ✅ Diagnostic script passes all tests
3. ✅ Frontend loads without console errors
4. ✅ You're logged in with a fresh token

**Try logging a mood:**
1. Go to http://localhost:5173/mood-tracker
2. Click a mood emoji (e.g., 😊)
3. Adjust intensity slider
4. Select some activities
5. Add notes (optional)
6. Click **"Log Mood for Today"**

**Expected result:**
- ✅ Green success message appears
- ✅ "You earned X NeuraCoins!" shows
- ✅ Your mood appears in the "Recent Moods" sidebar
- ✅ Analytics update with your new data

---

## Still Not Working?

**Share this information:**

1. **Output from diagnostic script** (`check_mood_endpoint.py`)
2. **Backend terminal output** (any errors in red)
3. **Browser console errors** (F12 → Console tab)
4. **Network tab details** (F12 → Network → click failed request → screenshot)

**I'll help debug from there!**

---

## Prevention Tips

**To avoid this in the future:**

1. ✅ **Always start backend before frontend**
   ```powershell
   # Terminal 1
   cd backend
   python run.py
   
   # Terminal 2 (new terminal)
   cd frontend
   npm run dev
   ```

2. ✅ **Check backend terminal** for errors before testing features

3. ✅ **Refresh login** if you haven't used the app in a while (tokens expire)

4. ✅ **Keep backend running** while using the app (don't close the terminal!)
