# -*- coding: utf-8 -*-

import re
from codecs import open


def preprocess_query(query):

    query = query.replace('\n', ' ')
    query = re.sub(r'[.,:;=()-]', '', query)
    query = re.sub(r'[|]+', r'', query)
    query = re.sub(r'[\']+', r' ', query)
    query = re.sub(r'/\*.*?\*/', r'', query, flags = re.DOTALL)

    return query

def get_tables_names(query):

    tokens = re.split(r"[\s)(;]+", query)

    indices_join = []
    indices_from = []
    

    for i in range(len(tokens)):
        if tokens[i] == 'JOIN' or tokens[i] == 'join':
            indices_join.append(i)
        elif tokens[i] == 'FROM' or tokens[i] == 'from':
            indices_from.append(i)

    tb_names = []
    for j in indices_join:
        if(tokens[j+2][:1] != "_"):
            tb_names.append(tokens[j+2])
        else:
            pass
        
    for j in indices_from:
        if(tokens[j+2][:1] != "_"):
            tb_names.append(tokens[j+2])
        else:
            pass
    
    tb_names = list(set(tb_names))

    return tb_names

if __name__ == '__main__':

    sqlfile = "C:/Users/gulsen.pekcan/Downloads/asset.sql"
    sql_query = open(sqlfile, mode='r', encoding='utf-8-sig').read()
    
    sql_query = preprocess_query(sql_query)
    
    names = []
    names = get_tables_names(sql_query)

    print("*******************************************************************")
    print( names)
    print("*******************************************************************")

    