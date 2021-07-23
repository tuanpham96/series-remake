import re
import numpy as np 
import pandas as pd 
import requests 
from bs4 import BeautifulSoup as bs

from imdb import IMDb
imdb_req = IMDb()
from functools import partial

def soup_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        print('Something wrong at %s, not processed' %(url))
        return None
    return bs(r.text, 'html.parser')

def process_wikitable(wiki_url, colrename_dict = None, dropcol_list = None, addcol_dict = None,
                      url_prefix = 'https://en.wikipedia.org', empty_url = 'NA', 
                      cols_only_proctxt = dict()):
    s = soup_url(wiki_url)
    if s is None:
        return None 
    tbl = s.find('table', {'class':"wikitable"})

    # https://github.com/pandas-dev/pandas/issues/13141 
    # https://stackoverflow.com/a/42285792
    data = [
        [dict(
            show = ''.join(td.stripped_strings), # text of cell
            wikiurl = url_prefix + td.a['href'] if td.find('a') else empty_url # first href in cell
        ) 
        for td in row.find_all('td')] 
        if row.find('td') else 
        [th.text.strip() for th in row.find_all('th')]
        for row in tbl.find_all('tr')]
    df = pd.DataFrame(data[1:], columns=data[0])

    if colrename_dict is not None:
        df.rename(columns = colrename_dict, inplace = True)

    if dropcol_list is not None:
        df.drop(columns=dropcol_list, inplace = True)

    if addcol_dict is not None:
        df = df.assign(**addcol_dict)
    else:
        addcol_dict = dict()

    df = pd.concat(
        [df[k] if k in addcol_dict 
         else pd.DataFrame(df[k].tolist()).add_prefix(k + '_')
        for k in df.columns], axis=1)
    
    for k in cols_only_proctxt: 
        df.drop(columns=k + '_wikiurl', inplace=True)
        df.rename(columns={k + '_show': k}, inplace=True)

    filter_nonemptyurl = ' and '.join(
        ['`%s` != @empty_url' %(s) 
        for s in list(df.columns) if 'wikiurl' in s])

    df.query(filter_nonemptyurl, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def imdbID_re_from_url(s):
    id = re.findall('\d+', s)
    return id[0] if len(id) > 0 else None

def imdburls_from_wiki(wiki_url):
    imdb_re_from_wiki = re.compile('^https:\/\/www\.imdb\.com\/title\/\w*\/$')
    s = soup_url(wiki_url)
    if s is None: return None
    imdb_urls = [x['href'] for x in s.find_all('a', href=imdb_re_from_wiki)]
    return set(imdb_urls)

def empty_val(r):
    if r is None: return True
    return len(r) == 0

def empty_row(row, fields):
    return any([empty_val(row[k]) for k in fields])

def filtout_rows(df, func, reset_index=False):
    toremove_rows = df.apply(func, axis=1)
    df = df[~(toremove_rows)]
    if reset_index:
        df = df.reset_index(drop=True)
    return df

def get_imdbinfo(imdb_urls, imdb_fields = ['title', 'imdbID', 'rating']):
    imdb_objs = [imdb_req.get_movie(imdbID_re_from_url(x)) for x in imdb_urls]
    imdb_objs = [x for x in imdb_objs if x is not None]
    imdb_vals = [{k: x.get(k) for k in imdb_fields} for x in imdb_objs if x is not None]
    return imdb_vals


