#!/usr/bin/env python3
"""Module containing filtered_datum function"""
import re
from typing import List

def filter_datum(flds: List[str], rdcn: str, msg: str, sep: str) -> str:
    """Returns the log messafe obfuscated"""
    pattern = '|'.join([f"{field}=[^{sep}]+" for field in flds])
    return re.sub(pattern, lambda m: f"{m.group(0).split('=')[0]}={rdcn}", msg)
