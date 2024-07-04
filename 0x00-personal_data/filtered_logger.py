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
    for field in fields:
        message = re.sub(
            rf'({re.escape(field)}=)[^{re.escape(separator)}]*',
            r'\1' + redaction,
            message)
    return message
