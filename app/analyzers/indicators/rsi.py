""" RSI Indicator
"""

import pandas
import numpy as np
from analyzers.utils import IndicatorUtils


class RSI(IndicatorUtils):
    def analyze(self, historical_data, period_count=14,
                signal=['rsi'], hot_thresh=None, cold_thresh=None):
        """
        Performs an RSI analysis on the historical data
        This is a momentum oscillator.
        RSI > 70, overbought
        RSI < 30, oversold

        However, rsi value can hover in a region for a very long time (upto a month)

        Args:
            historical_data (pandas.DataFrame): A matrix of historical OHCLV data.
            period_count (int, optional): Defaults to 14. The number of data points to consider for
                our RSI.
            signal (list, optional): Defaults to rsi. The indicator line to check hot/cold
                against.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """

        dataframe = historical_data.copy()
        dataframe["change"] = dataframe["Adj Close"] - dataframe["Adj Close"].shift(1)
        dataframe["gain"] = np.where(dataframe["change"]>=0, dataframe["change"], 0)
        dataframe["loss"] = np.where(dataframe["change"]<0, -1*dataframe["change"], 0)
        dataframe["avgGain"] = dataframe["gain"].ewm(alpha=1/period_count, min_periods=period_count).mean()
        dataframe["avgLoss"] = dataframe["loss"].ewm(alpha=1/period_count, min_periods=period_count).mean()
        dataframe["rs"] = dataframe["avgGain"]/dataframe["avgLoss"]
        dataframe["rsi"] = 100 - (100/ (1 + dataframe["rs"]))
        return dataframe["rsi"]
