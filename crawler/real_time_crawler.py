import os
import datetime
from ssq_crawler import add_ssq_data
from dlt_crawler import add_dlt_data
from utils import find_last_year
SSQ_CURRENT_YEAR = datetime.datetime.now().year
print(SSQ_CURRENT_YEAR)
DLT_CURRENT_YEAR = SSQ_CURRENT_YEAR%100
print(DLT_CURRENT_YEAR)
SSQ_FROM = 2003
DLT_FROM = 7
ROOT_DIR = '../data'
if (not os.path.exists(ROOT_DIR)):
    os.mkdir(ROOT_DIR)
ssq_last = find_last_year(ROOT_DIR, prefix='ssq_')
dlt_last = find_last_year(ROOT_DIR, prefix='dlt_')
if ssq_last > SSQ_FROM:
    SSQ_FROM = ssq_last
if dlt_last > DLT_FROM:
    DLT_FROM = dlt_last

for year in range(SSQ_FROM, SSQ_CURRENT_YEAR+1):
    add_ssq_data(rootdir=ROOT_DIR, year=f'{year:04d}')
for year in range(DLT_FROM, DLT_CURRENT_YEAR+1):
    add_dlt_data(rootdir=ROOT_DIR, year=f'{year:02d}')
