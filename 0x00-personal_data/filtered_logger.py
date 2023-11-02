#!/usr/bin/env python3
"""
use of regexing
"""
import re
from typing import List
import logging
import mysql.connector
import os


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        return filter_datum(
                self.fields, self.REDACTION, log_message, self.SEPARATOR)


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Method that connect to a database
    """
    db_connect = mysql.connector.connect(
            user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
            host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return db_connect


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
 ) -> str:
    """
    method that returns log message obfuscated
    """
    for field in fields:
        message = re.sub(f'{field}=(.*?){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    Method that takes no arg and return logging.logger
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = redactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    main()
