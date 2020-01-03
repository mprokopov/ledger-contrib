#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sys
import re
import privat
from ledger import CashAccount,ExpenseAccount,Money,Transaction,IncomeAccount,Account

class PrivatIncomeAccount(IncomeAccount):
    from_payee_comment = privat.income_from_payee_comment

class PrivatExpenseAccount(ExpenseAccount):
    from_payee_comment = privat.expense_from_payee_comment

class PrivatTransaction(Transaction):
    def __init__(self,date='',amount='',payee='',comment=''):
        value, currency = amount.split(' ')
        super().__init__(date=date,
                         money=Money(amount=self.clear_amount(value),currency=currency),
                         payee=payee,
                         comment=comment)
        self.negative = re.search('-', amount) is not None
        if self.negative:
            self.debit = CashAccount()
            self.credit = PrivatExpenseAccount()
            self.credit.from_payee_comment(payee=payee, comment=comment)
        else:
            self.credit = CashAccount()
            self.debit = PrivatIncomeAccount()
            self.debit.from_payee_comment(payee=payee, comment=comment)

resp = ET.parse(sys.stdin)
for i in resp.findall('.//statement'):
    amount = i.attrib['cardamount']
    terminal = i.attrib['terminal']
    tr_date = i.attrib[ 'trandate' ]
    description = i.attrib['description']

    trans = PrivatTransaction(amount=amount,
                              date=tr_date.replace('-','/'),
                              payee=terminal,
                              comment=description)
    print(trans)
