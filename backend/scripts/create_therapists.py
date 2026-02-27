<<<<<<< HEAD
"""
Create dummy therapist accounts and assign them to test users
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import Therapist, User, UserTherapist
from app.auth import get_password_hash

def create_therapists():
    """Create dummy therapist accounts"""
    db = SessionLocal()
    
    try:
        therapists_data = [
            # Original named therapists
            {
                'name': 'Ritvik',
                'email': 'ritvik@therapy.com',
                'password': '123456',
                'specialization': 'Cognitive Behavioral Therapy',
                'credentials': 'PhD, Licensed Psychologist',
                'experience': 8,
                'rating': 5,
                'cost': 500,
                'bio': 'Specializing in CBT and anxiety treatment.',
                'avatar': '�‍⚕️'
            },
            {
                'name': 'Liban',
                'email': 'liban@therapy.com',
                'password': '123456',
                'specialization': 'PTSD & Trauma Specialist',
                'credentials': 'PsyD, EMDR Certified',
                'experience': 6,
                'rating': 5,
                'cost': 550,
                'bio': 'Expert in trauma recovery and PTSD treatment.',
                'avatar': '👨‍⚕️'
            },
            {
                'name': 'Yash',
                'email': 'yash@therapy.com',
                'password': '123456',
                'specialization': 'Depression & Mood Disorders',
                'credentials': 'MD, Psychiatrist',
                'experience': 10,
                'rating': 5,
                'cost': 600,
                'bio': 'Specialized in mood disorders and medication management.',
                'avatar': '👨‍⚕️'
            },
            {
                'name': 'Abhisaar',
                'email': 'abhisaar@therapy.com',
                'password': '123456',
                'specialization': 'Family & Relationship Therapy',
                'credentials': 'LMFT, MA',
                'experience': 7,
                'rating': 5,
                'cost': 450,
                'bio': 'Helping families build stronger relationships.',
                'avatar': '👨‍⚕️'
            },
            # Test therapist accounts t1-t6
            {
                'name': 'Therapist 1',
                'email': 't1@therapy.com',
                'password': '123456',
                'specialization': 'General Therapy',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'General mental health counseling.',
                'avatar': '�‍⚕️'
            },
            {
                'name': 'Therapist 2',
                'email': 't2@therapy.com',
                'password': '123456',
                'specialization': 'Anxiety Specialist',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Anxiety and stress management.',
                'avatar': '👩‍⚕️'
            },
            {
                'name': 'Therapist 3',
                'email': 't3@therapy.com',
                'password': '123456',
                'specialization': 'Child Therapy',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Specialized in child and adolescent therapy.',
                'avatar': '👨‍⚕️'
            },
            {
                'name': 'Therapist 4',
                'email': 't4@therapy.com',
                'password': '123456',
                'specialization': 'Couples Therapy',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Relationship and couples counseling.',
                'avatar': '👩‍⚕️'
            },
            {
                'name': 'Therapist 5',
                'email': 't5@therapy.com',
                'password': '123456',
                'specialization': 'Addiction Counseling',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Addiction recovery and support.',
                'avatar': '👨‍⚕️'
            },
            {
                'name': 'Therapist 6',
                'email': 't6@therapy.com',
                'password': '123456',
                'specialization': 'Grief Counseling',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Grief and loss support.',
                'avatar': '�‍⚕️'
            }
        ]
        
        print("=" * 60)
        print("CREATING THERAPIST ACCOUNTS")
        print("=" * 60)
        print()
        
        created_therapists = []
        
        for therapist_data in therapists_data:
            # Check if therapist already exists
            existing = db.query(Therapist).filter(Therapist.email == therapist_data['email']).first()
            
            if existing:
                print(f"📝 Updating {therapist_data['name']}...")
                existing.name = therapist_data['name']
                existing.specialization = therapist_data['specialization']
                existing.credentials = therapist_data['credentials']
                existing.experience = therapist_data['experience']
                existing.rating = therapist_data['rating']
                existing.cost = therapist_data['cost']
                existing.bio = therapist_data['bio']
                existing.avatar = therapist_data['avatar']
                existing.hashed_password = get_password_hash(therapist_data['password'])
                created_therapists.append(existing)
                print(f"   ✅ Updated: {therapist_data['specialization']}")
            else:
                print(f"👨‍⚕️ Creating {therapist_data['name']}...")
                new_therapist = Therapist(
                    name=therapist_data['name'],
                    email=therapist_data['email'],
                    hashed_password=get_password_hash(therapist_data['password']),
                    specialization=therapist_data['specialization'],
                    credentials=therapist_data['credentials'],
                    experience=therapist_data['experience'],
                    rating=therapist_data['rating'],
                    cost=therapist_data['cost'],
                    bio=therapist_data['bio'],
                    avatar=therapist_data['avatar']
                )
                db.add(new_therapist)
                db.commit()
                db.refresh(new_therapist)
                created_therapists.append(new_therapist)
                print(f"   ✅ Created: {therapist_data['specialization']}")
        
        db.commit()
        
        # Assign therapists to test users
        print()
        print("=" * 60)
        print("ASSIGNING THERAPISTS TO TEST USERS")
        print("=" * 60)
        print()
        
        # Get test1 user (the one with 1000 coins)
        test1 = db.query(User).filter(User.username == 'test1').first()
        
        if test1 and created_therapists:
            # Assign first therapist to test1
            existing_assignment = db.query(UserTherapist).filter(
                UserTherapist.user_id == test1.id,
                UserTherapist.therapist_id == created_therapists[0].id
            ).first()
            
            if not existing_assignment:
                assignment = UserTherapist(
                    user_id=test1.id,
                    therapist_id=created_therapists[0].id
                )
                db.add(assignment)
                db.commit()
                print(f"✅ Assigned {created_therapists[0].name} to test1")
            else:
                print(f"📝 test1 already has {created_therapists[0].name} assigned")
        
        print()
        print("=" * 60)
        print("✅ ALL THERAPISTS CREATED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Therapist Login Credentials:")
        print("-" * 60)
        print("Named Therapists:")
        print("  ritvik@therapy.com       | Password: 123456")
        print("  liban@therapy.com        | Password: 123456")
        print("  yash@therapy.com         | Password: 123456")
        print("  abhisaar@therapy.com     | Password: 123456")
        print()
        print("Test Therapists:")
        print("  t1@therapy.com - t6@therapy.com | Password: 123456")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_therapists()
=======
"""
Create dummy therapist accounts and assign them to test users
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models import Therapist, User, UserTherapist
from app.auth import get_password_hash

def create_therapists():
    """Create dummy therapist accounts"""
    db = SessionLocal()
    
    try:
        therapists_data = [
            # Original named therapists
            {
                'name': 'Ritvik',
                'email': 'ritvik@therapy.com',
                'password': '123456',
                'specialization': 'Cognitive Behavioral Therapy',
                'credentials': 'PhD, Licensed Psychologist',
                'experience': 8,
                'rating': 5,
                'cost': 500,
                'bio': 'Specializing in CBT and anxiety treatment.',
                'avatar': '�‍⚕️'
            },
            {
                'name': 'Liban',
                'email': 'liban@therapy.com',
                'password': '123456',
                'specialization': 'PTSD & Trauma Specialist',
                'credentials': 'PsyD, EMDR Certified',
                'experience': 6,
                'rating': 5,
                'cost': 550,
                'bio': 'Expert in trauma recovery and PTSD treatment.',
                'avatar': '👨‍⚕️'
            },
            {
                'name': 'Yash',
                'email': 'yash@therapy.com',
                'password': '123456',
                'specialization': 'Depression & Mood Disorders',
                'credentials': 'MD, Psychiatrist',
                'experience': 10,
                'rating': 5,
                'cost': 600,
                'bio': 'Specialized in mood disorders and medication management.',
                'avatar': '👨‍⚕️'
            },
            {
                'name': 'Abhisaar',
                'email': 'abhisaar@therapy.com',
                'password': '123456',
                'specialization': 'Family & Relationship Therapy',
                'credentials': 'LMFT, MA',
                'experience': 7,
                'rating': 5,
                'cost': 450,
                'bio': 'Helping families build stronger relationships.',
                'avatar': '👨‍⚕️'
            },
            # Test therapist accounts t1-t6
            {
                'name': 'Therapist 1',
                'email': 't1@therapy.com',
                'password': '123456',
                'specialization': 'General Therapy',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'General mental health counseling.',
                'avatar': '�‍⚕️'
            },
            {
                'name': 'Therapist 2',
                'email': 't2@therapy.com',
                'password': '123456',
                'specialization': 'Anxiety Specialist',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Anxiety and stress management.',
                'avatar': '👩‍⚕️'
            },
            {
                'name': 'Therapist 3',
                'email': 't3@therapy.com',
                'password': '123456',
                'specialization': 'Child Therapy',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Specialized in child and adolescent therapy.',
                'avatar': '👨‍⚕️'
            },
            {
                'name': 'Therapist 4',
                'email': 't4@therapy.com',
                'password': '123456',
                'specialization': 'Couples Therapy',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Relationship and couples counseling.',
                'avatar': '👩‍⚕️'
            },
            {
                'name': 'Therapist 5',
                'email': 't5@therapy.com',
                'password': '123456',
                'specialization': 'Addiction Counseling',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Addiction recovery and support.',
                'avatar': '👨‍⚕️'
            },
            {
                'name': 'Therapist 6',
                'email': 't6@therapy.com',
                'password': '123456',
                'specialization': 'Grief Counseling',
                'credentials': 'Licensed Therapist',
                'experience': 5,
                'rating': 5,
                'cost': 400,
                'bio': 'Grief and loss support.',
                'avatar': '�‍⚕️'
            }
        ]
        
        print("=" * 60)
        print("CREATING THERAPIST ACCOUNTS")
        print("=" * 60)
        print()
        
        created_therapists = []
        
        for therapist_data in therapists_data:
            # Check if therapist already exists
            existing = db.query(Therapist).filter(Therapist.email == therapist_data['email']).first()
            
            if existing:
                print(f"📝 Updating {therapist_data['name']}...")
                existing.name = therapist_data['name']
                existing.specialization = therapist_data['specialization']
                existing.credentials = therapist_data['credentials']
                existing.experience = therapist_data['experience']
                existing.rating = therapist_data['rating']
                existing.cost = therapist_data['cost']
                existing.bio = therapist_data['bio']
                existing.avatar = therapist_data['avatar']
                existing.hashed_password = get_password_hash(therapist_data['password'])
                created_therapists.append(existing)
                print(f"   ✅ Updated: {therapist_data['specialization']}")
            else:
                print(f"👨‍⚕️ Creating {therapist_data['name']}...")
                new_therapist = Therapist(
                    name=therapist_data['name'],
                    email=therapist_data['email'],
                    hashed_password=get_password_hash(therapist_data['password']),
                    specialization=therapist_data['specialization'],
                    credentials=therapist_data['credentials'],
                    experience=therapist_data['experience'],
                    rating=therapist_data['rating'],
                    cost=therapist_data['cost'],
                    bio=therapist_data['bio'],
                    avatar=therapist_data['avatar']
                )
                db.add(new_therapist)
                db.commit()
                db.refresh(new_therapist)
                created_therapists.append(new_therapist)
                print(f"   ✅ Created: {therapist_data['specialization']}")
        
        db.commit()
        
        # Assign therapists to test users
        print()
        print("=" * 60)
        print("ASSIGNING THERAPISTS TO TEST USERS")
        print("=" * 60)
        print()
        
        # Get test1 user (the one with 1000 coins)
        test1 = db.query(User).filter(User.username == 'test1').first()
        
        if test1 and created_therapists:
            # Assign first therapist to test1
            existing_assignment = db.query(UserTherapist).filter(
                UserTherapist.user_id == test1.id,
                UserTherapist.therapist_id == created_therapists[0].id
            ).first()
            
            if not existing_assignment:
                assignment = UserTherapist(
                    user_id=test1.id,
                    therapist_id=created_therapists[0].id
                )
                db.add(assignment)
                db.commit()
                print(f"✅ Assigned {created_therapists[0].name} to test1")
            else:
                print(f"📝 test1 already has {created_therapists[0].name} assigned")
        
        print()
        print("=" * 60)
        print("✅ ALL THERAPISTS CREATED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Therapist Login Credentials:")
        print("-" * 60)
        print("Named Therapists:")
        print("  ritvik@therapy.com       | Password: 123456")
        print("  liban@therapy.com        | Password: 123456")
        print("  yash@therapy.com         | Password: 123456")
        print("  abhisaar@therapy.com     | Password: 123456")
        print()
        print("Test Therapists:")
        print("  t1@therapy.com - t6@therapy.com | Password: 123456")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_therapists()
>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
