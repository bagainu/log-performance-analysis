# -*- coding:utf-8 -*-

from log_parser import LogParser
import tags
from lifecycle import LifecycleBase


class NonSSOLifecycle(LifecycleBase):

    def __init__(self):
        super(NonSSOLifecycle, self).__init__()

    @LifecycleBase.case
    def first_sign_in(self, log_list, msg=''):
        self.clear_all()

        self.discovery = log_list.get(tags.Lifecycle.EMAIL_REQUIRED) - log_list.get(tags.Lifecycle.START)

        self.show_main_hub_since_launch = self.discovery\
                             + log_list.get(tags.Lifecycle.PWD_REQUIRED) - log_list.get(tags.Lifecycle.EMAIL_ENTERED)\
                             + log_list.get(tags.Lifecycle.SIGNED_IN) - log_list.get(tags.Lifecycle.PWD_ENTERED)

        self.jcc_auth = log_list.get(tags.JCC.STARTED) - log_list.get(tags.JCC.START)

        self.jcc_connect = log_list.get(tags.JCC.CONNECTED) - log_list.get(tags.JCC.START)

        self.imp_auth = log_list.get(tags.IMP.STARTED) - log_list.get(tags.IMP.START)

        self.presence_received_since_connected = log_list.get(tags.IMP.PRESENCE_RECEIVED) - log_list.get(tags.IMP.STARTED)

        self.contacts_fetched = log_list.get(tags.Contacts.STARTED) - log_list.get(tags.Contacts.START)

        if msg is None or len(msg) == 0:
            self.print_all(self.first_sign_in.__name__)
        else:
            self.print_all(msg)

    @LifecycleBase.case
    def second_sign_in(self, log_list, msg=''):
        self.clear_all()

        self.discovery = log_list.get(tags.Lifecycle.SIGNING_IN) - log_list.get(tags.Lifecycle.START)

        self.show_main_hub_since_launch = self.discovery\
                                          + log_list.get(tags.Lifecycle.SIGNED_IN) - log_list.get(tags.Lifecycle.SIGNING_IN)

        self.jcc_auth = log_list.get(tags.JCC.STARTED) - log_list.get(tags.JCC.START)

        self.jcc_connect = log_list.get(tags.JCC.CONNECTED) - log_list.get(tags.JCC.START)

        self.imp_auth = log_list.get(tags.IMP.STARTED) - log_list.get(tags.IMP.START)

        self.presence_received_since_connected = log_list.get(tags.IMP.PRESENCE_RECEIVED) - log_list.get(tags.IMP.STARTED)

        self.contacts_fetched = log_list.get(tags.Contacts.STARTED) - log_list.get(tags.Contacts.START)

        if msg is None or len(msg) == 0:
            self.print_all(self.second_sign_in.__name__)
        else:
            self.print_all(msg)

    @LifecycleBase.case
    def first_second_sign_in_out(self, log_list, msg=''):
        self.clear_all()

        self.discovery_1 = log_list.get(tags.Lifecycle.EMAIL_REQUIRED) - log_list.get(tags.Lifecycle.START)

        self.show_main_hub_since_launch_1 = self.discovery_1\
            + log_list.get(tags.Lifecycle.PWD_REQUIRED) - log_list.get(tags.Lifecycle.EMAIL_ENTERED) \
            + log_list.get(tags.Lifecycle.SIGNED_IN) - log_list.get(tags.Lifecycle.PWD_ENTERED)

        self.sign_out = log_list.get(tags.Lifecycle.SIGN_IN_REQUIRED) - log_list.get(tags.Lifecycle.SIGNING_OUT)

        self.discovery_2 = log_list.get(tags.Lifecycle.SIGNING_IN, 1) - log_list.get(tags.Lifecycle.START, 1)

        self.show_main_hub_since_launch_2 = self.discovery_2\
                                            + log_list.get(tags.Lifecycle.SIGNED_IN, 1) - log_list.get(tags.Lifecycle.SIGNING_IN, 1)

        self.total_first_sign_in = self.discovery_1 + self.sign_in_1

        self.total_second_sign_in = self.discovery_2 + self.sign_in_2

        if msg is None or len(msg) == 0:
            self.print_all(self.first_second_sign_in_out.__name__)
        else:
            self.print_all(msg)


class SSOLifecycle(LifecycleBase):

    def __init__(self):
        super(SSOLifecycle, self).__init__()

    @LifecycleBase.case
    def first_sign_in(self, log_list, msg=''):
        self.clear_all()

        self.discovery = log_list.get(tags.Lifecycle.EMAIL_REQUIRED) - log_list.get(tags.Lifecycle.START)

        self.launch_browser = log_list.get(tags.Lifecycle.SSO_BROWSER_SWITCH_ON) - log_list.get(tags.Lifecycle.EMAIL_ENTERED)

        self.show_main_hub_since_launch = self.discovery + self.launch_browser\
                                          + log_list.get(tags.Lifecycle.SIGNED_IN) - log_list.get(tags.Lifecycle.SSO_BROWSER_SWITCH_OFF)

        self.jcc_auth = log_list.get(tags.JCC.STARTED) - log_list.get(tags.JCC.START)

        self.jcc_connect = log_list.get(tags.JCC.CONNECTED) - log_list.get(tags.JCC.START)

        self.imp_auth = log_list.get(tags.IMP.STARTED) - log_list.get(tags.IMP.SSO_START)

        self.presence_received_since_connected = log_list.get(tags.IMP.PRESENCE_RECEIVED) - log_list.get(tags.IMP.STARTED)

        self.contacts_fetched = log_list.get(tags.Contacts.STARTED) - log_list.get(tags.Contacts.START)

        if msg is None or len(msg) == 0:
            self.print_all(self.first_sign_in.__name__)
        else:
            self.print_all(msg)

    @LifecycleBase.case
    def second_sign_in(self, log_list, msg=''):
        self.discovery = log_list.get(tags.Lifecycle.SIGNING_IN) - log_list.get(tags.Lifecycle.START)

        self.show_main_hub_since_launch = self.discovery\
                                          + log_list.get(tags.Lifecycle.SIGNED_IN) - log_list.get(tags.Lifecycle.SIGNING_IN)

        self.jcc_auth = log_list.get(tags.JCC.STARTED) - log_list.get(tags.JCC.START)

        self.jcc_connect = log_list.get(tags.JCC.CONNECTED) - log_list.get(tags.JCC.START)

        self.imp_auth = log_list.get(tags.IMP.STARTED) - log_list.get(tags.IMP.SSO_START)

        self.presence_received_since_connected = log_list.get(tags.IMP.PRESENCE_RECEIVED) - log_list.get(tags.IMP.STARTED)

        self.contacts_fetched = log_list.get(tags.Contacts.STARTED) - log_list.get(tags.Contacts.START)

        if msg is None or len(msg) == 0:
            self.print_all(self.second_sign_in.__name__)
        else:
            self.print_all(msg)

    @LifecycleBase.case
    def first_second_sign_in_out(self, log_list, msg=''):
        self.clear_all()

        self.discovery_1 = log_list.get(tags.Lifecycle.EMAIL_REQUIRED) - log_list.get(tags.Lifecycle.START)

        self.launch_browser_1 = + log_list.get(tags.Lifecycle.SSO_BROWSER_SWITCH_ON) - log_list.get(tags.Lifecycle.EMAIL_ENTERED)

        self.show_main_hub_since_launch_1 = self.discovery_1 + self.launch_browser_1\
                                            + log_list.get(tags.Lifecycle.SIGNED_IN) - log_list.get(tags.Lifecycle.SSO_BROWSER_SWITCH_OFF)

        self.sign_out = log_list.get(tags.Lifecycle.SIGN_IN_REQUIRED) - log_list.get(tags.Lifecycle.SIGNING_OUT)

        self.discovery_2 = log_list.get(tags.Lifecycle.SIGNING_IN, 1) - log_list.get(tags.Lifecycle.START, 1)

        self.show_main_hub_since_launch_2 = self.discovery_2\
                                            + log_list.get(tags.Lifecycle.SIGNED_IN, 1) - log_list.get(tags.Lifecycle.SIGNING_IN, 1)

        self.total_first_sign_in = self.discovery_1 + self.sign_in_1

        self.total_second_sign_in = self.discovery_2 + self.sign_in_2

        if msg is None or len(msg) == 0:
            self.print_all(self.first_second_sign_in_out.__name__)
        else:
            self.print_all(msg)


def main():
    from config import Config
    conf = Config()

    log_list = LogParser(conf.log_file_path, conf.log_file_tag)
    # non_sso_lifecycle = NonSSOLifecycle()
    # non_sso_lifecycle.first_sign_in(log_list)
    sso_lifecycle = SSOLifecycle()
    sso_lifecycle.second_sign_in(log_list)
    print sso_lifecycle.to_dict()

if __name__ == '__main__':
    main()

