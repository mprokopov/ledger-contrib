# Scripts set for import to the *ledger-cli* transactions format

Scripts designed to be composable by pipe and standard unix utilities. There are two kinds of scripts: fetch raw data and processing to the proper .ledger format.

- fetch
- csv2ledger
- xml2ledger

## Dependencies
- python3
- pipenv

## Usage
issue command `pipenv sync` to install python dependencies

### Privat24 xml fetch

setup merchant account according to the [https://api.privatbank.ua/#p24/orders|Privat24 Merchant APIp]

for further steps you neer to have Merchant ID and Merchant password, for the convenience you can setup environment variables

- `PRIVAT_MERCHANT_ID`
- `PRIVAT_MERCHANT_PASSWORD`
 
 then issue the following command replacing 5167XXXXXXXXXXXX with your merchant card

`./fetch.py --sd=1.10.2019 --ed=31.12.2019 --card=5167XXXXXXXXXXXX > privat.xml`

### Payoneer CSV fetch

fetch and save payoyeer CSV file manually to some file, for example to *payoneer.csv*


### Privat24 XML processing to the ledger format

`cat privat.xml | ./xml2ledger > privat24.ledger`

### Payoneer CSV processing to the ledger format

`cat payoyeer.csv | ./csv2ledger > payoyeer.ledger`

### Hints

You can combine two ledger from Privat24 and Payoner by using only unix commands like this

`cat privat24.ledger payoneer.ledger > combined.ledger`

Use separate currencies file for analysis

Example: *currencies.ledger*

```

P 2019/01/01 00:00:01 UAH $0.035837

P 2019/02/01 00:00:01 UAH $0.035972

P 2019/03/01 00:00:01 UAH $0.0369

P 2019/04/01 00:00:01 UAH $0.0368375

P 2019/05/01 00:00:01 UAH $0.0379045

P 2019/06/01 00:00:01 UAH $0.037227

P 2019/07/01 00:00:01 UAH $0.0380305

P 2019/08/01 00:00:01 UAH $0.039379

P 2019/09/01 00:00:01 UAH $0.0398045

P 2019/10/01 00:00:01 UAH $0.040892

P 2019/11/01 00:00:01 UAH $0.04031028

P 2019/12/01 00:00:01 UAH $0.04183353

P 2019/01/01 02:18:01 EUR $1.12

P 2019/01/01 02:18:01 NOK $0.11

```

`ledger -f currencies.ledger -f combined.ledger -V bal`

### Implement your own classification for the transactions

Use `privat_example.py` and `payoneer_example.py` as example, rename to `privat.py` and `payoneer.py` and create your own implementation.
