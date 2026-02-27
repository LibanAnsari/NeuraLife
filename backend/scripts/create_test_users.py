"""
Create test user accounts with NeuraCoins
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import User
from app.auth import get_password_hash

def create_test_users():
    """Create test user accounts"""
    db = SessionLocal()
    
    try:
        # Test users configuration
        test_users = [
            {
                'username': 'test1',
                'email': 'test1@test.com',
                'password': '123456',
                'neuracoins': 1000,
                'is_premium': True
            },
            {
                'username': 'test2',
                'email': 'test2@test.com',
                'password': '123456',
                'neuracoins': 5000,
                'is_premium': True
            },
            {
                'username': 'test3',
                'email': 'test3@test.com',
                'password': '123456',
                'neuracoins': 5000,
                'is_premium': True
            },
            {
                'username': 'test4',
                'email': 'test4@test.com',
                'password': '123456',
                'neuracoins': 5000,
                'is_premium': True
            },
            {
                'username': 'test5',
                'email': 'test5@test.com',
                'password': '123456',
                'neuracoins': 5000,
                'is_premium': True
            },
            {
                'username': 'test6',
                'email': 'test6@test.com',
                'password': '123456',
                'neuracoins': 5000,
                'is_premium': True
            }
        ]
        
        print("=" * 60)
        print("CREATING TEST USERS")
        print("=" * 60)
        print()
        
        for user_data in test_users:
            # Check if user already exists
            existing_user = db.query(User).filter(User.username == user_data['username']).first()
            
            if existing_user:
                # Update existing user
                print(f"📝 Updating {user_data['username']}...")
                existing_user.neuracoins = user_data['neuracoins']
                existing_user.is_premium = user_data['is_premium']
                existing_user.hashed_password = get_password_hash(user_data['password'])
                print(f"   ✅ Updated: {user_data['neuracoins']} coins, Premium: {user_data['is_premium']}")
            else:
                # Create new user
                print(f"👤 Creating {user_data['username']}...")
                new_user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    hashed_password=get_password_hash(user_data['password']),
                    neuracoins=user_data['neuracoins'],
                    is_premium=user_data['is_premium']
                )
                db.add(new_user)
                print(f"   ✅ Created: {user_data['neuracoins']} coins, Premium: {user_data['is_premium']}")
        
        db.commit()
        
        print()
        print("=" * 60)
        print("✅ ALL TEST USERS CREATED/UPDATED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Login Credentials:")
        print("-" * 60)
        for user_data in test_users:
            print(f"Username: {user_data['username']:<10} | Password: 123456 | Coins: {user_data['neuracoins']} | Premium: {'Yes' if user_data['is_premium'] else 'No'}")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()
