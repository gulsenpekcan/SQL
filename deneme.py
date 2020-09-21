
import ParserModule as pm

if __name__ == '__main__':
    
    elements = []
    with open ("C:/Users/gulsen.pekcan/Downloads/fact_dvr_change.sql", mode='r', encoding='utf-8-sig') as sql_file:
        sql_query = sql_file.read()
        
    elements = sql_query.split(";")
    
    scripts = []
    for element in elements:
        if "v_script:=" in element:
            element = element.split("v_script:=", 1)[1]
            scripts.append(element.strip("' "))
       
        elif "v_script :=" in element:
            element = element.split("v_script :=", 1)[1]
            scripts.append(element.strip("' "))
        elif "select" in element:
            scripts.append(element)
        
    scripts = list(map(lambda x: pm.preprocess_query(x), scripts))
    
    tb_names = []
    for i in range(len(scripts)):
        tb_names = tb_names + pm.sql_parse(scripts[i])
        
    tb_names = list(set(tb_names))
    
    #scripts = list(map(lambda x: pm.sql_tokens(x), scripts))
    
    
    