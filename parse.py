import csv

def remove_commas(s):
  return str(s).replace(',', '')

def wrap_in_quotes(s):
  return '"{0}"'.format(s)

def dataframe2arff(dataframe, filename, coltypes, relation, include_index=False):
    dataframe = dataframe.applymap(remove_commas)
    if include_index:
        dataframe = dataframe.reset_index()
        
    with open(filename, 'w') as f:
        f.write('@relation {}\n'.format(relation))
        
        for column in dataframe:
            attrtype = 'nominal'
            # TODO input validation
            if attrtype == 'numeric':
                f.write('@attribute {} numeric\n'.format(column))
            elif attrtype == 'string':
                f.write('@attribute {} string\n'.format(column))
            elif attrtype == 'nominal':
                levels = dataframe[column].unique()
                set_notation = '{' + ','.join('"{0}"'.format(w) for w in map(str, levels)) + '}'
                f.write('@attribute {} {}\n'.format(column, set_notation))
            else:
                pass
                # TODO raise a stink

        f.write('@data\n')
        dataframe = dataframe.applymap(wrap_in_quotes)
        dataframe.to_csv(f, header=False, index=False, quoting=csv.QUOTE_NONE)

import pandas
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz

data = pandas.io.stata.read_stata('data/aa.dta')
## politics
# attrs = ['asnidone', 'sex', 'cdivision', 'q24', 'q30', 'birth_coded', 'pvote08a']
# attrs = ['q12b', 'q24', 'q33', 'q82', 'q83', 'party']
# attrs = ['asnidone', 'cdivision', 'q24', 'q30', 'birth_coded', 'usgen', 'pvote08a', 'party', 'educ', 'income']
# attrs = ['asnidone', 'q24', 'q30', 'usgen', 'educ', 'income', 'party']

## qol
attrs = ['asnidone', 'educ', 'q21', 'q24', 'q80', 'q10', 'q87']

cols = [c for c in data.columns if c in attrs]
data = data[cols]

## politics
# data = data[pandas.notnull(data['pvote08a'])]
# data = data.query('party == "Republican" | party == "Democrat"')
# data = data.query('party == "Republican" | party == "Democrat" | party == "Independent"')
# data['party'] = data['party'].str.replace('Independent', 'Not Democrat')
# data['party'] = data['party'].str.replace('Republican', 'Not Democrat')
# data.replace({'Independent': 'Republican'}, regex=True)

## qol
for a in attrs:
    data = data.query(a + ' != "(VOL) Don\'t Know/Refused"')

data['q87'] = data['q87'].str.replace('Excellent shape', 'good')
data['q87'] = data['q87'].str.replace('Good shape', 'good')
data['q87'] = data['q87'].str.replace('Only fair shape', 'bad')
data['q87'] = data['q87'].str.replace('Poor shape', 'bad')
data.to_csv('aa.csv')

total_examples = data.shape[0]
training_set_size = int(total_examples * 0.85)

df_train = data[:training_set_size]
df_test = data[training_set_size:]

print df_train.shape
print df_test.shape

dataframe2arff(df_train, 'aa_train.arff', [], 'aa_train')
dataframe2arff(df_test, 'aa_test.arff', [], 'aa_test')
