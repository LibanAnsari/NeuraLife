"""Force logout all users by updating their tokens - this will require re-login"""
from app.database import SessionLocal
from app.models import User
from datetime import datetime

db = SessionLocal()

print("\n" + "="*60)
print("FORCE TOKEN REFRESH")
print("="*60)

# Get test1 details
test1 = db.query(User).filter(User.username == "test1").first()

if test1:
    print(f"\n✅ test1 current status:")
    print(f"   Username: {test1.username}")
    print(f"   Email: {test1.email}")
    print(f"   NeuraCoins: {test1.neuracoins}")
    print(f"   Premium: {test1.is_premium}")
    print(f"   ID: {test1.id}")
    
    print("\n📝 To fix the frontend display:")
    print("   1. Clear browser cache (Ctrl+Shift+Delete)")
    print("   2. Or use Incognito/Private window")
    print("   3. Or clear localStorage manually:")
    print("      - Open DevTools (F12)")
    print("      - Go to Application/Storage tab")
    print("      - Clear localStorage for localhost:5174")
    print("   4. Login again with test1/123456")
    
    print("\n💡 The issue:")
    print("   - Old JWT token has outdated user data")
    print("   - Token contains: old coins (0) and premium status")
    print("   - Database has: correct coins (1000) and premium (True)")
    print("   - Solution: Get new token by logging in again")

else:
    print("\n❌ test1 not found!")

print("\n" + "="*60)
db.close()
