# -*- coding:utf-8 -*-

"""
Analyze logs of the following situations:
    Non SSO 1st login
    Non SSO 2nd login
    SSO 1st login
    SSO 2nd login

The analyze results will include:
    1. Log analyse:
        Login lifecycle time cost
        JCC connection time cost
        JMP connection time cost
    2. Performance:
        List of CPU percentage
        List of Memory usage

Parameters:
    -c --clean: clean log at the end of the script
    -s --sso: SSO
    -i --sign-in: sign in
    -r --reset: reset
    -o --sign-out: sign out
    -t --type: 1 = 1st, 2 = 2nd, 3 = 1st and 2nd
    -m --monitor: monitor cpu and memory usage of a certain process
    --export: File path the analysis result exported to

PS: The current version is lack of reset and logout part
"""

import logging
import argparse
from os import getcwd
from os import chdir
from os.path import dirname, basename, join

from config import Config
from log_parser import LogParser
from lifecycle import LifecycleBase
import lifecycle_cases
from performance import Performance


class ArgType:

    SSO = 0x00008000
    SIGN_IN = 0x00004000
    SIGN_OUT = 0x00002000
    RESET = 0x00001000
    FIRST_SIGN_IN = 0x00000001
    SECOND_SIGN_IN = 0x00000002
    MONITOR = 0x10000000

    def __init__(self):
        self.analyze_type = 0
        self.clean = False
        self.export_to = None
        self.process_name = None
        self.is_monitor = False
        self.timespan = 1
        self.message = ""
        self.process_args()

    @staticmethod
    def get_parsed_args():
        parser = argparse.ArgumentParser(description="Run Log Performance Analysis.")

        parser.add_argument("-c", "--clean",
                            action="store_true",
                            help="Clean log at the end of the script")

        parser.add_argument("--export",
                            default="",
                            action="store",
                            help="File path the analysis result exported to.")

        parser.add_argument("-s", "--sso",
                            action="store_true",
                            help="SSO")

        parser.add_argument("-i", "--sign-in",
                            action="store_true",
                            help="Analyze log data of sign in.")

        parser.add_argument("-r", "--reset",
                            action="store_true",
                            help="Analyze log data of reset.")

        parser.add_argument("-o", "--sign-out",
                            action="store_true",
                            help="Analyze log data of sign out.")

        parser.add_argument("-t", "--type",
                            default=1,
                            type=int,
                            action="store",
                            choices=[1, 2, 3],
                            help="1st (1), 2nd (2) or 3(1st and 2nd) sign in.\
                             Only useful with -i or --sign-in parameter.")

        parser.add_argument("-m", "--monitor",
                            type=str,
                            action="store",
                            help="Monitor process for CPU and memory usage.")

        parser.add_argument("-M", "--message",
                            type=str,
                            action="store",
                            help="Title message of report")

        parser.add_argument("-ts", "--timespan",
                            default=1,
                            type=int,
                            action="store",
                            help="Time span (s) of monitor. Default is 1s.")

        return parser.parse_args()

    def process_args(self):
        args = ArgType.get_parsed_args()
        self.analyze_type = 0

        if args.clean:
            self.clean = True

        if args.export:
            LifecycleBase._export_to = args.export
            Performance._export_to = args.export

        if args.sso:
            self.analyze_type = self.analyze_type | ArgType.SSO

        if args.sign_in:
            self.analyze_type = self.analyze_type | ArgType.SIGN_IN
            if args.type == 1:
                self.analyze_type = self.analyze_type | ArgType.FIRST_SIGN_IN
            elif args.type == 2:
                self.analyze_type = self.analyze_type | ArgType.SECOND_SIGN_IN
            elif args.type == 3:
                self.analyze_type = self.analyze_type | ArgType.FIRST_SIGN_IN | ArgType.SECOND_SIGN_IN

        if args.sign_in is False and args.sign_out:
            self.analyze_type = self.analyze_type | ArgType.SIGN_OUT

        if args.sign_in is False and args.sign_out is False and args.reset:
            self.analyze_type = self.analyze_type | ArgType.RESET

        if args.message:
            self.message = args.message

        if args.monitor:
            self.is_monitor = True
            self.process_name = args.monitor
            self.analyze_type = ArgType.MONITOR
            self.timespan = args.timespan


def exec_operation():
    arg_type = ArgType()
    args_res = arg_type.analyze_type

    conf = Config()
    if arg_type.is_monitor:
        perform = Performance(arg_type.process_name, arg_type.message)

    if LifecycleBase._export_to is None:
        LifecycleBase._export_to = conf.export_path
    if Performance._export_to is None:
        Performance._export_to = conf.export_path


    operations = {
        ArgType.SIGN_IN | ArgType.FIRST_SIGN_IN :\
            lambda var, msg: lifecycle_cases.NonSSOLifecycle().first_sign_in(var, msg),

        ArgType.SIGN_IN | ArgType.SECOND_SIGN_IN:\
            lambda var, msg: lifecycle_cases.NonSSOLifecycle().second_sign_in(var, msg),

        ArgType.SIGN_IN | ArgType.FIRST_SIGN_IN | ArgType.SECOND_SIGN_IN:\
            lambda var, msg: lifecycle_cases.NonSSOLifecycle().first_second_sign_in_out(var, msg),

        ArgType.SSO | ArgType.SIGN_IN | ArgType.FIRST_SIGN_IN:\
            lambda var, msg: lifecycle_cases.SSOLifecycle().first_sign_in(var, msg),

        ArgType.SSO | ArgType.SIGN_IN | ArgType.SECOND_SIGN_IN:\
            lambda var, msg: lifecycle_cases.SSOLifecycle().second_sign_in(var, msg),

        ArgType.SSO | ArgType.SIGN_IN | ArgType.FIRST_SIGN_IN | ArgType.SECOND_SIGN_IN:\
            lambda var, msg: lifecycle_cases.SSOLifecycle().first_second_sign_in_out(var, msg),

        ArgType.MONITOR:\
            lambda: perform.begin_monitor(time_span=arg_type.timespan),
    }

    method = operations.get(args_res)
    if method is not None:
        if arg_type.is_monitor:
            method()
        else:
            log_list = LogParser(conf.log_file_path, conf.log_file_tag)
            method(log_list, arg_type.message)
            if arg_type.clean:
                log_list.clean_log()
                logging.info("Log cleaned")


if __name__ == "__main__":
    logging.basicConfig(format="[%(asctime)s][%(levelname)s][%(filename)s][%(lineno)d] %(message)s",
                        level=logging.INFO,
                        filename="./LogPerformanceAnalysis.log")
    chdir(dirname(join(r".", __file__)))
    exec_operation()
