# -*- coding: utf-8 -*-

import re 


def preprocess_query(query):

    query = query.replace('\n', ' ')
    query = re.sub(r'[|]+', r'', query)
    query = re.sub(r'[\']+', r' ', query)
    #query = re.sub(r'^.*?(?=\s(JOIN))', r'', query)

    return query


def get_tables_names(query):
    
    tokens = re.split(r"[\s)(;]+", query)
     
    print(tokens)
    
    indices = []
    
    for i in range(len(tokens)):
        if tokens[i] == 'JOIN' or tokens[i] == 'join':
            indices.append(i)
    
        
    print(indices)
    
    tb_names = []
    for j in indices:
        tb_names.append(tokens[j+2])
        
        
    return tb_names

if __name__ == '__main__':
    query1 = preprocess_query("FROM  '||v_dwh_owner||v_temp_tab_prefix||'_9 tmp LEFT OUTER JOIN "\
                  "'||v_dwh_stg_owner||'stg_dce_prod_ofr po on tmp.prod_ofr_id=po.prod_ofr_id "\
    		"left outer join '||v_dwh_stg_owner||'stg_dce_gnl_tp gt on po.cntnt_tp_id=gt.gnl_tp_id'")
        
    query = preprocess_query("FROM  '||v_dwh_owner||v_temp_tab_prefix||'_18 tmp18 LEFT OUTER JOIN " \
                    "'||v_dwh_stg_owner||'stg_dce_prod_spec_fmly_prod_spec sdpsfps on tmp18.prod_spec_id = sdpsfps.prod_spec_id " \
    "left outer join '||v_dwh_stg_owner||'stg_dce_prod_spec_fmly_subcatg sdpsfs on sdpsfps.prod_spec_fmly_subcatg_id = sdpsfs.prod_spec_fmly_subcatg_id " \
    "left outer join '||v_dwh_stg_owner||'stg_dce_prod_spec_fmly_catg sdpsfc on sdpsfc.prod_spec_fmly_catg_id = sdpsfs.prod_spec_fmly_catg_id " \
    "left outer join '||v_dwh_stg_owner||'stg_dce_prod_spec_fmly sdpsf on sdpsf.prod_spec_fmly_id = sdpsfc.prod_spec_fmly_id " \
    "left outer join '||v_dwh_stg_owner||'stg_dce_prod_spec_fmly_lang sdpsfl on sdpsfl.prod_spec_fmly_id = sdpsf.prod_spec_fmly_id '")
        
    #print("query: " + query)
    
    names = []
    
    names = get_tables_names(query)
    
    print("*******************")
    
    print( names)
    
  
    
        
        