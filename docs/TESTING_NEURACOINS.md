<<<<<<< HEAD
# NeuraCoins System Testing Guide 🧪

## Quick Test Checklist

### ✅ Backend Tests

#### Test 1: New User Registration
```bash
# Register a new user (not test2-test6)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser123","email":"new@test.com","password":"test123"}'

# Expected: User created with neuracoins: 0
```

#### Test 2: Test User Registration
```bash
# Register as test user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test7","email":"test7@test.com","password":"test123"}'

# Expected: User created with neuracoins: 0 (only test2-test6 get 5000)

curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test3","email":"test3new@test.com","password":"test123"}'

# Expected: User created with neuracoins: 5000
```

#### Test 3: First Quiz Completion
```bash
# 1. Login as user
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test1","password":"123456"}'

# Save the token from response

# 2. Submit PHQ-9 quiz (first time)
curl -X POST http://localhost:8000/api/quiz/phq9/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"answers":[2,2,2,2,2,2,2,2,2]}'

# Expected response:
# {
#   "score": 18,
#   "result": "...",
#   "severity": "Moderately Severe",
#   "first_time_completion": true,
#   "coins_earned": 500,
#   "total_coins": 500
# }
```

#### Test 4: Repeat Quiz Completion
```bash
# Submit same quiz again (should not earn coins)
curl -X POST http://localhost:8000/api/quiz/phq9/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"answers":[1,1,1,1,1,1,1,1,1]}'

# Expected:
# {
#   "score": 9,
#   "result": "...",
#   "severity": "Mild",
#   "first_time_completion": false,
#   "coins_earned": 0,
#   "total_coins": 500  # Unchanged
# }
```

#### Test 5: Different Quiz Type
```bash
# Submit GAD-7 (different quiz, should earn coins)
curl -X POST http://localhost:8000/api/quiz/gad7/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"answers":[2,2,2,2,2,2,2]}'

# Expected:
# {
#   "first_time_completion": true,
#   "coins_earned": 500,
#   "total_coins": 1000  # 500 + 500
# }
```

---

### 🎨 Frontend Tests

#### Test 1: View Starting Balance
1. Open http://localhost:5174
2. Login as test1 (should have 0 coins after migration)
3. Check navbar: Should show "0 NeuraCoins"
4. Login as test2 (test user)
5. Check navbar: Should show "5000 NeuraCoins"

#### Test 2: Quiz Reward Notification
1. Login as user who hasn't completed PHQ-9
2. Navigate to Quizzes/Resources
3. Start and complete PHQ-9
4. After submission, should see:
   - 🎉 Animated gold celebration card
   - "You earned 500 NeuraCoins!"
   - Updated total balance display
   - "First time completing this assessment!" message

#### Test 3: No Reward for Repeat
1. Complete same quiz again
2. Should see normal results screen
3. No celebration notification
4. Coin balance unchanged

#### Test 4: Multiple Quizzes
1. Complete all 3 assessments (PHQ-9, GAD-7, PSS-10)
2. Should earn 500 coins each time (1500 total)
3. Each should show celebration
4. Final balance: 1500 coins

#### Test 5: Premium Upgrade
1. User with 1000+ coins
2. Navigate to Premium page
3. Click "Upgrade to Premium"
4. Balance should decrease by 1000
5. Should have premium access

---

### 📊 Database Verification

#### Check User Balances
```python
# Run in backend directory
python -c "
from app.database import SessionLocal
from app.models import User

db = SessionLocal()

print('\n=== All Users ===')
for user in db.query(User).all():
    print(f'{user.username}: {user.neuracoins} coins (Premium: {user.is_premium})')

db.close()
"
```

#### Check Quiz Results
```python
python -c "
from app.database import SessionLocal
from app.models import QuizResult, User

db = SessionLocal()

print('\n=== Quiz Completions ===')
for result in db.query(QuizResult).join(User).all():
    print(f'{result.user.username} - {result.quiz_type}: Score {result.score}')

db.close()
"
```

---

### 🔄 Reset Test Environment

#### Reset Single User
```python
# backend/reset_user.py
from app.database import SessionLocal
from app.models import User, QuizResult

db = SessionLocal()

username = "test1"
user = db.query(User).filter(User.username == username).first()

if user:
    # Reset coins
    user.neuracoins = 0
    
    # Delete quiz results
    db.query(QuizResult).filter(QuizResult.user_id == user.id).delete()
    
    db.commit()
    print(f"Reset {username}: 0 coins, no quiz history")

db.close()
```

#### Run Migration Again
```bash
cd backend
python update_neuracoins.py
```

---

### 🎯 Complete User Journey Test

**Scenario: New User to Premium**

1. **Registration**
   - Register as new user
   - Verify: 0 coins in navbar

2. **First Assessment**
   - Complete PHQ-9
   - Verify: Celebration appears
   - Verify: Balance = 500 coins

3. **Second Assessment**
   - Complete GAD-7
   - Verify: Another celebration
   - Verify: Balance = 1,000 coins

4. **Premium Upgrade**
   - Go to Premium page
   - Click "Upgrade to Premium"
   - Verify: Balance = 0 coins
   - Verify: Premium badge appears

5. **Third Assessment**
   - Complete PSS-10
   - Verify: Celebration appears (can still earn)
   - Verify: Balance = 500 coins

6. **Book Therapy**
   - Navigate to Therapy Sessions
   - Book Video Call (500 coins)
   - Verify: Balance = 0 coins

7. **Repeat Assessment**
   - Retake PHQ-9
   - Verify: NO celebration
   - Verify: Balance still 0 coins
   - Verify: New score recorded

---

### 🐛 Troubleshooting

#### Issue: No coins earned after quiz
**Check:**
- Backend logs for errors
- Quiz submission response includes `first_time_completion` field
- Database has QuizResult entries
- User exists in database

#### Issue: Celebration not showing
**Check:**
- `result.first_time_completion === true` in response
- `result.coins_earned > 0` in response
- Browser console for errors
- Component re-render after API call

#### Issue: Test users not getting 5000 coins
**Check:**
- Username is exactly test2, test3, test4, test5, or test6
- Registration endpoint has correct logic
- Database was migrated with update_neuracoins.py

#### Issue: Coins not persisting
**Check:**
- Database commit called after coin update
- Token is valid (not expired)
- User ID matches in database

---

### 📝 Expected Results Summary

| Action | Starting Coins | Ending Coins | Notes |
|--------|---------------|--------------|-------|
| New registration | 0 | 0 | Not test2-test6 |
| Test user registration | 0 | 5000 | Username test2-test6 |
| First PHQ-9 | X | X + 500 | Celebration shown |
| Repeat PHQ-9 | X | X | No celebration |
| First GAD-7 | X | X + 500 | Celebration shown |
| First PSS-10 | X | X + 500 | Celebration shown |
| Premium upgrade | X | X - 1000 | Must have 1000+ |
| Video call booking | X | X - 500 | Premium only |

---

### ✨ Success Criteria

- ✅ New users start with 0 coins
- ✅ Test users (test2-test6) start with 5000 coins
- ✅ First quiz completion earns 500 coins
- ✅ Repeat quiz completion earns 0 coins
- ✅ Celebration notification shows for first time
- ✅ No notification for repeat
- ✅ Coin balance updates in real-time
- ✅ All 3 quizzes can earn coins (1500 max)
- ✅ Premium costs 1000 coins
- ✅ Therapy sessions deduct coins

---

## Running Tests

### Quick Test Commands
```bash
# 1. Start backend (Terminal 1)
cd backend
start_backend.bat

# 2. Start frontend (Terminal 2)
cd frontend
start_frontend.bat

# 3. Run migration (Terminal 3)
cd backend
python update_neuracoins.py

# 4. Open browser
# http://localhost:5174

# 5. Test as new user
# Register → Complete quizzes → Watch for celebrations

# 6. Test as test user
# Login as test2 → Should have 5000 coins immediately
```

---

Happy Testing! 🚀💰🎉
=======
# NeuraCoins System Testing Guide 🧪

## Quick Test Checklist

### ✅ Backend Tests

#### Test 1: New User Registration
```bash
# Register a new user (not test2-test6)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"newuser123","email":"new@test.com","password":"test123"}'

# Expected: User created with neuracoins: 0
```

#### Test 2: Test User Registration
```bash
# Register as test user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test7","email":"test7@test.com","password":"test123"}'

# Expected: User created with neuracoins: 0 (only test2-test6 get 5000)

curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test3","email":"test3new@test.com","password":"test123"}'

# Expected: User created with neuracoins: 5000
```

#### Test 3: First Quiz Completion
```bash
# 1. Login as user
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test1","password":"123456"}'

# Save the token from response

# 2. Submit PHQ-9 quiz (first time)
curl -X POST http://localhost:8000/api/quiz/phq9/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"answers":[2,2,2,2,2,2,2,2,2]}'

# Expected response:
# {
#   "score": 18,
#   "result": "...",
#   "severity": "Moderately Severe",
#   "first_time_completion": true,
#   "coins_earned": 500,
#   "total_coins": 500
# }
```

#### Test 4: Repeat Quiz Completion
```bash
# Submit same quiz again (should not earn coins)
curl -X POST http://localhost:8000/api/quiz/phq9/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"answers":[1,1,1,1,1,1,1,1,1]}'

# Expected:
# {
#   "score": 9,
#   "result": "...",
#   "severity": "Mild",
#   "first_time_completion": false,
#   "coins_earned": 0,
#   "total_coins": 500  # Unchanged
# }
```

#### Test 5: Different Quiz Type
```bash
# Submit GAD-7 (different quiz, should earn coins)
curl -X POST http://localhost:8000/api/quiz/gad7/submit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"answers":[2,2,2,2,2,2,2]}'

# Expected:
# {
#   "first_time_completion": true,
#   "coins_earned": 500,
#   "total_coins": 1000  # 500 + 500
# }
```

---

### 🎨 Frontend Tests

#### Test 1: View Starting Balance
1. Open http://localhost:5174
2. Login as test1 (should have 0 coins after migration)
3. Check navbar: Should show "0 NeuraCoins"
4. Login as test2 (test user)
5. Check navbar: Should show "5000 NeuraCoins"

#### Test 2: Quiz Reward Notification
1. Login as user who hasn't completed PHQ-9
2. Navigate to Quizzes/Resources
3. Start and complete PHQ-9
4. After submission, should see:
   - 🎉 Animated gold celebration card
   - "You earned 500 NeuraCoins!"
   - Updated total balance display
   - "First time completing this assessment!" message

#### Test 3: No Reward for Repeat
1. Complete same quiz again
2. Should see normal results screen
3. No celebration notification
4. Coin balance unchanged

#### Test 4: Multiple Quizzes
1. Complete all 3 assessments (PHQ-9, GAD-7, PSS-10)
2. Should earn 500 coins each time (1500 total)
3. Each should show celebration
4. Final balance: 1500 coins

#### Test 5: Premium Upgrade
1. User with 1000+ coins
2. Navigate to Premium page
3. Click "Upgrade to Premium"
4. Balance should decrease by 1000
5. Should have premium access

---

### 📊 Database Verification

#### Check User Balances
```python
# Run in backend directory
python -c "
from app.database import SessionLocal
from app.models import User

db = SessionLocal()

print('\n=== All Users ===')
for user in db.query(User).all():
    print(f'{user.username}: {user.neuracoins} coins (Premium: {user.is_premium})')

db.close()
"
```

#### Check Quiz Results
```python
python -c "
from app.database import SessionLocal
from app.models import QuizResult, User

db = SessionLocal()

print('\n=== Quiz Completions ===')
for result in db.query(QuizResult).join(User).all():
    print(f'{result.user.username} - {result.quiz_type}: Score {result.score}')

db.close()
"
```

---

### 🔄 Reset Test Environment

#### Reset Single User
```python
# backend/reset_user.py
from app.database import SessionLocal
from app.models import User, QuizResult

db = SessionLocal()

username = "test1"
user = db.query(User).filter(User.username == username).first()

if user:
    # Reset coins
    user.neuracoins = 0
    
    # Delete quiz results
    db.query(QuizResult).filter(QuizResult.user_id == user.id).delete()
    
    db.commit()
    print(f"Reset {username}: 0 coins, no quiz history")

db.close()
```

#### Run Migration Again
```bash
cd backend
python update_neuracoins.py
```

---

### 🎯 Complete User Journey Test

**Scenario: New User to Premium**

1. **Registration**
   - Register as new user
   - Verify: 0 coins in navbar

2. **First Assessment**
   - Complete PHQ-9
   - Verify: Celebration appears
   - Verify: Balance = 500 coins

3. **Second Assessment**
   - Complete GAD-7
   - Verify: Another celebration
   - Verify: Balance = 1,000 coins

4. **Premium Upgrade**
   - Go to Premium page
   - Click "Upgrade to Premium"
   - Verify: Balance = 0 coins
   - Verify: Premium badge appears

5. **Third Assessment**
   - Complete PSS-10
   - Verify: Celebration appears (can still earn)
   - Verify: Balance = 500 coins

6. **Book Therapy**
   - Navigate to Therapy Sessions
   - Book Video Call (500 coins)
   - Verify: Balance = 0 coins

7. **Repeat Assessment**
   - Retake PHQ-9
   - Verify: NO celebration
   - Verify: Balance still 0 coins
   - Verify: New score recorded

---

### 🐛 Troubleshooting

#### Issue: No coins earned after quiz
**Check:**
- Backend logs for errors
- Quiz submission response includes `first_time_completion` field
- Database has QuizResult entries
- User exists in database

#### Issue: Celebration not showing
**Check:**
- `result.first_time_completion === true` in response
- `result.coins_earned > 0` in response
- Browser console for errors
- Component re-render after API call

#### Issue: Test users not getting 5000 coins
**Check:**
- Username is exactly test2, test3, test4, test5, or test6
- Registration endpoint has correct logic
- Database was migrated with update_neuracoins.py

#### Issue: Coins not persisting
**Check:**
- Database commit called after coin update
- Token is valid (not expired)
- User ID matches in database

---

### 📝 Expected Results Summary

| Action | Starting Coins | Ending Coins | Notes |
|--------|---------------|--------------|-------|
| New registration | 0 | 0 | Not test2-test6 |
| Test user registration | 0 | 5000 | Username test2-test6 |
| First PHQ-9 | X | X + 500 | Celebration shown |
| Repeat PHQ-9 | X | X | No celebration |
| First GAD-7 | X | X + 500 | Celebration shown |
| First PSS-10 | X | X + 500 | Celebration shown |
| Premium upgrade | X | X - 1000 | Must have 1000+ |
| Video call booking | X | X - 500 | Premium only |

---

### ✨ Success Criteria

- ✅ New users start with 0 coins
- ✅ Test users (test2-test6) start with 5000 coins
- ✅ First quiz completion earns 500 coins
- ✅ Repeat quiz completion earns 0 coins
- ✅ Celebration notification shows for first time
- ✅ No notification for repeat
- ✅ Coin balance updates in real-time
- ✅ All 3 quizzes can earn coins (1500 max)
- ✅ Premium costs 1000 coins
- ✅ Therapy sessions deduct coins

---

## Running Tests

### Quick Test Commands
```bash
# 1. Start backend (Terminal 1)
cd backend
start_backend.bat

# 2. Start frontend (Terminal 2)
cd frontend
start_frontend.bat

# 3. Run migration (Terminal 3)
cd backend
python update_neuracoins.py

# 4. Open browser
# http://localhost:5174

# 5. Test as new user
# Register → Complete quizzes → Watch for celebrations

# 6. Test as test user
# Login as test2 → Should have 5000 coins immediately
```

---

Happy Testing! 🚀💰🎉
>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
