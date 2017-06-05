import csv
import pandas
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz

def remove_commas(s):
  return str(s).replace(',', '')

def wrap_in_quotes(s):
  return '"{0}"'.format(s)

# converts pandas dataframe to arff
def dataframe_to_arff(dataframe, filename, coltypes, relation, include_index=False):
    dataframe = dataframe.applymap(remove_commas)
    if include_index:
        dataframe = dataframe.reset_index()
        
    with open(filename, 'w') as f:
        f.write('@relation {}\n'.format(relation))
        
        for column in dataframe:
            levels = dataframe[column].unique()
            set_notation = '{' + ','.join('"{0}"'.format(w) for w in map(str, levels)) + '}'
            f.write('@attribute {} {}\n'.format(column, set_notation))

        f.write('@data\n')
        dataframe = dataframe.applymap(wrap_in_quotes)
        dataframe.to_csv(f, header=False, index=False, quoting=csv.QUOTE_NONE)

data = pandas.io.stata.read_stata('data/aa.dta')

attrs = ['asnidone', 'educ', 'q21', 'q24', 'q80', 'q10', 'q87']

cols = [c for c in data.columns if c in attrs]
data = data[cols]

# remove data with unanswered questions
for a in attrs:
    data = data.query(a + ' != "(VOL) Don\'t Know/Refused"')

# process class into two categories
data['q87'] = data['q87'].str.replace('Excellent shape', 'good')
data['q87'] = data['q87'].str.replace('Good shape', 'good')
data['q87'] = data['q87'].str.replace('Only fair shape', 'bad')
data['q87'] = data['q87'].str.replace('Poor shape', 'bad')
data.to_csv('aa.csv')

total_examples = data.shape[0]
training_set_size = int(total_examples * 0.85)

df_train = data[:training_set_size]
df_test = data[training_set_size:]

dataframe_to_arff(df_train, 'aa_train.arff', [], 'aa_train')
dataframe_to_arff(df_test, 'aa_test.arff', [], 'aa_test')
