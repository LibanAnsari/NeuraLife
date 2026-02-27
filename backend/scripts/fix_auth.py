<<<<<<< HEAD
"""
Script to fix all authentication issues in main.py
Replaces manual token verification with Depends(get_current_user)
"""
import re

# Read the file
with open('c:/Users/savit/Hackathon/NIT/NeuraLife+/NeuraLife+/backend/app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the old authentication style
old_pattern = r'''    payload = verify_token\(credentials\.credentials\)
    current_user = db\.query\(User\)\.filter\(User\.id == payload\.get\("user_id"\)\)\.first\(\)'''

# Replace with empty string (we'll update function signatures separately)
content = re.sub(old_pattern, '', content)

# Now fix function signatures - replace credentials with current_user parameter
# Pattern: credentials: HTTPAuthorizationCredentials = Depends(security),
content = re.sub(
    r'credentials: HTTPAuthorizationCredentials = Depends\(security\),\s*\n\s*db: Session = Depends\(get_db\)',
    r'current_user: User = Depends(get_current_user),\n    db: Session = Depends(get_db)',
    content
)

# Write back
with open('c:/Users/savit/Hackathon/NIT/NeuraLife+/NeuraLife+/backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all authentication patterns!")
print("✅ Replaced 'credentials' parameter with 'current_user: User = Depends(get_current_user)'")
print("✅ Removed all 'payload = verify_token' and 'db.query(User).filter...' lines")
=======
"""
Script to fix all authentication issues in main.py
Replaces manual token verification with Depends(get_current_user)
"""
import re

# Read the file
with open('c:/Users/savit/Hackathon/NIT/NeuraLife+/NeuraLife+/backend/app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the old authentication style
old_pattern = r'''    payload = verify_token\(credentials\.credentials\)
    current_user = db\.query\(User\)\.filter\(User\.id == payload\.get\("user_id"\)\)\.first\(\)'''

# Replace with empty string (we'll update function signatures separately)
content = re.sub(old_pattern, '', content)

# Now fix function signatures - replace credentials with current_user parameter
# Pattern: credentials: HTTPAuthorizationCredentials = Depends(security),
content = re.sub(
    r'credentials: HTTPAuthorizationCredentials = Depends\(security\),\s*\n\s*db: Session = Depends\(get_db\)',
    r'current_user: User = Depends(get_current_user),\n    db: Session = Depends(get_db)',
    content
)

# Write back
with open('c:/Users/savit/Hackathon/NIT/NeuraLife+/NeuraLife+/backend/app/main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all authentication patterns!")
print("✅ Replaced 'credentials' parameter with 'current_user: User = Depends(get_current_user)'")
print("✅ Removed all 'payload = verify_token' and 'db.query(User).filter...' lines")
>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
