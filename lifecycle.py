# -*- coding:utf-8 -*-

import logging
import time
import functools
from log_parser import LogParser
import re
from os.path import exists
from collections import OrderedDict


class LifecycleBase(object):

    _export_to = None

    def __init__(self):
        self._ordered_dict_ = OrderedDict()
        self._total = 0

    def __setattr__(self, key, value):
        if key == "_ordered_dict_":
            return super(LifecycleBase, self).__setattr__(key, value)
        self._ordered_dict_[key] = value

    def __getattr__(self, item):
        try:
            return self._ordered_dict_[item]
        except KeyError:
            raise AttributeError(item)

    @property
    def total(self):
        for key in self._ordered_dict_.keys():
            if key != "_total":
                self._total = self._total + self._ordered_dict_[key]
        return self._total

    def clear_all(self):
        for key in self._ordered_dict_.keys():
            self._ordered_dict_[key] = 0

    @staticmethod
    def case(method):
        @functools.wraps(method)
        def wrapper(self, arg, msg):
            if isinstance(arg, LogParser) and len(arg.log_list) > 0:
                return method(self, arg, msg)
            else:
                logging.error("Error: Log is empty")
        return wrapper

    def first_sign_in(self, log_list, msg=''):
        raise NotImplementedError

    def second_sign_in(self, log_list, msg=''):
        raise NotImplementedError

    def first_second_sign_in_out(self, log_list, msg=''):
        """
        first sign in
        exit
        second sign in
        sign out
        exit
        """
        raise NotImplementedError

    def to_dict(self):
        res_dict = {}
        for key, val in self._ordered_dict_.items():
            if not re.match(r"_.?", key):
                res_dict[key] = val / 1000.0
        return res_dict

    def format_msg(self, msg, total):
        format_str = ""
        for key, val in self._ordered_dict_.items():
            if not re.match(r"_.?", key):
                format_str += "{0} : {1} s\n".format(key, val / 1000.0)
                # format_str += "{0}\n".format(val / 1000.0)
        if total:
            format_str += "{0} : {1} s\n".format("total", self.total / 1000.0)
        return """<report title="{0}" datetime="{1}" >
{2}</report>
""".format(
            msg,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            format_str
        )

    def print_all(self, msg="", total=False):
        msg_res = self.format_msg(msg, total)
        logging.debug(msg_res)
        if self.__class__._export_to:
            if not exists(self.__class__._export_to):
                with open(self.__class__._export_to, "w") as pf:
                    pf.write('<reports>\n')
                    pf.write(msg_res)
                    pf.write('</reports>')
            else:
                with open(self.__class__._export_to, "r+") as pf:
                    data = pf.readlines()
                    if len(data) == 0:
                        pf.write('<reports>\n')
                    elif data[-1].find('</reports>') != -1:
                        data.pop()
                    pf.seek(0, 0)
                    pf.writelines(data)
                    pf.write(msg_res)
                    pf.write('</reports>')



