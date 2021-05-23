import pymysql
from pymysql.converters import escape_string

# data base setting
db_settings = {
    "host": "156.67.222.43",
    "port": 3306,
    "user": "u565698326_Comics987",
    "password": "T5204t5204",
    "db": "u565698326_Comics",
    "charset": "utf8",
    "autocommit": True
}
# db_settings = {
#     "host": "127.0.0.1",
#     "port": 3306,
#     "user": "root",
#     "password": "password",
#     "db": "Comics",
#     "charset": "utf8",
#     "autocommit": True
# }


def storeRootComicsData(mainIndex_name, mainIndex, descr, link, title, thumbnail_name,thumbnail_url):
    try:
    # 建立Connection物件
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # check we had table if we don't then create 
            checkTableCommand = "CREATE TABLE IF NOT EXISTS rootComics (id INT(11) NOT NULL AUTO_INCREMENT,mainIndex INT(11) NOT NULL,mainIndex_name varchar(30) NOT NULL , descr varchar(300),link varchar(300),title varchar(20), thumbnail_name varchar(300) NOT NULL,thumbnail_url varchar(600) NOT NULL,PRIMARY KEY (id) )ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"
            cursor.execute(checkTableCommand)

            result1 = cursor.fetchall()
            print(result1)
            # insert data
            command = "INSERT INTO rootComics (mainIndex, mainIndex_name,descr,link, title,thumbnail_name,thumbnail_url) SELECT %s,'%s','%s','%s','%s','%s','%s' WHERE NOT EXISTS (SELECT * FROM rootComics WHERE mainIndex = %s )" % (mainIndex, mainIndex_name, descr, link, title, thumbnail_name, thumbnail_url,mainIndex)
            # 執行指令
            
            cursor.execute(command)
             
            updateurl_command = "UPDATE rootComics set thumbnail_url = '%s' WHERE mainIndex = '%s'" % (thumbnail_url,mainIndex)
            cursor.execute(updateurl_command)
            # 取得所有資料
            result2 = cursor.fetchall()
            print(result2)

    except Exception as ex:
        print(ex)
        print("storeRootComicsData had error:\n" + command)


def storeComics(page_num_Arrary, img_url_Arrary , path_Array, canvasExist_Arrary, comicMainIndexNumData):
    try:
    # 建立Connection物件
        # descr = "test"
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # check we had table if we don't then create 
            checkTableCommand = "CREATE TABLE IF NOT EXISTS comics (id INT(11) NOT NULL AUTO_INCREMENT,rootComics_id INT(11) NOT NULL,name varchar(30) NOT NULL ,  url varchar(300)  NOT NULL,path_name varchar(30) NOT NULL,onCanvas boolean DEFAULT FALSE,createTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,lastUpdateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (id) ,unique(url),FOREIGN KEY(rootComics_id) REFERENCES rootComics(id) ON UPDATE CASCADE ON DELETE NO ACTION )ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"
            cursor.execute(checkTableCommand)
            # test
            # Values = "VALUES "
            # for index, page_num in enumerate(page_num_Arrary, start=0):
            #     value = "("
            #     img_url = img_url_Arrary[index]
            #     path = path_Array[index]
            #     canvasExist = canvasExist_Arrary[index]
            #     rootComics_id = "(select id from rootComics where  mainIndex='%s')" % comicMainIndexNumData
            #     value = value + "'%s','%s'" % (page_num, img_url) + "," + path + "," + str(canvasExist) + "," + rootComics_id
            #     if 2 == index:
            #         value = value + ")"
            #         Values += value
            #         break
            #     else:
            #         value = value + "),"
            #         Values += value
                    
            #     Values += value
            # command2 = "INSERT IGNORE INTO comics (name, url,path_name,onCanvas,rootComics_id) " + Values 
            # result1 = cursor.fetchall()
            # print(result1)
            # # insert data
            # command = "INSERT INTO comics (name, url,path_name,onCanvas,rootComics_id) SELECT '%s','%s','%s','%s',(select id from rootComics where  mainIndex = '%s' ) WHERE NOT EXISTS (SELECT * FROM comics WHERE url = '%s' )" % (name, url, path_name, onCanvas, comicMainIndexNumData, url)
            # # 執行指令
            Values = "VALUES "
            for index, page_num in enumerate(page_num_Arrary, start=0):
                value = "("
               
                img_url = img_url_Arrary[index]
                path = path_Array[index]
                canvasExist = canvasExist_Arrary[index]
                rootComics_id = "(select id from rootComics where  mainIndex='%s')" % comicMainIndexNumData
                value = value + "'%s','%s'" % (page_num, img_url) + "," + path + "," + str(canvasExist) + "," + rootComics_id
                if len(page_num_Arrary) - 1 == index:
                    value = value + ")"
                else:
                    value = value + "),"
                Values += value
            # command = "INSERT IGNORE INTO comics (name, url,path_name,onCanvas,rootComics_id) " + Values 
            command = "INSERT IGNORE  INTO comics (name, url,path_name,onCanvas,rootComics_id) " + Values +"ON DUPLICATE KEY UPDATE url = VALUES(url)"
            cursor.execute(command)
            # # 取得所有資料
            result_set = cursor.fetchall()
            print(result_set)

    except Exception as ex:
        print(ex)
        print("storeComics had error:\n" + command)


def storeGenre(genre, mainIndex):
    try:
    # 建立Connection物件
        # descr = "test"
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # check we had table if we don't then create 
            checkTableCommand = "CREATE TABLE IF NOT EXISTS genre (id INT(11) NOT NULL AUTO_INCREMENT,rootComics_id INT(11) NOT NULL,name varchar(30) DEFAULT NULL , PRIMARY KEY (id) ,FOREIGN KEY(rootComics_id) REFERENCES rootComics(id) ON UPDATE CASCADE ON DELETE NO ACTION )ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"
            cursor.execute(checkTableCommand)

            result1 = cursor.fetchall()
            print(result1)
            # # insert data
            command = "INSERT INTO genre (name,rootComics_id) SELECT '%s',(select id from rootComics where mainIndex = %s) WHERE NOT EXISTS (SELECT * FROM genre WHERE name ='%s' )" % (genre, mainIndex, genre)
            # # 執行指令
            
            cursor.execute(command)
            # # 取得所有資料
            result2 = cursor.fetchall()
            print(result2)

    except Exception as ex:
        print(ex)
        print("storeGenre had error:\n" + command)


def storeAuthor(author, mainIndex):
    try:
    # 建立Connection物件
        # descr = "test"
        conn = pymysql.connect(**db_settings)
        # 建立Cursor物件
        with conn.cursor() as cursor:
            # check we had table if we don't then create 
            checkTableCommand = "CREATE TABLE IF NOT EXISTS author (id INT(11) NOT NULL AUTO_INCREMENT,rootComics_id INT(11) NOT NULL,name varchar(30) NOT NULL , PRIMARY KEY (id) ,FOREIGN KEY(rootComics_id) REFERENCES rootComics(id) ON UPDATE CASCADE ON DELETE NO ACTION )ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"
            cursor.execute(checkTableCommand)

            result1 = cursor.fetchall()
            print(result1)
            # # insert data
            command = "INSERT INTO author (name,rootComics_id) SELECT '%s',(select id from rootComics where mainIndex = '%s') WHERE NOT EXISTS (SELECT * FROM author WHERE name = '%s' )" % (author, mainIndex, author)
            # # 執行指令
            
            cursor.execute(command)
            # # 取得所有資料
            result2 = cursor.fetchall()
            print(result2)

    except Exception as ex:
        print(ex)
        print("storeAuthor had error:\n" + command)

def getData(target_row_name, tablename, where_row_name, where_row_value):
    
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            geturl_name_command = "SELECT %s FROM  %s where %s = %s" % (target_row_name, tablename,where_row_name,where_row_value) 
            print(geturl_name_command)
            cursor.execute(geturl_name_command)
            # convert to arrary
            results = [res[0] for res in cursor.fetchall()]
            print("Gett Sql data sucess:"+ target_row_name)
            return  results
    except Exception as e:
        print(e)
        null = []
        return null
   
