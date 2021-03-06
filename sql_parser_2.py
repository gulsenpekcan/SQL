# -*- coding: utf-8 -*-

import re
from codecs import open


def preprocess_query(query):

    # r'' yapisinda tirnak isaretleri icerisine yazilan \ (backslash) isaretleri yorumlanmaz
    # query'deki /*******/, /* comments */ yapilarini kaldirmak icin kullanilir
    query = re.sub(r'/\*.*?\*/', r'', query, flags = re.DOTALL)
    # query'deki -- ile başlayan satirlari siler
    query = re.sub(r'(?m)^[\s]*\-.*\n?', r'', query)
    # v_message icerigi lazim olmadigi icin o satirlari kaldiriyoruz ki gereksiz tablo isimlerini bulmayalim
    query = re.sub(r'(?m)^[\s]*v_message.*\n?', r'', query)
    # verilen query icerisindeki .,:;()=- karakterleri yerine bosluk koyar
    query = re.sub(r'[.,:;()=-]', r' ', query)
    # query'de '|.....|' (pipe) karakterleri arasinda kalanlari kaldirir
    query = re.sub(r'\'[\s]*\|.*?\|[\s]*\'', r'', query)
    # query'deki ' karakterlerinin yerine bosluk koyar
    query = re.sub(r'[\']+', r'', query)
    # satir atlama kisimlarini bosluk ile degistirir
    query = query.replace('\n', ' ')

    return query

def get_tables_names(query):

    # query'i bosluk karakterinden tokenlara ayirir
    tokens = re.split(r"[\s]+", query)

    indices_join = []
    indices_from = []
    indices_with = []
    indices_as = []

    for i in range(len(tokens)):
        if tokens[i] == 'JOIN' or tokens[i] == 'join':
            indices_join.append(i)
        elif tokens[i] == 'FROM' or tokens[i] == 'from':
            indices_from.append(i)
        elif tokens[i] == 'WITH' or tokens[i] == 'with':
            for k in range(i, i+20):
                indices_with.append(i)
                if tokens[k] == 'AS' or tokens[k] == 'as':
                    indices_as.append(k)
                else:
                    pass
        else:
            pass


    # tokenlarin icerisinden tablo isimlerini cekmeye yarayan bloklar
    tb_names = []
    for j in indices_join:
        if tokens[j+1][:1] != "_" and tokens[j+1][:1] != "(" and "_" in tokens[j+1] \
            and "temp_" not in tokens[j+1]:
            tb_names.append(tokens[j+1])
        else:
            pass

    for j in indices_from:
        if tokens[j+1][:1] != "_" and tokens[j+1][:1] != "(" and "_" in tokens[j+1] \
            and "temp_" not in tokens[j+1]:
            tb_names.append(tokens[j+1])
        else:
            pass

    for j in indices_with:
        if tokens[j+1] in tb_names:
            tb_names.remove(tokens[j+1])
        elif tokens[j+2] in tb_names:
            tb_names.remove(tokens[j+2])

    for j in indices_as:
        if tokens[j-1] in tb_names:
            tb_names.remove(tokens[j-1])

    # tablodaki elemanlarin tekligi kesinlestirilir
    tb_names = list(set(tb_names))

    return tb_names

if __name__ == '__main__':

    # sql uzantili dosya okunup string olarak alinir
    sqlfile = "C:/Users/gulsen.pekcan/Downloads/fact_dvr_change.sql"
    sql_query = open(sqlfile, mode='r', encoding='utf-8-sig').read()

    # string uzerinde on isleme gerceklestirilir
    sql_query = preprocess_query(sql_query)

    # okunan sql uzantili dosyadaki tablo isimleri alinir
    names = []
    names = get_tables_names(sql_query)

    print("*******************************************************************")
    print( names)
    print("*******************************************************************")

