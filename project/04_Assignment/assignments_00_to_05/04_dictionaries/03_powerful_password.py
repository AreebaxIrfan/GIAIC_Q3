# You want to be safe online and use different passwords for different websites. However, you are forgetful at times and want to make a program that can match which password belongs to which website without storing the actual password!

from hashlib import sha256

def login(email , stored_logins, password_to_check):

    if stored_logins[email] == hash_password(password_to_check):
        return True
    
    return False

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def main():
    stored_logins = {
        "example@gmail.com": "53nisfnishfishhr399922494jn483y34r",
        "code_in_cde@gmail.com":
        "8ur9cufh3433bwhSHjuhh",
        "student-of-the-year@gmail.com":
        "hduhS8SHush999Y38HSJD38"
    }
    
    print(login("example@gmail.com", stored_logins, "word"))
    print(login("example@gmail.com", stored_logins, "password"))

    print(login("code_in_cde@gmail.com", stored_logins, "karel"))
    print(login("code_in_cde@gmail.com", stored_logins, "karel"))

    print(login("student-of-the-year@gmail.com", stored_logins, "password"))
    print(login("student-of-the-year@gmail.com", stored_logins, "123!456?789"))

if __name__ == '__main__':
    main()