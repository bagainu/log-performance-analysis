# -*- coding:utf-8 -*-

from os import listdir, remove
from os.path import isfile, join
import re
import tags


def clean_log_from_path(file_path):
    for f in listdir(file_path):
        temp = join(file_path, f)
        if isfile(temp): remove(temp)


def get_file_list(file_path, file_tag=""):
    log_list = list()
    for f in listdir(file_path):
        if file_tag is not None and re.match(r'.*?{0}.*?'.format(file_tag), f) is None:
            continue
        temp = join(file_path, f)
        if isfile(temp): log_list.append(temp)
    log_list.sort(reverse=True)
    return log_list


def time_string_to_millisecond(time_str):
    temp = time_str.strip().split(",")
    millisecond = int(temp[-1])
    temp = temp[0].split(":")
    hour = int(temp[0])
    minute = int(temp[1])
    second = int(temp[2])
    res = millisecond + second * 1000 + minute * 60 * 1000 + hour * 60 * 60 * 1000
    return res


def get_log_list(file_list, tag_list):
    log_list = list()
    for log in file_list:
        with open(log, "r") as pf:
            for line in pf.xreadlines():
                for tag in tag_list:
                    if re.match(r'.*?{0}.*?'.format(tag), line):
                        temp = line.strip().split(" ")
                        log_list.append(([tag, time_string_to_millisecond(temp[1])]))
                        print """[{0}] - [{1}]""".format(str(tag), temp[1])
                        break
    return log_list


class LogParser(object):

    def __init__(self, file_path, file_tag=""):
        self.file_path = file_path
        self.file_tag = file_tag
        self.tag_list = tags.to_list()
        self.log_list = list()
        self.reload()

    def get(self, key, number=0):
        """
        Get time stamp of key.
        :param key:
        key: key tag in log_list
        number: No. number key in the log_list
        :return: time stamp (int)
        """
        res = 0
        assert number >= 0
        for temp in self.log_list:
            if temp[0] == key:
                if number == 0:
                    res = temp[1]
                    break
                number -= 1
        return res

    def reload(self):
        file_list = get_file_list(self.file_path, self.file_tag)
        self.log_list = get_log_list(file_list, self.tag_list)

    def clean_log(self):
        clean_log_from_path(self.file_path)


if __name__ == '__main__':
    file_path = ".\\fastlogin_log_test"
    file_tag = "jabber_nonsso_1st_login"

    log_parser = LogParser(file_path, file_tag)
    print log_parser.get("Performance: START")
    print log_parser.get("Performance: PWD_ENTERED")

