import mysql

# here is get sql data to check it's existed it will remove duplicate data
def filter_imgurl(rootComics_mainIndex,src_arrary):
    set_arrary_data = mysql.getData('target_row_name', 'tablename', 'where_row_name', 'where_row_value')
    subset_arrary_data = set(set_arrary_data)
    result = [url for url in src_arrary if url not in set_arrary_data]
    copy_result = result.copy()
    # here is remove duplicate data
    for index,item in enumerate(result, start=0) :
        if item.get_attribute('id') == None:
            copy_result.remove(item)
    return copy_result
