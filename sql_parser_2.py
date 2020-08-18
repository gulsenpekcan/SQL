# -*- coding: utf-8 -*-

import re
from codecs import open


def preprocess_query(query):

    # r'' yapisinda tirnak isaretleri icerisine yazilan \ (backslash) isaretleri yorumlanmaz
    # satir atlama kisimlarini bosluk ile degistirir
    query = query.replace('\n', ' ')
    # verilen query icerisindeki .,:;=()- karakterlerini siler
    query = re.sub(r'[.,:;=()-]', '', query)
    # query'de yan yana 1 veya daha fazla bulunan | (pipe) karakterini kaldirir 
    query = re.sub(r'[|]+', r'', query)
    # query'deki ' karakterlerinin yerine bosluk koyar
    query = re.sub(r'[\']+', r' ', query)
    # query'deki /*******/, /* comments */ yapilarini kaldirmak icin kullanilir
    query = re.sub(r'/\*.*?\*/', r'', query, flags = re.DOTALL)

    return query

def get_tables_names(query):

    # query'i bosluk karakterinden tokenlara ayirir
    tokens = re.split(r"[\s]+", query)

    indices_join = []
    indices_from = []
    
    for i in range(len(tokens)):
        if tokens[i] == 'JOIN' or tokens[i] == 'join':
            indices_join.append(i)
        elif tokens[i] == 'FROM' or tokens[i] == 'from':
            indices_from.append(i)

    # tokenlarin icerisinden tablo isimlerini cekmeye yarayan bloklar
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
    
    # tablodaki elemanlarin tekligi kesinlestirilir
    tb_names = list(set(tb_names))

    return tb_names

if __name__ == '__main__':

    # sql uzantili dosya okunup string olarak alinir
    sqlfile = "C:/Users/gulsen.pekcan/Downloads/asset.sql"
    sql_query = open(sqlfile, mode='r', encoding='utf-8-sig').read()
    
    # string uzerinde on isleme gerceklestirilir
    sql_query = preprocess_query(sql_query)
    
    # okunan sql uzantili dosyadaki tablo isimleri alinir
    names = []
    names = get_tables_names(sql_query)

    print("*******************************************************************")
    print( names)
    print("*******************************************************************")

    