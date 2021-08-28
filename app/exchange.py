"""
Interface for performing queries against exchange API's
"""

import re
import sys
import time
from datetime import datetime, timedelta, timezone

import yfinance as yf
import structlog
from tenacity import retry, retry_if_exception_type, stop_after_attempt


class ExchangeInterface:
    """
    Interface for performing queries against exchange API's
    """

    def __init__(self, ticker_config):
        """Initializes ExchangeInterface class

        Args:
            ticker_config (list): A list of tickers to operate on.
        """

        self.logger = structlog.get_logger()
        self.tickers = ticker_config

    def get_historical_data(self):
        """
        Get historical OHLCV for all tickers

        Returns:
            dict: Contains ticker as key and OHLCV data in value
        """
        historical_data = dict()
        for ticker in self.tickers:
            data = yf.download(ticker, period='1mo', interval='5m')
            data.dropna(how="any", inplace=True)
            historical_data[ticker] = data
        return historical_data