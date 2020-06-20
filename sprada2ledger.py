#!/usr/bin/env python
import csv
from datetime import datetime
import re
import sys
import sprada
from ledger import CashAccount,ExpenseAccount,Money,Transaction,Account,IncomeAccount

class SpradaCashAccount(Account):
    def __init__(self, currency=''):
        self.currency = currency
        self.parent = Account(name='Assets')
        super().__init__(name=f'Sprada:{self.currency}')
    def __str__(self):
        return f'{self.parent}:{self.name}'

class SpradaIncomeAccount(IncomeAccount):
    from_payee = sprada.income_from_payee

class SpradaExpenseAccount(ExpenseAccount):
    from_payee = sprada.expense_from_payee

class SpradaTransaction(Transaction):
    def clear_date(self, date):
        return datetime.strptime(date,'%d.%m.%Y').strftime('%Y/%m/%d')
    def clear_amount(self, amount):
        return amount.replace('.','').replace(',','.').replace('-','')
    def __init__(self,date='', amount=None, currency='', payee=''):
        super().__init__(date=self.clear_date(date),
                         money=Money(amount=self.clear_amount(amount),currency=currency),
                         payee=payee)
        self.negative = re.search('-', amount) is not None
        self.is_transfer = re.search('MAKSYM', payee) is not None

        if self.negative:
            if self.is_transfer:
                # transfer
                self.credit=Account(name='Sprada:Transfer')
                self.debit=SpradaCashAccount(currency)
            else:
                # expense
                self.debit=SpradaCashAccount(currency)
                self.credit=SpradaExpenseAccount()
                self.credit.from_payee(payee)
        else:
            if self.is_transfer:
                self.debit=Account(name='Sprada:Transfer')
                self.credit=SpradaCashAccount(currency)
            else:
                self.debit=SpradaIncomeAccount()
                self.credit=SpradaCashAccount(currency)
                self.debit.from_payee(payee)

csvreader = csv.reader(sys.stdin, delimiter=';', quotechar='"')
next(csvreader) # skip header
for row in csvreader:
    # Transaction Date,Transaction Time,Time Zone,Transaction ID,Description,Credit Amount,Debit Amount,Currency,Status,Running Balance,Additional Description,Store Name
    print(row)

    trans = SpradaTransaction(amount=row[3],
                              currency=row[4],
                              payee=row[2],
                              date=row[0])
    print(trans)
