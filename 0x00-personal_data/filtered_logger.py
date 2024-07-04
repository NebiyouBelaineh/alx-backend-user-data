#!/usr/bin/env python3
"""Module containing filtered_datum function"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated"""
    pattern = '|'.join([f"{field}=[^{separator}]+" for field in fields])
    return re.sub(pattern, lambda m: f"{m.group(0).split('=')[0]}={redaction}",
                  message)
