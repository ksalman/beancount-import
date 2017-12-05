#!/usr/bin/env python
import csv
import datetime
import re
import pprint
import logging
from os import path

from dateutil.parser import parse

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

  def __init__(self, currency):
    print('foo')
    self.currency = currency

  def identify(self, file):
    print('bar')
    return (re.match(r"stmt.csv", path.basename(file.name)) and
            re.match("Description,,Summary Amt.", file.head()))


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
