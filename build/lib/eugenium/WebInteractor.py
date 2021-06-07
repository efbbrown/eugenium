import logging
from typing import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


class BaseWebInteractor():
    """
    """
    def __init__(self,
                 wait_time: int = 3,
                 driver_path: str = None,
                 *args,
                 **kwargs):
        """
        """
        self.driver_path = driver_path
        self.driver = webdriver.Chrome(self.driver_path)
        self.ignored_exceptions = (
            NoSuchElementException,
            StaleElementReferenceException,
        )

    # def create_driver(self, driver_path: str = None):
    #     """Creates a driver instance for your interactor

    #     Parameters
    #     ----------
    #     driver_path : str
    #         The location of your chrome driver

    #     Returns
    #     -------
    #     None
    #     """
    #     if self.driver_path is None:
    #         self.driver_path = driver_path
    #     self.driver = webdriver.Chrome(driver_path)

    def find(self, by: str, identifier: str):
        result = WebDriverWait(
            self.driver, self.wait_time,
            ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located(
                    (by, identifier)))
        return result

    def data_to_sql(self,
                    data_collector: Callable,
                    name: str,
                    con,
                    schema=None,
                    if_exists: str = "fail",
                    **kwargs):
        """Runs a function that outputs a pandas dataframe and commits it to a
        database.

        Parameters
        ----------
        data_collector : Callable
            A function that will run some selenium code and return a pandas
            dataframe. Must accept an argument named driver that will be the
            selenium driver.            
        name : str
            Name of SQL table.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        con : sqlalchemy.engine.(Engine or Connection) or sqlite3.Connection
            Using SQLAlchemy makes it possible to use any DB supported by that library.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        schema : str, optional
            Specify the schema (if database flavor supports this). If None, use default schema.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
        if_exists : {‘fail’, ‘replace’, ‘append’}, default ‘fail’
            How to behave if the table already exists.
                fail: Raise a ValueError.
                replace: Drop the table before inserting new values.
                append: Insert new values to the existing table.
            See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html
            
        Returns
        -------
        None

        """
        try:
            df = data_collector(driver=self.driver, **kwargs)
            df.to_sql(con=con, schema=schema, if_exists=if_exists)
        except e:
            logging.debug(e)
