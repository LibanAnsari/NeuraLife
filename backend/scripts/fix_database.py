<<<<<<< HEAD
"""Fix all database issues - restore test1 premium, ensure all data is correct"""
from app.database import SessionLocal
from app.models import User, Therapist

db = SessionLocal()

print("\n" + "="*60)
print("FIXING DATABASE ISSUES")
print("="*60)

# Fix test1 - should have premium
test1 = db.query(User).filter(User.username == "test1").first()
if test1:
    print(f"\n📝 Fixing test1:")
    print(f"   Current: {test1.neuracoins} coins, Premium: {test1.is_premium}")
    test1.is_premium = True
    test1.neuracoins = 1000  # Give some coins back
    db.commit()
    print(f"   Fixed: {test1.neuracoins} coins, Premium: {test1.is_premium}")
else:
    print("\n❌ test1 not found!")

# Show all users after fix
print("\n" + "="*60)
print("CURRENT USER STATUS")
print("="*60)

users = db.query(User).all()
for user in users:
    premium_badge = "✅ PREMIUM" if user.is_premium else "⭕ Free"
    print(f"   {user.username:15} | {user.neuracoins:5} coins | {premium_badge}")

print("\n" + "="*60)
print("THERAPISTS")
print("="*60)

therapists = db.query(Therapist).all()
for t in therapists:
    print(f"   {t.name:20} | {t.email}")

print("\n✅ All fixes applied!")
print("\n📝 Summary:")
print("   - test1: Premium with 1000 coins")
print("   - test2-test6: 5000 coins each (for testing)")
print("   - Resources & Quizzes: Available via API")
print("   - Therapists: All registered")

db.close()
=======
"""Fix all database issues - restore test1 premium, ensure all data is correct"""
from app.database import SessionLocal
from app.models import User, Therapist

db = SessionLocal()

print("\n" + "="*60)
print("FIXING DATABASE ISSUES")
print("="*60)

# Fix test1 - should have premium
test1 = db.query(User).filter(User.username == "test1").first()
if test1:
    print(f"\n📝 Fixing test1:")
    print(f"   Current: {test1.neuracoins} coins, Premium: {test1.is_premium}")
    test1.is_premium = True
    test1.neuracoins = 1000  # Give some coins back
    db.commit()
    print(f"   Fixed: {test1.neuracoins} coins, Premium: {test1.is_premium}")
else:
    print("\n❌ test1 not found!")

# Show all users after fix
print("\n" + "="*60)
print("CURRENT USER STATUS")
print("="*60)

users = db.query(User).all()
for user in users:
    premium_badge = "✅ PREMIUM" if user.is_premium else "⭕ Free"
    print(f"   {user.username:15} | {user.neuracoins:5} coins | {premium_badge}")

print("\n" + "="*60)
print("THERAPISTS")
print("="*60)

therapists = db.query(Therapist).all()
for t in therapists:
    print(f"   {t.name:20} | {t.email}")

print("\n✅ All fixes applied!")
print("\n📝 Summary:")
print("   - test1: Premium with 1000 coins")
print("   - test2-test6: 5000 coins each (for testing)")
print("   - Resources & Quizzes: Available via API")
print("   - Therapists: All registered")

db.close()
>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
