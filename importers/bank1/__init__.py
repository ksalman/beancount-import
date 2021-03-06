#!/usr/bin/env python
import csv
import datetime
import re
import pprint
import logging
from os import path

from itertools import islice
from dateutil.parser import parse
from titlecase import titlecase
from beancount.core import flags

from beancount.core.number import D
from beancount.core.number import ZERO
from beancount.core.number import MISSING
from beancount.core import data
from beancount.core import account
from beancount.core import amount
from beancount.core import position
from beancount.core import inventory
from beancount.ingest import importer
from beancount.ingest import regression

class Importer(importer.ImporterProtocol):

  def __init__(self, currency,
               account_root,
               account2):
    self.currency = currency
    self.account_root = account_root
    self.account2 = account2

  def identify(self, file):
    return (re.match(r"stmt.csv", path.basename(file.name)) and
            re.match("Description,,Summary Amt.", file.head()))

  def file_account(self, _):
    return self.account_root

  def extract(self, file):
    entries = []
    with open(file.name) as f:
      for index, row in enumerate(csv.DictReader(islice(f, 6, None))):
        if index == 0:
          if 'Beginning balance' in row['Description']:
            continue
          else:
            logging.error("Missing 'Beginning balance' in '{}'".format(row['Description']))

        meta = data.new_metadata(file.name, index)
        trans_date = parse(row['Date']).date()
        trans_desc = titlecase(row['Description'])
        trans_amt = row['Amount']
        units = amount.Amount(D(row['Amount']), self.currency)

        txn = data.Transaction(
            meta, trans_date, self.FLAG, trans_desc, None, data.EMPTY_SET, data.EMPTY_SET, [
                data.Posting(self.account_root, units, None, None, None, None),
                data.Posting(self.account2, -units, None, None, None, None),
            ])

        entries.append(txn)

    return entries
