
import re


def preprocess_query(query):

    # r'' yapisinda tirnak isaretleri icerisine yazilan \ (backslash) isaretleri yorumlanmaz
    # v_message icerigi lazim olmadigi icin o satirlari kaldiriyoruz ki gereksiz tablo isimlerini bulmayalim
    query = re.sub(r'(?m)^[\s]*v_message.*\n?', r'', query)
    # verilen query icerisindeki .,:;()=- karakterleri yerine bosluk koyar
    query = re.sub(r'[.:;()=-]', r' ', query)
    # verilen query icerisindeki , karakterlerini önceki kelimeden ayirir
    query = re.sub(r',', r' , ', query)
    # query'de '|.....|' (pipe) karakterleri arasinda kalanlari kaldirir
    query = re.sub(r'\'[\s]*\|.*?\|[\s]*\'', r' ', query)
    # query'deki ' karakterlerinin yerine bosluk koyar
    query = re.sub(r'[\']+', r'', query)
    # satir atlama kisimlarini bosluk ile degistirir
    query = query.replace('\n', ' ')

    return query


def sql_parse(query):
    # query'i bosluk karakterinden tokenlara ayirir
    tokens = re.split(r"[\s]+", query)
    
    indices_join = []
    indices_from = []
    indices_with = []
    indices_as = []
    indices_insert = []
    indices_select = []
    
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
        try:
            if tokens[j+3] == ',' and tokens[j+1].lower() != 'select' and tokens[j+4].lower() != 'select':
                while tokens[j+2+i] == ',':
                    if tokens[j+i][:1] != "_" and tokens[j+i][:1] != "(" and tokens[j+i][:1] != "|" and "_" in tokens[j+i] \
                        and "temp_" not in tokens[j+i]:
                            tb_names.append(tokens[j+i])
                    else:
                        pass
                    i += 3
                if tokens[j+i][:1] != "_" and tokens[j+i][:1] != "(" and tokens[j+i][:1] != "|" and "_" in tokens[j+i] \
                        and "temp_" not in tokens[j+i] and tokens[j+2] != "and":
                            tb_names.append(tokens[j+i])
            elif tokens[j+1][:1] != "_" and tokens[j+1][:1] != "(" and tokens[j+1][:1] != "|" and "_" in tokens[j+1] \
               and "temp_" not in tokens[j+1]:
                   tb_names.append(tokens[j+1])
                        
        except:
            try:
                if tokens[j+1][:1] != "_" and tokens[j+1][:1] != "(" and tokens[j+1][:1] != "|" and "_" in tokens[j+1] \
                   and "temp_" not in tokens[j+1]:
                       tb_names.append(tokens[j+1])
            except:
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


    
    for table_name in tb_names:
        table_name_split = table_name.split('_')
        if "pre" in table_name_split:
            tb_names.remove(table_name)
        else:
            pass
        
    return tb_names



def sql_tokens(query):
    tokens = re.split(r"[\s]+", query)
    
    return tokens







