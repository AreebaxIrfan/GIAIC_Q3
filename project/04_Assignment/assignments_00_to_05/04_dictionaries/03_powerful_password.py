from hashlib import sha256

# Constants for reused emails
EXAMPLE_EMAIL = "example@gmail.com"
CODE_EMAIL = "code_in_cde@gmail.com"
STUDENT_EMAIL = "student-of-the-year@gmail.com"

def login(email, stored_logins, password_to_check):
    if stored_logins[email] == hash_password(password_to_check):
        return True
    return False

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def main():
    stored_logins = {
        EXAMPLE_EMAIL: "53nisfnishfishhr399922494jn483y34r",
        CODE_EMAIL: "8ur9cufh3433bwhSHjuhh",
        STUDENT_EMAIL: "hduhS8SHush999Y38HSJD38"
    }

    print(login(EXAMPLE_EMAIL, stored_logins, "word"))
    print(login(EXAMPLE_EMAIL, stored_logins, "password"))

    print(login(CODE_EMAIL, stored_logins, "karel"))
    print(login(CODE_EMAIL, stored_logins, "karel"))

    print(login(STUDENT_EMAIL, stored_logins, "password"))
    print(login(STUDENT_EMAIL, stored_logins, "123!456?789"))

if __name__ == '__main__':
    main()
