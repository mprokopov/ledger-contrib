#!/usr/bin/env python
import argparse
import hashlib
import requests
import os
from datetime import date
import xml.etree.ElementTree as ET

def inner_xml(element):
    return (element.text or '') + ''.join(ET.tostring(e, encoding='unicode') for e in element)

def signature(data='',password=''):
    md5 = hashlib.md5(( data+password ).encode('utf-8')).hexdigest()
    sha1= hashlib.sha1(md5.encode('utf-8'))
    return sha1.hexdigest()

def build_req(args):
    req = ET.Element('request')
    req.set('version','1.0')
    merch = ET.SubElement(req, 'merchant')
    id = ET.SubElement(merch, 'id')
    id.text = args.merchant_id   # Merchant ID
    sign = ET.SubElement(merch, 'signature')
    data = ET.SubElement(req, 'data')
    oper = ET.SubElement(data, 'oper')
    oper.text = 'cmt'
    wait = ET.SubElement(data, 'wait')
    wait.text = '0'
    payment = ET.SubElement(data,'payment', {'id': ''})
    sd = ET.SubElement(payment, 'prop', {'name': 'sd', 'value': args.sd})
    ed = ET.SubElement(payment, 'prop', {'name': 'ed', 'value': args.ed})
    card = ET.SubElement(payment, 'prop', {'name': 'card', 'value': args.card})
    sign.text = signature(data=inner_xml(data), password=args.merchant_password)

    return req

today_str = date.today().strftime('%d.%m.%Y')
parser = argparse.ArgumentParser(description='Fetches statements XML from Privat24 Merchant API for the defined period.')
parser.add_argument('--merchant-id', help='Privat24 merchant ID', default=os.environ["PRIVAT_MERCHANT_ID"])
parser.add_argument('--merchant-password', help='Privat24 merchant password', default=os.environ["PRIVAT_MERCHANT_PASSWORD"])
parser.add_argument('--sd', help='start date', default=today_str)
parser.add_argument('--ed', help='end date', default=today_str)
parser.add_argument('-debug', help='debug',action='store_const', const=True)
parser.add_argument('--card', help='MasterCard or Visa card number', required=True)
args = parser.parse_args()

if args.debug:
    print(ET.tostring(build_req(args)))
else:
    r=requests.post(url='https://api.privatbank.ua/p24api/rest_fiz', data=ET.tostring(build_req(args)))
    print(r.text)
