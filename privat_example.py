import re
def income_from_payee_comment(self, payee='', comment=''):
    if re.search('CS980400', payee):
        elif re.search('Перевод со своей карты', comment):
            self.parent = Account(name='Assets')
            self.name = 'Cash:FOP'
    elif re.search('WWW.27.UA', payee):
        self.parent = Account(name='Assets')
        self.name = 'Reimbursments'

def expense_from_payee_comment(self, payee='', comment=''):
    if re.search('WOG|OKKO|SHELL AZS|AVANTI', payee):
        self.name = 'Car:Gasoline'
    elif re.search('Citrus', payee):
        self.name = 'Gadgets'
