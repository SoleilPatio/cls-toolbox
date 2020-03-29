# -*- coding: utf-8 -*-
from __future__ import print_function
# import json
import commentjson
import codecs
import logging

class JsonConfig(object):
    def __init__(self):
        super(JsonConfig, self).__init__()
        self.data = {}

    def Load(self, json_file_name):
        with open(json_file_name) as infile:
            self.data = commentjson.load(infile)
        return self.data

    def Save(self, json_file_name):
        self.SaveData(self.data, json_file_name)

    def SaveData(self, data, json_file_name):
        self.data = data
        with codecs.open(json_file_name, 'w' , encoding='utf-8') as outfile:
            commentjson.dump(self.data, outfile, indent=4 , ensure_ascii=False, sort_keys=True)

    def Show(self):
        self.ShowData(self.data)

    def ShowData(self, data):
        logging.info(commentjson.dumps(data, indent=4 , sort_keys=True).decode('unicode-escape'))


if __name__ == '__main__':
    jsonconf = JsonConfig()
    jsonconf.Load("test-config-common-read.json")
    jsonconf.Show()
    jsonconf.Save("test-config-common-write.json")
    pass
