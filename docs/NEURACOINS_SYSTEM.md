# NeuraCoins Economy System 💰

## Overview
NeuraCoins is NeuraLife's virtual currency that encourages user engagement with mental health assessments and rewards proactive wellness activities.

---

## Starting Balance

### New Users
- **Starting Coins**: 0 NeuraCoins
- **Philosophy**: Earn through engagement, not handouts
- **Goal**: Incentivize platform usage and mental health awareness

### Test Accounts (test2 - test6)
- **Starting Coins**: 5,000 NeuraCoins
- **Purpose**: Testing premium features and therapy sessions
- **Accounts**: test2, test3, test4, test5, test6

---

## Earning NeuraCoins

### 🎯 Quiz/Assessment Completion (First Time Bonus)
Users earn **500 NeuraCoins** for completing each mental health assessment for the **first time**.

| Assessment | First Completion Reward | Repeat Completion |
|------------|------------------------|-------------------|
| PHQ-9 (Depression) | 500 coins | 0 coins |
| GAD-7 (Anxiety) | 500 coins | 0 coins |
| PSS-10 (Stress) | 500 coins | 0 coins |

**Maximum Quiz Earnings**: 1,500 NeuraCoins (500 × 3 assessments)

#### How It Works:
1. User completes an assessment (e.g., PHQ-9)
2. Backend checks if user has completed this assessment before
3. If first time: Award 500 coins + show celebration notification
4. If repeat: No coins earned (can still retake for tracking progress)

#### User Experience:
- ✅ Big celebration popup: "🎉 You earned 500 NeuraCoins!"
- ✅ Shows updated total balance
- ✅ Animated notification with gold theme
- ✅ "First time completing this assessment!" message

---

## Spending NeuraCoins

### Premium Membership
- **Cost**: 1,000 NeuraCoins
- **Benefits**: AI therapy chat, therapy session booking, premium resources
- **After Quiz Earnings**: Need 2 assessments minimum (500 × 2 = 1,000)

### Therapy Sessions
- **In Person**: 600 NeuraCoins per session
- **Video Call**: 500 NeuraCoins per session
- **Chat**: 500 NeuraCoins per session

---

## Economy Math

### Pathway to Premium
```
New User Registration: 0 coins
↓
Complete PHQ-9 Assessment: +500 coins = 500 total
↓
Complete GAD-7 Assessment: +500 coins = 1,000 total
↓
Upgrade to Premium: -1,000 coins = 0 remaining
```

### Pathway to Therapy
```
Premium User with 0 coins
↓
Complete PSS-10 Assessment: +500 coins = 500 total
↓
Book Video Call Session: -500 coins = 0 remaining
```

### Full Engagement Path
```
New User: 0 coins
↓
Complete all 3 assessments: +1,500 coins = 1,500 total
↓
Upgrade to Premium: -1,000 coins = 500 remaining
↓
Book Video Call Session: -500 coins = 0 remaining
```

---

## Implementation Details

### Backend (FastAPI)

#### Registration (`/api/auth/register`)
```python
initial_coins = 0
if user_data.username in ['test2', 'test3', 'test4', 'test5', 'test6']:
    initial_coins = 5000

new_user = User(..., neuracoins=initial_coins)
```

#### Quiz Submission (`/api/quiz/{quiz_id}/submit`)
```python
# Check if first time
previous_results = db.query(QuizResult).filter(
    QuizResult.user_id == current_user.id,
    QuizResult.quiz_type == quiz_id
).count()

is_first_time = (previous_results == 0)
coins_earned = 0

if is_first_time:
    coins_earned = 500
    current_user.neuracoins += coins_earned
    db.commit()

# Return with reward info
return {
    "score": score,
    "result": interpretation,
    "severity": severity,
    "first_time_completion": is_first_time,
    "coins_earned": coins_earned,
    "total_coins": current_user.neuracoins
}
```

### Frontend (React)

#### Reward Notification (Quiz.jsx)
```jsx
{result.first_time_completion && result.coins_earned > 0 && (
  <div className="mb-6 animate-bounce">
    <div className="bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600 rounded-xl p-6">
      <div className="text-5xl mb-3">🎉</div>
      <h3 className="text-2xl font-bold text-white mb-2">Congratulations!</h3>
      <p className="text-white text-lg mb-3">
        You earned <span className="font-bold text-3xl">{result.coins_earned}</span> NeuraCoins!
      </p>
      <div className="bg-yellow-300 bg-opacity-30 rounded-lg p-3">
        <p className="text-white font-semibold">
          💰 Total Balance: {result.total_coins} NeuraCoins
        </p>
      </div>
    </div>
  </div>
)}
```

---

## Database Migration

### Update Script (`update_neuracoins.py`)
Updates all existing users to new coin system:
- Test users (test2-test6): 5,000 coins
- Regular users: 0 coins

```bash
cd backend
python update_neuracoins.py
```

---

## Future Earning Opportunities

### Potential Additions:
- 📅 **Daily Login Bonus**: 50 coins/day
- 🎯 **Streak Rewards**: Bonus for consecutive daily assessments
- 📝 **Journal Entries**: 100 coins per entry (max 3/day)
- 🏆 **Achievement Badges**: 200-1000 coins for milestones
- 🤝 **Community Engagement**: Coins for forum participation
- 📚 **Resource Completion**: 50 coins per resource read
- 🔔 **Notification Actions**: 25 coins for following up on reminders

---

## Benefits of This System

### User Engagement
- ✅ Encourages completion of mental health assessments
- ✅ Promotes self-awareness and progress tracking
- ✅ Gamifies wellness activities
- ✅ Provides tangible rewards for healthy behaviors

### Business Goals
- ✅ Increases platform usage and retention
- ✅ Generates valuable mental health data
- ✅ Creates pathway to premium conversion
- ✅ Reduces friction in user journey
- ✅ Encourages repeat visits

### Mental Health Benefits
- ✅ Regular assessment completion → Early detection
- ✅ Progress tracking → Better insights
- ✅ Positive reinforcement → Habit formation
- ✅ Lower barrier → Therapy access

---

## Testing Guide

### Test Scenario 1: New User Journey
1. Register as new user (not test2-test6)
2. Check balance: Should be 0 coins
3. Complete PHQ-9 assessment
4. See celebration: "You earned 500 NeuraCoins!"
5. Check balance: Should be 500 coins
6. Complete GAD-7 assessment  
7. See celebration again
8. Check balance: Should be 1,000 coins
9. Upgrade to Premium (costs 1,000)
10. Balance should be 0

### Test Scenario 2: Repeat Assessment
1. User with previous PHQ-9 completion
2. Complete PHQ-9 again
3. Should NOT see celebration
4. Balance should remain unchanged
5. Results still saved for tracking

### Test Scenario 3: Test User
1. Register as "test3"
2. Check balance: Should be 5,000 coins
3. Complete any assessment
4. Still earn 500 coins (5,500 total)
5. Can immediately access premium features

---

## API Response Examples

### Successful Quiz Submission (First Time)
```json
{
  "score": 12,
  "result": "Moderate depression",
  "severity": "Moderate",
  "first_time_completion": true,
  "coins_earned": 500,
  "total_coins": 1500
}
```

### Quiz Submission (Repeat)
```json
{
  "score": 8,
  "result": "Mild depression", 
  "severity": "Mild",
  "first_time_completion": false,
  "coins_earned": 0,
  "total_coins": 1500
}
```

---

## Summary

The NeuraCoins system creates a **virtuous cycle**:

1. User starts with 0 coins
2. Completes mental health assessments to earn coins
3. Uses coins to unlock premium features
4. Premium features provide better support
5. Better support leads to improved outcomes
6. Improved outcomes encourage continued use

**Result**: Engaged users, better mental health outcomes, sustainable platform growth. 🚀
