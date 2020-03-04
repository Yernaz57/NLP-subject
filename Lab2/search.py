import os
from os.path import join, abspath, dirname
base_path = "D:\\anaconda\\"
os.environ['PATH'] = '%s%s' % (
    os.environ['PATH'],
    join(base_path, 'Library', 'bin'),
)


from search_engine_parser import YahooSearch, GoogleSearch, BingSearch
import pandas as pd
import pprint
import tqdm
from joblib import Parallel, delayed

gsearch = GoogleSearch()
ysearch = YahooSearch()
bsearch = BingSearch()


data = []
nouns_df = pd.read_csv('./data/training_data/synsets_nouns.tsv', sep='\t')
def gather(row):
    # pprint.pprint(row,indent=2)
    for word in row[1].split(","):
        datum = [row[0],word]
        search_args = ('что такое %s?'%word, 1)
        try:
            gres = gsearch.search(*search_args)
            yres = ysearch.search(*search_args)
            bres = bsearch.search(*search_args)
            a = [
                gres['titles'],
                gres['links'],
                gres['descriptions'],
                yres['titles'],
                yres['links'],
                yres['descriptions'],
                bres['titles'],
                bres['links'],
                bres['descriptions'],
            ]
            datum.extend(a)
        except Exception as e:
            a = [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ]
            datum.extend(a)
            print(e)


        data.append(datum)

print(len(data))
[gather(rrr) for rrr in tqdm.tqdm(nouns_df.values[1000:2000])]
# Parallel(n_jobs=-1,require='sharedmem')(delayed(gather)(rrr) for rrr in tqdm.tqdm(nouns_df.values[:30]))
# Parallel(n_jobs=-1,require='sharedmem')(delayed(gather)(rrr) for rrr in tqdm.tqdm(nouns_df.values))
print(len(data))

df = pd.DataFrame(data,columns=['SynsetID',
                           'CoHypo',
                           'GTitle',
                           'GUrls',
                           'GDescr',
                           'YTitle',
                           'YUrls',
                           'YDescr',
                           'BTitle',
                           'BUrls',
                           'BDescr'])

df.to_csv('internet2000.csv')
df.to_csv('internet2000.pickle')