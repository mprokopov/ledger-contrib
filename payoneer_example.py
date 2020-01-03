import re
def income_from_payee(self, payee):
        if re.search('MYCOMPANY', payee):
            self.name = 'Work'
        else:
            self.name = 'Reimbursments'

def expense_from_payee(self, payee):
    if re.search('WOG|SLOVNAFT|OMV 1971|HUNOIL', payee):
        self.name = 'Car:Gasoline'
    elif re.search(r'Uber BV|NSB OSL TVM|www.airbaltic.com|KVG|BOLT.EU|WIENER LINIEN', payee):
        self.name = 'Transport'
    elif re.search('AIRBNB|HOLIDAY INN|APARTMENTS|HOTEL', payee):
        self.name = 'Vacation:Hotel'
