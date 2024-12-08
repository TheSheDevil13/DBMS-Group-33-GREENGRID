from werkzeug.security import generate_password_hash

# The password you want to hash
password = "admin123"  # Replace this with whatever password you want

# Generate the hash
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

print(f"\nOriginal password: {password}")
print(f"Hashed password: {hashed_password}")
print("\nYou can use this hashed password in your SQL query to update the admin user's password")
