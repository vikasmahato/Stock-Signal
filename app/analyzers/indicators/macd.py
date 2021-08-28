""" MACD Indicator
"""

import math

import pandas

from analyzers.utils import IndicatorUtils


class MACD(IndicatorUtils):
    def analyze(self, historical_data, signal=['macd'], hot_thresh=None, cold_thresh=None):
        """Performs a macd analysis on the historical data

        Args:
            historical_data (): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to macd. The indicator line to check hot/cold
                against.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """

        dataframe = historical_data.copy()
        dataframe['ma_fast'] = dataframe['Adj Close'].ewm(span=12, min_periods=12).mean()
        dataframe['ma_slow'] = dataframe['Adj Close'].ewm(span=26, min_periods=26).mean()
        dataframe['macd'] = dataframe['ma_fast'] - dataframe['ma_slow']
        dataframe['signal'] = dataframe['macd'].ewm(span=9, min_periods=9).mean()

        #TODO: this is wrong. we need to figure out if signal is being cut by macd from above or below
        dataframe['is_hot'] = dataframe['macd'] > dataframe['signal']
        dataframe['is_cold'] = dataframe['macd'] <= dataframe['signal']

        return dataframe.loc[:, ['macd', 'signal', 'is_hot', 'is_cold']]
