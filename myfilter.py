import mysql


def filter_imgurl(rootComics_mainIndex,src_arrary_img_url):
    set_arrary_imgurl_data = mysql.getData('url', 'comics', 'path_name', rootComics_mainIndex)
    subset_arrary_imgurl_data = set(set_arrary_imgurl_data)
    result = [url for url in src_arrary_img_url if url.get_attribute('data-original') not in set_arrary_imgurl_data]
    copy_result = result.copy()
    for index,item in enumerate(result, start=0) :
        if item.get_attribute('id') == None:
            copy_result.remove(item)
    return copy_result
def filter_Path(pathUrl_arrary):
    path_arrary = []
    result =[]
    for item in pathUrl_arrary:
        strarrary = item.split('https://18comic.org/photo/')
        path_arrary.append(strarrary[len(strarrary) - 1])
        
    strarrary = pathUrl_arrary[0].split('https://18comic.org/photo/')
    path = strarrary[len(strarrary)-1]
    rootComics_id = mysql.getData('rootComics_id', 'comics', 'path_name', path)
    if len(rootComics_id) == 0:
        return pathUrl_arrary
    data_path_arrary = mysql.getData('path_name', 'comics', 'rootComics_id', rootComics_id[0])

    subset_arrary_imgurl_data = set(data_path_arrary)
    result = [path for path in path_arrary if path not in data_path_arrary]
    return result

    

