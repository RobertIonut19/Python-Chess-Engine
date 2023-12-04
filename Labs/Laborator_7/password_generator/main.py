from password_generator import generator

def main():
    print("Welcome to the Password Generator!")
    print("Please select the options for your password.")
    length = int(input("How long would you like your password to be? "))
    include_special = input("Would you like to include special characters? (y/n) ")
    include_numbers = input("Would you like to include numbers? (y/n) ")
    include_uppercase = input("Would you like to include uppercase letters? (y/n) ")
    password = generator.generate_password(length, include_special, include_numbers, include_uppercase)
    print("Your password is: " + password)

main()

