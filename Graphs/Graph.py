import pandas as pd
import sys
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"

# Common imports
import numpy as np
import os
import matplotlib as mpl
import matplotlib.pyplot as plt


def load_NSIN_data():
    df = pd.read_csv('../datasets/DeviceCoordinates.csv')

    return df

coordinates = load_NSIN_data()

coordinates.head(n=5)
