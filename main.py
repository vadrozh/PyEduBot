# -*- coding: utf-8 -*-

from HTMLTableParser import HTMLTableParser
from config import URL

hp = HTMLTableParser()
table = hp.parse_url(URL)[0][1]
fname = r'data.csv'
table.head().to_csv(fname, index=False, header=True)

