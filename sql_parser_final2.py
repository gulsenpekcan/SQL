# -*- coding: utf-8 -*-

import re
from codecs import open


def preprocess_query(query):

    # r'' yapisinda tirnak isaretleri icerisine yazilan \ (backslash) isaretleri yorumlanmaz
    # query'deki /*******/, /* comments */ yapilarini kaldirmak icin kullanilir
    query = re.sub(r'/\*.*?\*/', r'', query, flags = re.DOTALL)
    # query'deki -- ile başlayan satirlari siler
    # query = re.sub(r'(?m)^[\s]*\-.*\n?', r'', query)
    # v_message icerigi lazim olmadigi icin o satirlari kaldiriyoruz ki gereksiz tablo isimlerini bulmayalim
    query = re.sub(r'(?m)^[\s]*v_message.*\n?', r'', query)
    # verilen query icerisindeki .,:;()=- karakterleri yerine bosluk koyar
    query = re.sub(r'[.:;()=-]', r' ', query)
    # verilen query icerisindeki , karakterlerini önceki kelimeden ayirir
    query = re.sub(r',', r' ,', query)
    # query'de '|.....|' (pipe) karakterleri arasinda kalanlari kaldirir
    query = re.sub(r'\'[\s]*\|.*?\|[\s]*\'', r' ', query)
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
    indices_insert = []
    indices_select = []

    if 'common_variable_proc_id' in tokens:
        func_name = tokens[tokens.index('common_variable_proc_id') + 1]
    else:
        indx = tokens.index('FUNCTION')
        func_name = tokens[indx + 2]
    
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
        elif tokens[i] == 'INSERT':
            indices_insert.append(i)
        elif tokens[i] == 'select':
            indices_select.append(i)
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
        i = 1
        if tokens[j+3] == ',' and tokens[j+1].lower() != 'select' and tokens[j+4].lower() != 'select':
            while tokens[j+2+i] == ',':
                if tokens[j+i][:1] != "_" and tokens[j+i][:1] != "(" and "_" in tokens[j+i] \
                    and "temp_" not in tokens[j+i]:
                        tb_names.append(tokens[j+i])
                else:
                    pass
                i += 3
            if tokens[j+i][:1] != "_" and tokens[j+i][:1] != "(" and "_" in tokens[j+i] \
                    and "temp_" not in tokens[j+i] and tokens[j+2] != "and":
                        tb_names.append(tokens[j+i])
        elif tokens[j+1][:1] != "_" and tokens[j+1][:1] != "(" and "_" in tokens[j+1] \
            and "temp_" not in tokens[j+1] and tokens[j+2] != "and":
                tb_names.append(tokens[j+1])
        else:
            pass
                
        
    for j in indices_insert:
        if tokens[j+2][:1] != "_" and tokens[j+2][:1] != "(" and "_" in tokens[j+2] \
            and "temp_" not in tokens[j+2] and tokens[j+1] == "INTO":
            tb_names.append(tokens[j+2])
        else:
            pass
 
    for j in indices_select:
        if tokens[j+1][:6] != "common" and tokens[j+2] == "_":
            tb_names.append(tokens[j+1])
        else:
            pass


    for j in indices_with:
        if tokens[j+1] in tb_names:
            tb_names.remove(tokens[j+1])
        elif tokens[j+2] in tb_names:
            tb_names.remove(tokens[j+2])
        else:
            pass

    for j in indices_as:
        if tokens[j-1] in tb_names:
            tb_names.remove(tokens[j-1])
        else:
            pass


    # tablodaki elemanlarin tekligi kesinlestirilir
    tb_names = list(set(tb_names))

    _indices = [i for i in range(len(func_name)) if func_name[i] == '_']
    func_name = func_name[_indices[0]+1:_indices[-1]]
    
    for table_name in tb_names:
        table_name_split = table_name.split('_')
        if "pre" in table_name_split:
            tb_name_pre_split = table_name.split("pre_")
            if func_name in tb_name_pre_split:
                tb_names.remove(table_name)
        else:
            pass
        
    return tb_names


if __name__ == '__main__':

    # sql uzantili dosya okunup string olarak alinir
    sqlfile = "C:/Users/gulsen.pekcan/Downloads/trn_usage_summary_proc_create_script.sql"
    sql_query = open(sqlfile, mode='r', encoding='utf-8-sig').read()
    
    # string uzerinde on isleme gerceklestirilir
    sql_query = preprocess_query(sql_query)

    # okunan sql uzantili dosyadaki tablo isimleri alinir
    names = []
    names = get_tables_names(sql_query)

    print("*******************************************************************")
    print( names)
    print("*******************************************************************")
