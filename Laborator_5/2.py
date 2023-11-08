class Account:
    def __init__(self, account_number, holder_name, balance=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"Your new balance after withdrawal is {self.balance}"
        else:
            return "Invalid amount"

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Your new balance after deposit is {self.balance}"
        else:
            return "Invalid amount"


    def get_balance(self):
        return f"Your current balance is {self.balance}"

    def calculate_interest(self, rate):
        pass

class SavingsAccount(Account):
    def calculate_interest(self, rate):
        interest = (self.balance * rate) / 100
        self.balance += interest
        return f"Your new balance after interest is {self.balance}"

class CheckingAccount(Account):
    def deduct_fees(self, fee):
        if fee > 0 and fee <= self.balance:
            self.balance -= fee
            return f"Your new balance after fees is {self.balance}"
        else:
            return "Invalid amount"

    def calculate_interest(self, rate):
        return rate

def account_exercise():
    account = Account(100)
    account.withdraw(10)
    account.deposit(20)
    print(account.get_balance())
    account.interest(0.1)
    print(account.get_balance())

    savings_account = SavingsAccount(100)
    savings_account.withdraw(10)
    savings_account.deposit(20)
    print(savings_account.get_balance())
    savings_account.interest(0.1)
    print(savings_account.get_balance())

    checking_account = CheckingAccount(100)
    checking_account.withdraw(10)
    checking_account.deposit(20)
    print(checking_account.get_balance())


account_exercise()