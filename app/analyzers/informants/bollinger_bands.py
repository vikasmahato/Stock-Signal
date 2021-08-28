"""
Bollinger Bands Indicator
"""

import math

import numpy
import pandas

from analyzers.utils import IndicatorUtils


class Bollinger(IndicatorUtils):
    def analyze(self, historical_data, period_count=20):
        """
        Performs a bollinger band analysis on the historical data
        This is a volatility based indicator and tries to predict
        the underlying volatility of the asset.

        Bollinger band comprises of two lines plotted n (typically 2)
        Standard deviations from a `m` period simple moving average line (m typically 20)
        The bands widen during periods of increased volatility and shrink during period of
        reduced volatility.
        This is generally used in conjunction with ATR as they approach volatility differently

        Args:
            historical_data (DataFrame): A matrix of historical OHCLV data.
            period_count (int, optional): Defaults to 20. The number of data points to consider for
                our bollinger bands.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """

        dataframe = historical_data.copy()
        dataframe["middleband"] = dataframe["Adj Close"].rolling(period_count).mean()

        dataframe["upperband"] = dataframe["middleband"] + 2 * dataframe["Adj Close"].rolling(period_count).std(ddof=0)
        dataframe["lowerband"] = dataframe["middleband"] - 2 * dataframe["Adj Close"].rolling(period_count).std(ddof=0)
        dataframe["BB_width"] = dataframe["upperband"] - dataframe["lowerband"]

        return dataframe[["middleband", "upperband", "lowerband", "BB_width"]]
