# -*- coding:utf-8 -*-

import ConfigParser
from os import getenv
from os.path import join

CONFIG_PATH = ".\\config.ini"


def get_env(file_path):
    lpos = file_path.find(r"%")
    rpos = file_path.rfind(r"%")
    env_val = file_path[lpos : rpos + 1]
    other_path = file_path.replace(env_val, r"").strip("/").strip("\\")
    env_val = getenv(env_val[1 : -1])
    if env_val is None:
        return file_path
    file_path = join(env_val, other_path)
    return file_path


class Singleton(type):

    def __init__(cls, name, bases, class_dict):
        super(Singleton, cls).__init__(name, bases, class_dict)
        cls.instance = None

    def __call__(cls, *args, **argv):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **argv)
        return cls.instance


class Config(object):

    __metaclass__ = Singleton

    def __init__(self, config_path=CONFIG_PATH):
        self._config_path = config_path
        self.log_file_path = None
        self.log_file_tag = None
        self.export_path = None
        self.reload()

    def reload(self):
        cf = ConfigParser.ConfigParser()
        cf.read(self._config_path)
        self.log_file_path = cf.get("config", "LOG_FILE_PATH")
        self.log_file_path = get_env(self.log_file_path)
        self.log_file_tag = cf.get("config", "LOG_FILE_TAG")
        self.export_path = cf.get("config", "EXPORT_PATH")

    def print_config(self):
        print "{0}configuration{0}".format("=" * 20)
        print "log_file_path: ", self.log_file_path
        print "log_file_tag: ", self.log_file_tag
        print "export_path: ", self.export_path
        print "=" * 53


if __name__ == "__main__":
    conf = Config()
    conf.print_config()

