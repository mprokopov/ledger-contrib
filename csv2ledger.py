#!/usr/bin/env python
import csv
from datetime import datetime
import re
import sys
import payoneer
from ledger import CashAccount,ExpenseAccount,Money,Transaction,Account,IncomeAccount

class PayoneerCashAccount(Account):
    def __init__(self, currency=''):
        self.currency = currency
        self.parent = Account(name='Assets')
        super().__init__(name=f'Payoneer:{self.currency}')
    def __str__(self):
        return f'{self.parent}:{self.name}'

class PayoneerIncomeAccount(IncomeAccount):
    from_payee = payoneer.income_from_payee

class PayoneerExpenseAccount(ExpenseAccount):
    from_payee = payoneer.expense_from_payee

class PayoneerTransaction(Transaction):
    def clear_date(self, date):
        return datetime.strptime(date,'%m/%d/%Y').strftime('%Y/%m/%d')
    def clear_amount(self, amount):
        return amount.replace(',','').replace('-','')
    def __init__(self,date='', debit_amount=None, credit_amount=None, currency='', payee=''):
        if debit_amount:
            amount = debit_amount
            self.negative = True
        if credit_amount:
            amount = credit_amount
            self.negative = False
        super().__init__(date=self.clear_date(date),
                         money=Money(amount=self.clear_amount(amount),currency=currency),
                         payee=payee)
        # self.negative = re.search('-', amount) is not None
        self.is_transfer = re.search('USD to EUR', payee) is not None

        if self.negative:
            if self.is_transfer:
                # transfer
                self.credit=Account(name='Payoneer:Currency')
                self.debit=PayoneerCashAccount(currency)
            else:
                # expense
                self.debit=PayoneerCashAccount(currency)
                self.credit=PayoneerExpenseAccount()
                self.credit.from_payee(payee)
        else:
            if self.is_transfer:
                self.debit=Account(name='Payoneer:Currency')
                self.credit=PayoneerCashAccount(currency)
            else:
                self.debit=PayoneerIncomeAccount()
                self.credit=PayoneerCashAccount(currency)
                self.debit.from_payee(payee)

csvreader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
next(csvreader) # skip header
for row in csvreader:
    # Transaction Date,Transaction Time,Time Zone,Transaction ID,Description,Credit Amount,Debit Amount,Currency,Status,Running Balance,Additional Description,Store Name
    trans = PayoneerTransaction(credit_amount=row[5],
                                debit_amount=row[6],
                                currency=row[7],
                                payee=row[4],
                                date=row[0])
    print(trans)
