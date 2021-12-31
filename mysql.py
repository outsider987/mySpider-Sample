import pymysql
from pymysql.converters import escape_string

# data base setting
# db_settings = {
#     "host": "156.67.222.43",
#     "port": 3306,
#     "user": "u565698326_Comics987",
#     "password": "T5204t5204",
#     "db": "u565698326_Comics",
#     "charset": "utf8",
#     "autocommit": True
# }
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "db": "comics",
    "charset": "utf8",
    "autocommit": True
}

# sample create table and inser data


def storeRootComicsData(descr, link, title, author, status, thumbnail_url):
    try:
        # build Connection object
        conn = pymysql.connect(**db_settings)
        # build Cursor object
        with conn.cursor() as cursor:
            # check we had table if we don't then create
            checkTableCommand = "CREATE TABLE IF NOT EXISTS rouman_rootcomics (id INT(11) NOT NULL AUTO_INCREMENT, descr varchar(300),link varchar(300),title varchar(300),author varchar(600),status varchar(600),thumbnail_url varchar(600) NOT NULL,PRIMARY KEY (id) )ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"
            cursor.execute(checkTableCommand)
            # insert data
            command = "INSERT  INTO rouman_rootcomics (descr,link, title,author, status,thumbnail_url) SELECT '%s','%s','%s','%s','%s','%s'  WHERE NOT EXISTS (SELECT * FROM rouman_rootcomics WHERE title = '%s' )" % (
                descr, link, title, author, status, thumbnail_url, title)

            # apply command
            cursor.execute(command)

    except Exception as ex:
        print(ex)
        print("storeRootComicsData had error:\n" + command)


def storeGenreData(rouman_rootcomics_id, name):
    try:
        # build Connection object
        conn = pymysql.connect(**db_settings)
        # build Cursor object
        with conn.cursor() as cursor:
            # check we had table if we don't then create
            checkTableCommand = "CREATE TABLE IF NOT EXISTS rouman_genre (id INT(11) NOT NULL AUTO_INCREMENT, rouman_rootcomics_id int,name varchar(300),PRIMARY KEY (id),FOREIGN KEY(rouman_rootcomics_id) REFERENCES rouman_rootcomics(id) ON UPDATE CASCADE ON DELETE NO ACTION )ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"
            cursor.execute(checkTableCommand)

            # insert data
            command = "INSERT INTO rouman_genre (rouman_rootcomics_id,name) select '%s','%s' where not exists (select * from rouman_genre where  rouman_rootcomics_id = %s and name ='%s' )" % (
                rouman_rootcomics_id, name, rouman_rootcomics_id, name)

            # apply command
            cursor.execute(command)

    except Exception as ex:
        print(ex)
        print("storeRootComicsData had error:\n" + command)


def storeComicsData(rouman_rootcomics_id, url_arrary, chapter):
    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            # check we had table if we don't then create
            checkTableCommand = "CREATE TABLE IF NOT EXISTS rouman_comics (id INT(11) NOT NULL AUTO_INCREMENT, rouman_rootcomics_id INT not null,chapter varchar(300),url varchar(600) NOT NULL,PRIMARY KEY (id),FOREIGN KEY(rouman_rootcomics_id) REFERENCES rouman_rootcomics(id) ON UPDATE CASCADE ON DELETE NO ACTION  )ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"
            cursor.execute(checkTableCommand)
            # insert data
            Values = "VALUES "
            for index, page_num in enumerate(url_arrary, start=0):
                value = "("

                img_url = url_arrary[index]

                value = value + "'%s'" % (img_url) + ","  \
                    + str(rouman_rootcomics_id) + ","+str(chapter)
                if len(url_arrary) - 1 == index:
                    value = value + ")"
                else:
                    value = value + "),"
                Values += value
            # command = "INSERT IGNORE INTO comics (name, url,path_name,onCanvas,rootComics_id) " + Values
            command = "INSERT IGNORE  INTO rouman_comics (url,rouman_rootcomics_id, chapter) " + \
                Values + "ON DUPLICATE KEY UPDATE  url = VALUES(url)"

            cursor.execute(command)
            # # 取得所有資料
            result_set = cursor.fetchall()
            print(result_set)
    except Exception as ex:
        print(ex)

# sql to get data


def getData(target_row_name, tablename, where_row_name, where_row_value):

    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            geturl_name_command = "SELECT %s FROM  %s where %s ='%s'" % (
                target_row_name, tablename, where_row_name, where_row_value)
            print(geturl_name_command)
            cursor.execute(geturl_name_command)
            # convert to arrary
            results = [res[0] for res in cursor.fetchall()]
            print("Gett Sql data sucess:" + target_row_name)
            return results
    except Exception as e:
        print(e)
        null = []
        return null
