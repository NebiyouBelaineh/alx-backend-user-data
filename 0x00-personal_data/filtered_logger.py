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
        port=3306,
        user=user,
        password=pwd,
        database=name,
    )
    return db


def main():
        """Logs the information about user records in a table."""
        fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
        columns = fields.split(',')
        query = "SELECT {} FROM users;".format(fields)
        info_logger = get_logger()
        connection = get_db()
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                record = map(
                    lambda x: '{}={}'.format(x[0], x[1]),
                    zip(columns, row),
                )
                msg = '{};'.format('; '.join(list(record)))
                args = ("user_data", logging.INFO, None, None, msg, None, None)
                log_record = logging.LogRecord(*args)
                info_logger.handle(log_record)


if __name__ == "__main__":
    main()
