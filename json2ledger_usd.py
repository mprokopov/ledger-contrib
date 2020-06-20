#!/usr/bin/env python
from datetime import datetime
import requests
import sys
import json
import re
import privat_fop as privat
from ledger import *
from datetime import date

class PrivatCashAccount(CashAccount):
    from_acc = privat.from_acc

class PrivatIncomeAccount(IncomeAccount):
    from_payee = privat.income_from_payee

class PrivatExpenseAccount(ExpenseAccount):
    from_payee = privat.expense_from_payee

class PrivatTransaction(Transaction):
    def clear_date(self, date):
        return datetime.strptime(date,'%d.%m.%Y').strftime('%Y/%m/%d')

    def __init__(self, **kvargs):
        payee=kvargs['AUT_CNTR_NAM']
        if re.search('КОМИССИЯ ЗА ДЕБЕТОВАНИЕ', payee):
            payee=kvargs['AUT_MY_MFO_NAME']
        amount=kvargs['BPL_SUM']
        currency=kvargs['BPL_CCY']
        date=kvargs['BPL_DAT_OD']
        comment=kvargs['BPL_OSND']
        acc=kvargs['AUT_MY_ACC']
        tran_type=kvargs['TRANTYPE'] # C - income, D - expense
        if tran_type == 'C':
            debit = PrivatIncomeAccount()
            credit = PrivatCashAccount()
            debit.from_payee(payee, comment)
            credit.from_acc(acc)

        elif tran_type == 'D':
            debit = PrivatCashAccount()
            credit = PrivatExpenseAccount()
            credit.from_payee(payee, comment)
            debit.from_acc(acc)
        else:
            raise('Wrong transaction type')
        super().__init__(debit=debit,
                         credit=credit,
                         date=self.clear_date(date),
                         money=Money(amount,currency),
                         payee=payee,
                         comment=comment)

#f = open("q2.json", "r")
resp = json.load(sys.stdin)
#resp = json.load(f)
transactions = list()

for bankaccounts in resp['StatementsResponse']['statements']:
    for statements in bankaccounts.values():
        for statement in statements:
            for v in statement.values():
                transactions.append(PrivatTransaction(**v))

for tran in transactions:
    print(tran)
