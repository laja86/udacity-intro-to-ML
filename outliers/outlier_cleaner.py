#!/usr/bin/python
from operator import itemgetter, attrgetter

def outlierCleaner(net_worths_pred, ages, net_worths_actual):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where
        each tuple is of the form (age, net_worth, error).
    """
    PERCENT_TO_REMOVE = 10

    ### your code goes here
    errors = [x - y for x, y in zip(net_worths_actual, net_worths_pred)]
    cleaned_data = zip(ages, net_worths_actual, errors)
    cleaned_data = sorted(cleaned_data, key=lambda x: abs(x[2]))
    # number of points to remove
    n = (len(cleaned_data) * PERCENT_TO_REMOVE) / 100

    return cleaned_data[:-n]
