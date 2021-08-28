"""
Pattern recognition
"""

import numpy as np
import pandas
import talib
from itertools import compress
from rank import candle_rankings

from analyzers.utils import IndicatorUtils

class Patternrecognition(IndicatorUtils):
    def analyse(self, historical_data):
        """
        Recognizes candlestick patterns and appends 2 additional columns to df;
        1st - Best Performance candlestick pattern matched by www.thepatternsite.com
        2nd - # of matched patterns

        Args:
            historical_data (pandas.DataFrame): A matrix of historical OHCLV data.
        Returns:
            pandas.DataFrame: A dataframe containing the indicators
        """
        dataframe = historical_data.copy()
        op = dataframe["Open"]
        hi = dataframe["High"]
        lo = dataframe["Low"]
        cl = dataframe["Adj Close"]

        # List of all pattern names
        candle_names = talib.get_function_groups()['Pattern Recognition']

        # patterns not found in the patternsite.com
        exclude_items = ('CDLCOUNTERATTACK',
                         'CDLLONGLINE',
                         'CDLSHORTLINE',
                         'CDLSTALLEDPATTERN',
                         'CDLKICKINGBYLENGTH')

        candle_names = [candle for candle in candle_names if candle not in exclude_items]

        # create columns for each candle
        for candle in candle_names:
            # below is same as;
            # dataframe["CDL3LINESTRIKE"] = talib.CDL3LINESTRIKE(op, hi, lo, cl)
            dataframe[candle] = getattr(talib, candle)(op, hi, lo, cl)

        dataframe['candlestick_pattern'] = np.nan
        dataframe['candlestick_match_count'] = np.nan

        for index, row in dataframe.iterrows():

            # no pattern found
            if len(row[candle_names]) - sum(row[candle_names] == 0) == 0:
                dataframe.loc[index,'candlestick_pattern'] = "NO_PATTERN"
                dataframe.loc[index, 'candlestick_match_count'] = 0
            # single pattern found
            elif len(row[candle_names]) - sum(row[candle_names] == 0) == 1:
                # bull pattern 100 or 200
                if any(row[candle_names].values > 0):
                    pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bull'
                    dataframe.loc[index, 'candlestick_pattern'] = pattern
                    dataframe.loc[index, 'candlestick_match_count'] = 1
                # bear pattern -100 or -200
                else:
                    pattern = list(compress(row[candle_names].keys(), row[candle_names].values != 0))[0] + '_Bear'
                    dataframe.loc[index, 'candlestick_pattern'] = pattern
                    dataframe.loc[index, 'candlestick_match_count'] = 1
            # multiple patterns matched -- select best performance
            else:
                # filter out pattern names from bool list of values
                patterns = list(compress(row[candle_names].keys(), row[candle_names].values != 0))
                container = []
                for pattern in patterns:
                    if row[pattern] > 0:
                        container.append(pattern + '_Bull')
                    else:
                        container.append(pattern + '_Bear')
                rank_list = [candle_rankings[p] for p in container]
                if len(rank_list) == len(container):
                    rank_index_best = rank_list.index(min(rank_list))
                    dataframe.loc[index, 'candlestick_pattern'] = container[rank_index_best]
                    dataframe.loc[index, 'candlestick_match_count'] = len(container)

        # clean up candle columns
        cols_to_drop = candle_names + list(exclude_items)
        dataframe.drop(cols_to_drop, axis = 1, inplace = True)

        return dataframe
