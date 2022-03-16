#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import dateutil.parser
import re


def parse_keyvalue_pairs(line):
    ret_keyvalue = []
    # key_value_list = re.findall(r"\w+\s*=\s*[^, ]+",line)
    key_value_list = re.findall(r"[^,=:\[\]]+\s*=\s*[^, ]+", line)
    for pair in key_value_list:
        idx = pair.find("=")
        key = pair[:idx].strip()
        value = pair[idx+1:].strip()
        ret_keyvalue.append((key, value))
    return ret_keyvalue


def parse_ftrace_keyvalue_pairs(line):
    ret_ts = None
    ret_keyval = []
    m = re.match(r".*\[\d+\]\s*([\d.]+):\s*(\S*):\s*(.*)", line)
    if not m:
        return None
    ret_ts = float(m.group(1))
    trace_name = m.group(2)
    key_value_str = m.group(3)
    ret_keyval = parse_keyvalue_pairs(key_value_str)
    ret_keyval = [(trace_name + ":" + p[0], p[1]) for p in ret_keyval]
    return (ret_ts, ret_keyval)


def parse_teraterm_keyvalue_pairs(line):
    ret_ts = None
    ret_keyval = []
    m = re.match(r"\s*\[(.+)\]\s*(([\S^:]+):)?(.*)", line)
    if not m:
        return None
    ret_ts = dateutil.parser.parse(m.group(1), fuzzy=True).timestamp()
    trace_name = m.group(3)
    key_value_str = m.group(4)
    ret_keyval = parse_keyvalue_pairs(key_value_str)
    if trace_name:
        ret_keyval = [(trace_name + ":" + p[0], p[1]) for p in ret_keyval]
    return (ret_ts, ret_keyval)


def ParseKeyValue(line):
    line = line.strip()
    if line.startswith("["):
        return parse_teraterm_keyvalue_pairs(line)
    else:
        return parse_ftrace_keyvalue_pairs(line)


"""
--------------------------------------------------------
Main Test
--------------------------------------------------------
"""
if __name__ == '__main__':
    # line = r"[2022-03-12 19:00:37.955] GTM: temp = 24106, cur freq = 214000 KHz, ttj = 95000, bless=1.1 god-12.22"
    # line = r"[2022-03-12 19:00:37.955] temp = 24106, cur freq = 214000 KHz, ttj = 95000, bless=1.1 god=12.22"
    line = r" <idle>-0 [005] 387.386832: sched_wakeup: comm=met-cmd pid=6840 prio=120 success=1 target_cpu=005 state=R"

    # print(parse_ftrace_keyvalue_pairs(line))
    print(ParseKeyValue(line))
