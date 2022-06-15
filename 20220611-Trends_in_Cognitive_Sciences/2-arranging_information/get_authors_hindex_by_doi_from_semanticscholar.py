
import json
import pandas as pd
import requests
import time
import random

def get_doi_authors(doi, url_paper = 'https://api.semanticscholar.org/graph/v1/paper'):
    time.sleep(random.random() * 4)
    response = requests.get(
        url = 'https://api.semanticscholar.org/graph/v1/paper/' + doi, 
        params = {"fields": "citationCount,influentialCitationCount,authors.name,authors.paperCount,authors.citationCount,authors.hIndex"},
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',}
        )
    authors_json = response.text
    doi_authors = json.loads(authors_json)
    doi_authors['doi'] = doi
    doi_authors_json = json.dumps(doi_authors)
    return doi_authors_json

def doi_authors_json2df(doi_authors_json):
    df = pd.read_json(doi_authors_json)
    # https://stackoverflow.com/questions/38231591/split-explode-a-column-of-dictionaries-into-separate-columns-with-pandas
    df2 = pd.concat([df.drop(['authors'], axis = 1), pd.json_normalize(df['authors'])], axis = 1)
    return df2

def main():
    # 1. 获得 doi 列表
    # opening the file in read mode
    doi_file = open("TiCS_doi.txt", "r")
    # reading the file
    data = doi_file.read()
    # replacing end splitting the text 
    # when newline ('\n') is seen.
    dois = data.split("\n")
    # dois = ['10.1146/annurev.psych.58.110405.085709', '1']
    # print(dois)
    
    # 2. 获得 doi_authors
    out_file = open("TiCS_doi_with_authors_hindex_from_semanticscholar.json", mode='w', encoding='utf8')
    for doi in dois:
        try:
            js = get_doi_authors(doi)
            print(js + "\n")
            out_file.write(js + "\n")
        except:
            print("Exception!")
    
    out_file.close()
    

def main2():
    in_file = open("TiCS_doi_with_authors_hindex_from_semanticscholar.json", mode='r', encoding='utf8')

    dfs = [] # 空的 dataframe
    while True:
        js = in_file.readline()
        if not js:
            break
        
        # 因为缺失 authorId 的情况很常见，而且会报异常。
        # TODO 解决方案
        if js.find('"authorId":') == -1:
            continue
        try:
            # print(js + "\n")
            dfs.append(doi_authors_json2df(js))
        except:
            print(js)
            print("Exception!")

    # union 所有 dfs
    all_doi_authors_df = pd.concat(dfs)
    
    # 3. 输出
    # print(all_doi_authors_df[['paperId', 'doi']])
    all_doi_authors_path = "TiCS_doi_with_authors_hindex_from_semanticscholar.csv"
    all_doi_authors_df.to_csv(all_doi_authors_path, index=False)
    

if __name__ == '__main__':
    main2()