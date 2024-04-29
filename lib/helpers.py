import os
import re
import json
import time
import random
import hashlib
import asyncio
from datetime import datetime
from pathlib import Path

for x in os.environ:
    globals()[x] = os.environ[x]

# Return first non-null value
# https://stackoverflow.com/a/16247152
def coalesce(*arg):
    for el in arg:
        if el is not None:
            return el
    return None

def safely_get(input_array, key, default_value):
    if key in input_array:
        if input_array[key] is not None:
            return input_array[key]

    return default_value

def read_file(f_name, f_data_default):
    try:
        f_handle = open(f_name)
        f_data = f_handle.read()
        f_handle.close()
        return f_data
    except Exception as x:
        print(x)
        return f_data_default

def write_file(f_path, f_data):
    with Path(f_path) as f:
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(f_data)

def emoji_free_str(input_string):
    global emoji_pattern
    return emoji_pattern.sub(u"", input_string)

def get_timestamp(fname_safe=False):
    format_str = "%Y-%m-%d %H:%M:%S."
    format_str = "%Y%m%d_%H%M%S_" if fname_safe == True else format_str

    now = datetime.now()
    timestamp = now.strftime("%f")[:-3]
    timestamp = now.strftime(format_str) + timestamp
    return timestamp

def new_md5():
    input_str = str(time.time())
    md5_hash = hashlib.md5(input_str.encode()).hexdigest()
    return md5_hash

'''
Threading related:
'''
LOCK = False
async def thread_lock():
    global LOCK
    while LOCK is True:
        await asyncio.sleep(1)
    LOCK = True

def thread_unlock():
    global LOCK
    LOCK = False
