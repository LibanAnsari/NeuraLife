<<<<<<< HEAD
"""Update test users and set all new registrations to 0 coins"""
from app.database import SessionLocal
from app.models import User

db = SessionLocal()

try:
    # Update all existing users to 0 coins first
    all_users = db.query(User).all()
    print(f"\n{'='*60}")
    print(f"Updating {len(all_users)} users...")
    print(f"{'='*60}\n")
    
    for user in all_users:
        old_coins = user.neuracoins
        
        # Give test2-test6 5000 coins, everyone else gets 0
        if user.username in ['test2', 'test3', 'test4', 'test5', 'test6']:
            user.neuracoins = 5000
            print(f"✅ {user.username}: {old_coins} → 5000 NeuraCoins (Test User)")
        else:
            user.neuracoins = 0
            print(f"📊 {user.username}: {old_coins} → 0 NeuraCoins (Regular User)")
    
    db.commit()
    
    print(f"\n{'='*60}")
    print("✅ Successfully updated all users!")
    print(f"{'='*60}\n")
    
    # Show summary
    test_users = db.query(User).filter(User.username.in_(['test2', 'test3', 'test4', 'test5', 'test6'])).all()
    regular_users = db.query(User).filter(~User.username.in_(['test2', 'test3', 'test4', 'test5', 'test6'])).all()
    
    print("Summary:")
    print(f"  Test Users (5000 coins): {len(test_users)}")
    print(f"  Regular Users (0 coins): {len(regular_users)}")
    print(f"  Total Users: {len(all_users)}\n")
    
    print("Test Users:")
    for user in test_users:
        print(f"  - {user.username}: {user.neuracoins} coins")
    
    if regular_users:
        print("\nRegular Users:")
        for user in regular_users[:5]:  # Show first 5
            print(f"  - {user.username}: {user.neuracoins} coins")
        if len(regular_users) > 5:
            print(f"  ... and {len(regular_users) - 5} more")

except Exception as e:
    print(f"\n❌ Error: {e}")
    db.rollback()
finally:
    db.close()
=======
"""Update test users and set all new registrations to 0 coins"""
from app.database import SessionLocal
from app.models import User

db = SessionLocal()

try:
    # Update all existing users to 0 coins first
    all_users = db.query(User).all()
    print(f"\n{'='*60}")
    print(f"Updating {len(all_users)} users...")
    print(f"{'='*60}\n")
    
    for user in all_users:
        old_coins = user.neuracoins
        
        # Give test2-test6 5000 coins, everyone else gets 0
        if user.username in ['test2', 'test3', 'test4', 'test5', 'test6']:
            user.neuracoins = 5000
            print(f"✅ {user.username}: {old_coins} → 5000 NeuraCoins (Test User)")
        else:
            user.neuracoins = 0
            print(f"📊 {user.username}: {old_coins} → 0 NeuraCoins (Regular User)")
    
    db.commit()
    
    print(f"\n{'='*60}")
    print("✅ Successfully updated all users!")
    print(f"{'='*60}\n")
    
    # Show summary
    test_users = db.query(User).filter(User.username.in_(['test2', 'test3', 'test4', 'test5', 'test6'])).all()
    regular_users = db.query(User).filter(~User.username.in_(['test2', 'test3', 'test4', 'test5', 'test6'])).all()
    
    print("Summary:")
    print(f"  Test Users (5000 coins): {len(test_users)}")
    print(f"  Regular Users (0 coins): {len(regular_users)}")
    print(f"  Total Users: {len(all_users)}\n")
    
    print("Test Users:")
    for user in test_users:
        print(f"  - {user.username}: {user.neuracoins} coins")
    
    if regular_users:
        print("\nRegular Users:")
        for user in regular_users[:5]:  # Show first 5
            print(f"  - {user.username}: {user.neuracoins} coins")
        if len(regular_users) > 5:
            print(f"  ... and {len(regular_users) - 5} more")

except Exception as e:
    print(f"\n❌ Error: {e}")
    db.rollback()
finally:
    db.close()
>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
