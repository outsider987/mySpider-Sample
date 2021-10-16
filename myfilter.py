import mysql

# here is get sql data to check it's existed it will remove duplicate data


def filter_chapter(rouman_rootcomics_id, chapter_arrary):
    set_arrary_data = mysql.getData(
        'chapter', 'rouman_comics', 'rouman_rootcomics_id', rouman_rootcomics_id)
    subset_arrary_data = set(set_arrary_data)
    if len(subset_arrary_data) == 0:
        return chapter_arrary,0
    Existresult = [url for url in range(
        len(chapter_arrary)) if url in set_arrary_data]
    chapter = len(Existresult) 
    del chapter_arrary[0:len(Existresult)]
    # copy_result = result.copy()
    # here is remove duplicate data
    # for index, item in enumerate(result, start=0):
    #     if item.get_attribute('id') == None:
    #         copy_result.remove(item)
    return chapter_arrary,chapter
