class Account():
    def __init__(self, name='Expenses:Unknown'):
        self.name = name
    def __str__(self):
        return self.name

class IncomeAccount(Account):
    def __init__(self, name='Unknown'):
        self.parent = Account(name='Income')
        super().__init__(name=name)
    def __str__(self):
        return f'{self.parent}:{self.name}'
    def from_payee(self, payee):
        self.name = 'Unknown'

class ExpenseAccount(Account):
    def __init__(self, name='Unknown'):
        self.parent = Account(name='Expenses')
        super().__init__(name=name)
    def __str__(self):
        return f'{self.parent}:{self.name}'
    def from_payee(self, payee):
        self.name = 'Unknown'

class CashAccount(Account):
    def __init__(self, name='Cash'):
        self.parent = Account(name='Assets')
        super().__init__(name=name)
    def __str__(self):
        return f'{self.parent}:{self.name}'

class Money():
    def __init__(self, amount=0,currency='USD'):
        self.amount=amount
        self.currency=currency
    def __str__(self):
        if self.currency == 'USD':
            return f'${self.amount}'
        else:
            return f'{self.amount} {self.currency}'

class Transaction():
    def __init__(self, debit='',credit='',date='',money='',payee='',comment=''):
        self.debit = debit
        self.credit = credit
        self.date = date
        self.money = money
        self.payee = payee
        self.comment = comment
    def clear_amount(self, amount):
        return amount.replace(',','').replace('-','')
    def __str__(self):
        comment = ''
        if self.comment:
            comment = f'\n ;; {self.comment}'
        return f'{self.date} {self.payee}\n  {self.credit}   {self.money}\n  {self.debit} {comment}'
