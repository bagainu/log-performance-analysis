# -*- coding:utf-8 -*-

import logging
import psutil
import time
import threading
from os.path import exists
import csv


def get_process(process_name):
    res = None
    for p in psutil.process_iter():
        if process_name == p.name():
            res = p
            break
    return res


class Performance(object):

    _export_to = None

    def __init__(self, name, message=""):
        self.process = None
        self.process_name = name
        self.message = message
        self.data_cpu = {}
        self.data_memory = {}

        self.time_span = 1
        self.terminate = True

    @property
    def name(self):
        return self.process_name

    @property
    def is_active(self):
        return not self.terminate

    @property
    def cpu(self):
        return self.data_cpu

    @property
    def memory(self):
        return self.data_memory

    def begin_monitor(self, time_span=1, time_out=30):
        self.terminate = False
        self.time_span = time_span
        for i in range(time_out):
            logging.info("Finding process {0}. Trying....{1}".format(self.process_name, i + 1))
            self.process = get_process(self.process_name)
            if self.process is not None:
                break
            time.sleep(1)
        if self.process is None:
            logging.error("Finding process {0} time out".format(self.process_name))
            self.end_monitor()
            return
        logging.info("Process found. Begin monitor")
        self.recording()

    def end_monitor(self):
        logging.info("End monitor")
        self.terminate = True
        if self.__class__._export_to is not None:
            msg_type = self.__class__._export_to.strip().split(r".")[-1]
            print msg_type
            self.get_msg_type_print(msg_type)(self.message)

    def get_msg_type_print(self, msg_type):
        return {
            "": self.print_all_default,
            "xml": self.print_all_xml,
            "csv": self.print_all_csv,
        }.get(msg_type, self.print_all_default)

    @staticmethod
    def _thread_func(self):
        to_terminate = self.terminate
        while not to_terminate:
            to_terminate = self.terminate
            if not self.process.is_running():
                self.end_monitor()
                break
            time_stamp = time.time()
            self.data_cpu[time_stamp] = self.process.cpu_percent()                              # percentage
            self.data_memory[time_stamp] = self.process.memory_info().rss / 1024.0 / 1024.0     # MB
            time.sleep(self.time_span)

    def recording(self):
        th = threading.Thread(target=Performance._thread_func, args=[self, ])
        th.start()

    def format_msg_default(self, msg):
        format_str = ""
        for key in self.data_cpu.keys():
            format_str += "{0}\t{1}\t{2}\n".format(key, self.data_cpu[key], self.data_memory[key])
        return """report title="{0}"
datetime="{1}"
TimeStamp(s)\tCPU(%)\tMemory(MB)
{2}
""".format(
            msg,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            format_str,
        )

    def format_msg_xml(self, msg):
        format_str = ""
        for key in self.data_cpu.keys():
            format_str += "{0}\t{1}\t{2}\n".format(key, self.data_cpu[key], self.data_memory[key])
        return """<report title="{0}" datetime="{1}">
TimeStamp(s)\tCPU(%)\tMemory(MB)
{2}</report>
""".format(
            msg,
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            format_str,
        )

    def format_msg_csv(self, msg):
        format_list = []
        if msg is not None and len(msg) != 0:
            format_list.append(["title", msg])
        format_list.append(["datetime", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())])
        format_list.append(["TimeStamp(s)", "CPU(%)", "Memory(MB)"])
        for key in self.data_cpu.keys():
            format_list.append([str(key), str(self.data_cpu[key]), str(self.data_memory[key])])
        return format_list

    def print_all_default(self, msg=""):
        msg_res = self.format_msg_default(msg)
        logging.debug(msg_res)
        if self.__class__._export_to:
            if not exists(self.__class__._export_to):
                with open(self.__class__._export_to, "w+") as pf:
                    pf.write(msg_res)
            else:
                with open(self.__class__._export_to, "a+") as pf:
                    pf.write("\n\n")
                    pf.write(msg_res)

    def print_all_xml(self, msg=""):
        msg_res = self.format_msg_xml(msg)
        logging.debug(msg_res)
        if self.__class__._export_to:
            if not exists(self.__class__._export_to):
                with open(self.__class__._export_to, "w+") as pf:
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

    def print_all_csv(self, msg=""):
        msg_res = self.format_msg_csv(msg)
        logging.debug(msg_res)
        if self.__class__._export_to:
            if not exists(self.__class__._export_to):
                with open(self.__class__._export_to, "wb+") as pf:
                    csv_writer = csv.writer(pf)
                    for row in msg_res:
                        csv_writer.writerow(row)
            else:
                with open(self.__class__._export_to, "ab+") as pf:
                    csv_writer = csv.writer(pf)
                    csv_writer.writerow([])
                    csv_writer.writerow([])
                    for row in msg_res:
                        csv_writer.writerow(row)


if __name__ == "__main__":
    perform = Performance(r"CiscoJabber.exe")
    perform.begin_monitor()
    for i in range(100):
        print i
        time.sleep(1)
        if not perform.is_active:
            break
    print perform.cpu
    print perform.memory





