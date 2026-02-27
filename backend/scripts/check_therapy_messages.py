<<<<<<< HEAD
"""Check therapy messages and user-therapist relationships for test1"""
from app.database import SessionLocal
from app.models import User, Therapist, TherapyMessage, UserTherapist

db = SessionLocal()

print("\n" + "="*60)
print("THERAPY MESSAGING DEBUG")
print("="*60)

# Get test1
test1 = db.query(User).filter(User.username == "test1").first()
if not test1:
    print("\n❌ test1 not found!")
    db.close()
    exit()

print(f"\n✅ test1 found: ID = {test1.id}, Premium = {test1.is_premium}")

# Get Yash and Ritvik
yash = db.query(Therapist).filter(Therapist.name == "Yash").first()
ritvik = db.query(Therapist).filter(Therapist.name == "Ritvik").first()

print(f"\n👨‍⚕️ Therapists:")
if yash:
    print(f"   - Yash: ID = {yash.id}, Email = {yash.email}")
if ritvik:
    print(f"   - Ritvik: ID = {ritvik.id}, Email = {ritvik.email}")

# Check messages from test1
messages = db.query(TherapyMessage).filter(TherapyMessage.user_id == test1.id).all()
print(f"\n💬 Messages from test1: {len(messages)} total")
for msg in messages:
    therapist = db.query(Therapist).filter(Therapist.id == msg.therapist_id).first()
    print(f"   - To {therapist.name if therapist else 'Unknown'}: {msg.message[:50]}... (Sender: {msg.sender})")

# Check user-therapist relationships
relationships = db.query(UserTherapist).filter(UserTherapist.user_id == test1.id).all()
print(f"\n🤝 User-Therapist Relationships: {len(relationships)} total")
for rel in relationships:
    therapist = db.query(Therapist).filter(Therapist.id == rel.therapist_id).first()
    print(f"   - Opted in for: {therapist.name if therapist else 'Unknown'} (ID: {rel.therapist_id})")

# Check what Ritvik sees
if ritvik:
    print(f"\n📋 Ritvik's Patient List:")
    ritvik_relationships = db.query(UserTherapist).filter(UserTherapist.therapist_id == ritvik.id).all()
    print(f"   Total patients: {len(ritvik_relationships)}")
    for rel in ritvik_relationships:
        user = db.query(User).filter(User.id == rel.user_id).first()
        print(f"   - {user.username if user else 'Unknown'} (ID: {rel.user_id})")
    
    # Messages with Ritvik
    ritvik_messages = db.query(TherapyMessage).filter(
        TherapyMessage.user_id == test1.id,
        TherapyMessage.therapist_id == ritvik.id
    ).all()
    print(f"\n   Messages with test1: {len(ritvik_messages)}")
    for msg in ritvik_messages:
        print(f"   - [{msg.sender}] {msg.message[:50]}...")

# Check what Yash sees
if yash:
    print(f"\n📋 Yash's Patient List:")
    yash_relationships = db.query(UserTherapist).filter(UserTherapist.therapist_id == yash.id).all()
    print(f"   Total patients: {len(yash_relationships)}")
    for rel in yash_relationships:
        user = db.query(User).filter(User.id == rel.user_id).first()
        print(f"   - {user.username if user else 'Unknown'} (ID: {rel.user_id})")
    
    # Messages with Yash
    yash_messages = db.query(TherapyMessage).filter(
        TherapyMessage.user_id == test1.id,
        TherapyMessage.therapist_id == yash.id
    ).all()
    print(f"\n   Messages with test1: {len(yash_messages)}")
    for msg in yash_messages:
        print(f"   - [{msg.sender}] {msg.message[:50]}...")

print("\n" + "="*60)
print("💡 SOLUTION:")
print("   If relationships are missing, restart the backend and")
print("   send a new message from test1 to create the relationship")
print("="*60)

db.close()
=======
"""Check therapy messages and user-therapist relationships for test1"""
from app.database import SessionLocal
from app.models import User, Therapist, TherapyMessage, UserTherapist

db = SessionLocal()

print("\n" + "="*60)
print("THERAPY MESSAGING DEBUG")
print("="*60)

# Get test1
test1 = db.query(User).filter(User.username == "test1").first()
if not test1:
    print("\n❌ test1 not found!")
    db.close()
    exit()

print(f"\n✅ test1 found: ID = {test1.id}, Premium = {test1.is_premium}")

# Get Yash and Ritvik
yash = db.query(Therapist).filter(Therapist.name == "Yash").first()
ritvik = db.query(Therapist).filter(Therapist.name == "Ritvik").first()

print(f"\n👨‍⚕️ Therapists:")
if yash:
    print(f"   - Yash: ID = {yash.id}, Email = {yash.email}")
if ritvik:
    print(f"   - Ritvik: ID = {ritvik.id}, Email = {ritvik.email}")

# Check messages from test1
messages = db.query(TherapyMessage).filter(TherapyMessage.user_id == test1.id).all()
print(f"\n💬 Messages from test1: {len(messages)} total")
for msg in messages:
    therapist = db.query(Therapist).filter(Therapist.id == msg.therapist_id).first()
    print(f"   - To {therapist.name if therapist else 'Unknown'}: {msg.message[:50]}... (Sender: {msg.sender})")

# Check user-therapist relationships
relationships = db.query(UserTherapist).filter(UserTherapist.user_id == test1.id).all()
print(f"\n🤝 User-Therapist Relationships: {len(relationships)} total")
for rel in relationships:
    therapist = db.query(Therapist).filter(Therapist.id == rel.therapist_id).first()
    print(f"   - Opted in for: {therapist.name if therapist else 'Unknown'} (ID: {rel.therapist_id})")

# Check what Ritvik sees
if ritvik:
    print(f"\n📋 Ritvik's Patient List:")
    ritvik_relationships = db.query(UserTherapist).filter(UserTherapist.therapist_id == ritvik.id).all()
    print(f"   Total patients: {len(ritvik_relationships)}")
    for rel in ritvik_relationships:
        user = db.query(User).filter(User.id == rel.user_id).first()
        print(f"   - {user.username if user else 'Unknown'} (ID: {rel.user_id})")
    
    # Messages with Ritvik
    ritvik_messages = db.query(TherapyMessage).filter(
        TherapyMessage.user_id == test1.id,
        TherapyMessage.therapist_id == ritvik.id
    ).all()
    print(f"\n   Messages with test1: {len(ritvik_messages)}")
    for msg in ritvik_messages:
        print(f"   - [{msg.sender}] {msg.message[:50]}...")

# Check what Yash sees
if yash:
    print(f"\n📋 Yash's Patient List:")
    yash_relationships = db.query(UserTherapist).filter(UserTherapist.therapist_id == yash.id).all()
    print(f"   Total patients: {len(yash_relationships)}")
    for rel in yash_relationships:
        user = db.query(User).filter(User.id == rel.user_id).first()
        print(f"   - {user.username if user else 'Unknown'} (ID: {rel.user_id})")
    
    # Messages with Yash
    yash_messages = db.query(TherapyMessage).filter(
        TherapyMessage.user_id == test1.id,
        TherapyMessage.therapist_id == yash.id
    ).all()
    print(f"\n   Messages with test1: {len(yash_messages)}")
    for msg in yash_messages:
        print(f"   - [{msg.sender}] {msg.message[:50]}...")

print("\n" + "="*60)
print("💡 SOLUTION:")
print("   If relationships are missing, restart the backend and")
print("   send a new message from test1 to create the relationship")
print("="*60)

db.close()
>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
