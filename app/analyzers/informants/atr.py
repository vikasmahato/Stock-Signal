"""
ATR Indicator
"""

import math

import numpy
import pandas

from analyzers.utils import IndicatorUtils


class Atr(IndicatorUtils):
    def analyze(self, historical_data, n=14):
        """
        Performs ATR (Average True Range) analysis on historical data.
        This is a volatility based indicator and tries to predict
        the underlying volatility of the asset.

        ATR focuses on total price movement and conveys how widely the market is swinging
        as it moves.
        It takes into account the price movement in each period by considering the following ranges
            - Difference between High and Low of each period
            - Difference between High and previous period's close
            - Difference between Low and previous period's close
        This is generally used in conjunction with Bollinger bands as they approach volatility differently

        Args:
            historical_data (pandas.DataFrame): A matrix of historical OHCLV data.
            n (int, optional): Defaults to 14. The number of data points to consider for
                our bollinger bands.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """

        dataframe = historical_data.copy()

        dataframe['H-L'] = dataframe["High"] - dataframe["Low"]
        dataframe['H-PC'] = dataframe["High"] - dataframe["Adj Close"].shift(1)
        dataframe['L-PC'] = dataframe["Low"] - dataframe["Adj Close"].shift(1)

        dataframe["TR"] = dataframe[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)

        dataframe["ATR"] = dataframe["TR"].ewm(com=n, min_periods=n).mean()
        return dataframe["ATR"]
