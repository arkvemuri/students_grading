import pandas as pd
import os

basedir = os.path.abspath(os.path.dirname(__file__))

data = pd.read_csv(os.path.join(basedir, 'xAPI-Edu-Data.csv'))

print (data.to_html())