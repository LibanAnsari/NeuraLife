<<<<<<< HEAD
"""Check database status and restore if needed"""
from app.database import SessionLocal, engine
from app.models import Base, User, Therapist, TherapySession, QuizResult
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

print("\n" + "="*60)
print("DATABASE STATUS CHECK")
print("="*60)

# Count existing records
user_count = db.query(User).count()
therapist_count = db.query(Therapist).count()
session_count = db.query(TherapySession).count()
quiz_count = db.query(QuizResult).count()

print(f"\n📊 Current Database Status:")
print(f"   Users: {user_count}")
print(f"   Therapists: {therapist_count}")
print(f"   Therapy Sessions: {session_count}")
print(f"   Quiz Results: {quiz_count}")

# Check specific users
print(f"\n👥 User Details:")
users = db.query(User).all()
if users:
    for user in users:
        print(f"   - {user.username}: {user.neuracoins} coins, Premium: {user.is_premium}")
else:
    print("   ⚠️ NO USERS FOUND!")

print(f"\n👨‍⚕️ Therapist Details:")
therapists = db.query(Therapist).all()
if therapists:
    for t in therapists:
        print(f"   - {t.name} ({t.email})")
else:
    print("   ⚠️ NO THERAPISTS FOUND!")

# If database is empty or missing key data, restore it
if user_count == 0 or therapist_count == 0:
    print("\n" + "="*60)
    print("⚠️  DATABASE NEEDS RESTORATION")
    print("="*60)
    
    response = input("\nDo you want to restore the database? (yes/no): ")
    
    if response.lower() == 'yes':
        print("\n🔄 Restoring database...")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create test users
        test_users = [
            {"username": "test1", "email": "test1@test.com", "password": "123456", "neuracoins": 0, "is_premium": True},
            {"username": "test2", "email": "test2@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
            {"username": "test3", "email": "test3@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
            {"username": "test4", "email": "test4@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
            {"username": "test5", "email": "test5@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
            {"username": "test6", "email": "test6@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
        ]
        
        for user_data in test_users:
            existing = db.query(User).filter(User.username == user_data["username"]).first()
            if not existing:
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=pwd_context.hash(user_data["password"]),
                    neuracoins=user_data["neuracoins"],
                    is_premium=user_data["is_premium"]
                )
                db.add(user)
                print(f"   ✅ Created user: {user_data['username']}")
        
        # Create therapists
        therapists_data = [
            {"name": "Dr. Sarah Johnson", "email": "sarah@neuralife.com", "password": "123456", "specialization": "Depression & Anxiety"},
            {"name": "Dr. Michael Chen", "email": "michael@neuralife.com", "password": "123456", "specialization": "Stress Management"},
            {"name": "Dr. Emily Rodriguez", "email": "emily@neuralife.com", "password": "123456", "specialization": "Relationship Counseling"},
            {"name": "Liban Ansari", "email": "liban@neuralife.com", "password": "123456", "specialization": "General Mental Health"},
        ]
        
        for t_data in therapists_data:
            existing = db.query(Therapist).filter(Therapist.email == t_data["email"]).first()
            if not existing:
                therapist = Therapist(
                    name=t_data["name"],
                    email=t_data["email"],
                    hashed_password=pwd_context.hash(t_data["password"]),
                    specialization=t_data["specialization"]
                )
                db.add(therapist)
                print(f"   ✅ Created therapist: {t_data['name']}")
        
        db.commit()
        
        print("\n✅ Database restored successfully!")
        print("\n📋 Test Credentials:")
        print("   Users: test1-test6 / 123456")
        print("   Therapists: Any therapist email / 123456")
        
    else:
        print("\n❌ Database restoration cancelled")
else:
    print("\n✅ Database looks good!")

print("\n" + "="*60)
db.close()
=======
"""Check database status and restore if needed"""
from app.database import SessionLocal, engine
from app.models import Base, User, Therapist, TherapySession, QuizResult
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

print("\n" + "="*60)
print("DATABASE STATUS CHECK")
print("="*60)

# Count existing records
user_count = db.query(User).count()
therapist_count = db.query(Therapist).count()
session_count = db.query(TherapySession).count()
quiz_count = db.query(QuizResult).count()

print(f"\n📊 Current Database Status:")
print(f"   Users: {user_count}")
print(f"   Therapists: {therapist_count}")
print(f"   Therapy Sessions: {session_count}")
print(f"   Quiz Results: {quiz_count}")

# Check specific users
print(f"\n👥 User Details:")
users = db.query(User).all()
if users:
    for user in users:
        print(f"   - {user.username}: {user.neuracoins} coins, Premium: {user.is_premium}")
else:
    print("   ⚠️ NO USERS FOUND!")

print(f"\n👨‍⚕️ Therapist Details:")
therapists = db.query(Therapist).all()
if therapists:
    for t in therapists:
        print(f"   - {t.name} ({t.email})")
else:
    print("   ⚠️ NO THERAPISTS FOUND!")

# If database is empty or missing key data, restore it
if user_count == 0 or therapist_count == 0:
    print("\n" + "="*60)
    print("⚠️  DATABASE NEEDS RESTORATION")
    print("="*60)
    
    response = input("\nDo you want to restore the database? (yes/no): ")
    
    if response.lower() == 'yes':
        print("\n🔄 Restoring database...")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Create test users
        test_users = [
            {"username": "test1", "email": "test1@test.com", "password": "123456", "neuracoins": 0, "is_premium": True},
            {"username": "test2", "email": "test2@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
            {"username": "test3", "email": "test3@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
            {"username": "test4", "email": "test4@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
            {"username": "test5", "email": "test5@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
            {"username": "test6", "email": "test6@test.com", "password": "123456", "neuracoins": 5000, "is_premium": False},
        ]
        
        for user_data in test_users:
            existing = db.query(User).filter(User.username == user_data["username"]).first()
            if not existing:
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=pwd_context.hash(user_data["password"]),
                    neuracoins=user_data["neuracoins"],
                    is_premium=user_data["is_premium"]
                )
                db.add(user)
                print(f"   ✅ Created user: {user_data['username']}")
        
        # Create therapists
        therapists_data = [
            {"name": "Dr. Sarah Johnson", "email": "sarah@neuralife.com", "password": "123456", "specialization": "Depression & Anxiety"},
            {"name": "Dr. Michael Chen", "email": "michael@neuralife.com", "password": "123456", "specialization": "Stress Management"},
            {"name": "Dr. Emily Rodriguez", "email": "emily@neuralife.com", "password": "123456", "specialization": "Relationship Counseling"},
            {"name": "Liban Ansari", "email": "liban@neuralife.com", "password": "123456", "specialization": "General Mental Health"},
        ]
        
        for t_data in therapists_data:
            existing = db.query(Therapist).filter(Therapist.email == t_data["email"]).first()
            if not existing:
                therapist = Therapist(
                    name=t_data["name"],
                    email=t_data["email"],
                    hashed_password=pwd_context.hash(t_data["password"]),
                    specialization=t_data["specialization"]
                )
                db.add(therapist)
                print(f"   ✅ Created therapist: {t_data['name']}")
        
        db.commit()
        
        print("\n✅ Database restored successfully!")
        print("\n📋 Test Credentials:")
        print("   Users: test1-test6 / 123456")
        print("   Therapists: Any therapist email / 123456")
        
    else:
        print("\n❌ Database restoration cancelled")
else:
    print("\n✅ Database looks good!")

print("\n" + "="*60)
db.close()
>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
