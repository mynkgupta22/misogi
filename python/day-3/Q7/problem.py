# Test Case 1: Creating different types of accounts
savings_account = SavingsAccount("SA001", "Alice Johnson", 1000, 2.5)
checking_account = CheckingAccount("CA001", "Bob Smith", 500, 200)

print(f"Savings Account: {savings_account}")
print(f"Checking Account: {checking_account}")

# Test Case 2: Deposit and Withdrawal operations
print(f"Savings balance before: ${savings_account.get_balance()}")
savings_account.deposit(500)
print(f"After depositing $500: ${savings_account.get_balance()}")

withdrawal_result = savings_account.withdraw(200)
print(f"Withdrawal result: {withdrawal_result}")
print(f"Balance after withdrawal: ${savings_account.get_balance()}")

# Test Case 3: Overdraft protection in checking account
print(f"Checking balance: ${checking_account.get_balance()}")
overdraft_result = checking_account.withdraw(600)  # Should use overdraft
print(f"Overdraft withdrawal: {overdraft_result}")
print(f"Balance after overdraft: ${checking_account.get_balance()}")

# Test Case 4: Interest calculation for savings
interest_earned = savings_account.calculate_monthly_interest()
print(f"Monthly interest earned: ${interest_earned}")

# Test Case 5: Class methods and variables
print(f"Total accounts created: {Account.get_total_accounts()}")
print(f"Bank name: {Account.bank_name}")

# Change bank settings using class method
Account.set_bank_name("New National Bank")
Account.set_minimum_balance(100)

# Test Case 6: Account validation
try:
    invalid_account = SavingsAccount("SA002", "", -100, 1.5)  # Should raise error
except ValueError as e:
    print(f"Validation error: {e}")

# Expected outputs should show proper account creation, transaction handling,
# interest calculation, and class-level operations
class Account:
    total_accounts = 0
    bank_name = "National Bank"
    minimum_balance = 0
    def __init__(self, account_id, account_holder, balance = 0):
        self.account_id = account_id
        self.account_holder = account_holder
        self.balance = balance
    @classmethod
    def get_total_accounts(cls):
        """
            Get the total number of accounts created
            Returns:
                int: Total accounts
         """
        return cls.total_accounts
    @classmethod
    def set_bank_name(cls, name):
        """
            Set the bank name
            Args:
                name (str): New bank name
        """
        cls.bank_name = name
    @classmethod
    def set_minimum_balance(cls, amount):
        """
            Set the minimum balance required for accounts
            Args:
                amount (float): Minimum balance amount
        """
        cls.minimum_balance = amount

    def get_balance(self):
        """
            Get the current balance of the account
            Returns:
                float: Current balance
        """
        return self.balance

    def deposit(self, amount):
        """
            Deposit money into the account
            Args:
                amount (float): Amount to deposit
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount):
        """
            Withdraw money from the account
            Args:
                amount (float): Amount to withdraw
            Returns:
                bool: True if withdrawal successful, False otherwise
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < self.minimum_balance:
            return False
        self.balance -= amount
        return True

class SavingsAccount(Account):
    def __init__(self, account_id, account_holder, balance = 0, interest_rate = 0):
        super().__init__(account_id, account_holder, balance)
        self.interest_rate = interest_rate
        Account.total_accounts += 1

    def calculate_monthly_interest(self):
        """
            Calculate monthly interest earned
            Returns:
                float: Interest earned this month
        """
        return self.balance * (self.interest_rate / 100) / 12       

class CheckingAccount(Account): 
    def __init__(self, account_id, account_holder, balance = 0, overdraft_limit = 0):
        super().__init__(account_id, account_holder, balance)
        self.overdraft_limit = overdraft_limit
        Account.total_accounts += 1

    def withdraw(self, amount):
        """
            Withdraw money with overdraft protection
            Args:
                amount (float): Amount to withdraw
            Returns:
                bool: True if withdrawal successful, False otherwise
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < -self.overdraft_limit:
            return False
        self.balance -= amount
        return True

# Test your implementation


