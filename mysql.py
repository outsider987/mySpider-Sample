import pymysql
from pymysql.converters import escape_string

# data base setting
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "password",
    "db": "Comics",
    "charset": "utf8",
    "autocommit": True
}

# sample create table and inser data


def storeRootComicsData(descr, link, title, thumbnail_url):
    try:
        # build Connection object
        conn = pymysql.connect(**db_settings)
        # build Cursor object
        with conn.cursor() as cursor:
            # check we had table if we don't then create
            checkTableCommand = "CREATE TABLE IF NOT EXISTS rouman_rootComics (id INT(11) NOT NULL AUTO_INCREMENT, descr varchar(300),link varchar(300),title varchar(20),thumbnail_url varchar(600) NOT NULL,PRIMARY KEY (id) )ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC"
            cursor.execute(checkTableCommand)
            # insert data
            command = "INSERT INTO rootComics (descr,link, title,thumbnail_url) SELECT '%s','%s','%s',,'%s' WHERE NOT EXISTS (SELECT * FROM rootComics WHERE  = %s )" % (
                descr, link, title, thumbnail_url, title)
            # apply command
            cursor.execute(command)

    except Exception as ex:
        print(ex)
        print("storeRootComicsData had error:\n" + command)

# sql to get data


def getData(target_row_name, tablename, where_row_name, where_row_value):

    try:
        conn = pymysql.connect(**db_settings)
        with conn.cursor() as cursor:
            geturl_name_command = "SELECT %s FROM  %s where %s = %s" % (
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
