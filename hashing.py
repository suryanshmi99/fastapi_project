from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password ko hash karna (store karte waqt)
hashed_password = pwd_context.hash("mera_password123")
print(hashed_password)
# Result: kuch aisa "$2b$12$KIXQ...random_gibberish..."

# Verify karna (login karte waqt)
is_correct = pwd_context.verify("mera_password123", hashed_password)
print(is_correct)
# Result: True ya False