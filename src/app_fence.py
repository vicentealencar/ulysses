import json
import operator
import subprocess

import config

from upact.datetime import is_time_in_interval, is_day_in_recurrence

from datetime import datetime
from functools import reduce


with open(config.APPS_TO_BLOCK, "r") as block_list_file:
    block_list = [s.strip() for s in block_list_file.readlines()]

with open(config.APP_PLAYTIME_RULES) as exceptions_file:
    block_exceptions = json.loads(exceptions_file.read())

for be in block_exceptions:
    today = datetime.now()

    if not is_day_in_recurrence(be["frequency"], today):
        continue

    if reduce(operator.or_, 
            map(lambda period: is_time_in_interval(period[0], period[1], today.time()), be['time_periods'])):

        print("The APP(s) %s are currently accessible" % be['apps'])

        block_list = list(set(block_list) - set(be['apps']))

for app_to_kill in block_list:
    subprocess.call(["sudo", "pkill", "-9", app_to_kill])
