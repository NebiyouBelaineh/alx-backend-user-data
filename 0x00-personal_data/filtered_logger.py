#!/usr/bin/env python3
"""Module containing filtered_datum function"""
import re
import logging
import os
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializer"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Obfuscate fields with format"""
        message = super(RedactingFormatter, self).format(record)
        result = filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR)
        return result


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated"""
    pattern = '|'.join([f"{field}=[^{separator}]+" for field in fields])
    return re.sub(pattern, lambda m: f"{m.group(0).split('=')[0]}={redaction}",
                  message)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object named user_data"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database"""
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    db = mysql.connector.connect(
        host=host,
        database=name,
        user=user,
        password=pwd,
        port=3306,
    )
    return db
