"""
@AUTHOR:: Philip Julian
@CREATED_DATE: 9 May 2023
@PURPOSE: Runs all SQL commands for the program
@TODO: None
"""
from constants import CURSOR, CONNECTION
import pandas as pd


class sql_writer:
    def __init__(self) -> None:
        pass

    def sql_commander(self, command: str):
        CURSOR.execute(command)
        CONNECTION.commit()

        return CURSOR

    def sql_retriever(self, command: str):
        return CURSOR.execute(command)
