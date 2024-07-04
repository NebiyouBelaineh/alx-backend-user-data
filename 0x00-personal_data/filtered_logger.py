#!/usr/bin/env python3
"""Module containing filtered_datum function"""
import re
from typing import List


def filter_datum(flds: List[str], rdcn: str, msg: str, sep: str) -> str:
    """Returns the log message obfuscated"""
    for field in flds:
        message = re.sub(rf'({re.escape(field)}=)[^{re.escape(sep)}]*',
                         r'\1' + rdcn, msg)
    return message
