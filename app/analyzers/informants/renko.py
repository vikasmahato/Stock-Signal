"""
Renko Indicator
"""

import pandas

from analyzers.utils import IndicatorUtils
from stocktrends import Renko
from atr import Atr
import yfinance as yf

class Renko(IndicatorUtils):
    def analyze(self, historical_data, ticker):
        """
        Performs Renko analysis on historical data.

        Args:
            historical_data (pandas.DataFrame): A matrix of historical OHCLV data.
            ticker (string, optional): The ticker for which hourly data is required.
        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """

        hourly_dataframe = yf.download(ticker,period='1y',interval='1h')
        hourly_dataframe.dropna(how="any",inplace=True)

        dataframe = historical_data.copy()
        dataframe.reset_index(inplace=True)
        dataframe.drop("Close",axis=1,inplace=True)
        dataframe.columns = ["date","open","high","low","close","volume"]
        dataframe2 = Renko(dataframe)
        dataframe2.brick_size = 3*round(Atr(hourly_dataframe,120).iloc[-1],0)
        renko_dataframe = dataframe2.get_ohlc_data()
        return renko_dataframe
