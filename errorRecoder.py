import json
import os
import codecs

errorPath = os.getcwd() + '\\error.json'


def saveErrorUrlToJson(errorArray):
    with codecs.open(errorPath, 'a', encoding='UTF-8') as f:
        line = json.dumps(errorArray, ensure_ascii=False) + '\n'
        f.write(line)
        f.close()
