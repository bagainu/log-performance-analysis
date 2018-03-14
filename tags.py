# -*- coding:utf-8 -*-


registry_list = []


def to_list():
    res_list = []
    for temp in registry_list:
        res_list += temp.to_list()
    return res_list


class MetaTags(type):

    def __new__(meta, name, bases, class_dict):
        cls = super(MetaTags, meta).__new__(meta, name, bases, class_dict)
        registry_list.append(cls)
        return cls

    def to_list(cls):
        res_list = []
        for key, val in cls.__dict__.items():
            if key.find(r'__') is -1:
                res_list.append(val)
        return res_list


class Lifecycle(object):

    __metaclass__ = MetaTags

    START = r"Performance: START"
    EMAIL_REQUIRED = r"Performance: EMAIL_REQUIRED"
    EMAIL_ENTERED = r"Performance: EMAIL_ENTERED"
    PWD_REQUIRED = r"Performance: PWD_REQUIRED"
    PWD_ENTERED = r"Performance: PWD_ENTERED"
    SIGNING_IN = r"Performance: SIGNING_IN"
    SIGNED_IN = r"Performance: SIGNED_IN"
    SSO_BROWSER_SWITCH_ON = r"Performance: SSO_BROWSER_SWITCH_ON"
    SSO_BROWSER_SWITCH_OFF = r"Performance: SSO_BROWSER_SWITCH_OFF"
    SIGNING_OUT = r"Performance: SIGNING_OUT"
    SIGN_IN_REQUIRED = r"Performance: SIGN_IN_REQUIRED"


class JCC(object):

    __metaclass__ = MetaTags

    START = r"\[jcf.tel.adapter\] \[CSFUnified::TelephonyAdapter::startTelephonyAuthenticationFeatureSet\] - -->"
    STARTED = r"\[jcf.tel.adapter\] \[CSFUnified::TelephonyAdapter::startTelephonyAuthenticationFeatureSet\] - <--"
    CONNECT = r"Telephony Service Device Connection Status changed from \[Disconnected\] to \[Connecting\]"
    CONNECTED = r"Telephony Service Device Connection Status changed from \[Connecting\] to \[Connected\]"


class IMP(object):

    __metaclass__ = MetaTags

    # RECONNECTING = r"IMP Outage::Setting server health to Reconnecting"
    # CONNECTED = r"IMP Outage::Setting server health to Connected"
    START = r"\[csf.jwcpp\] \[LoginMgrImpl::Login\] - @LoginMgr: #0, LoginMgrImpl::Login type:"
    SSO_START = r"\[csf.jwcpp\] \[CLoginIM::_loginIM\] - @LoginMgr: #0, CLoginIM::_loginIM login, jabber, serv:"
    # STARTED = r"\[csf.jwcpp\] \[CLoginMgrConnectionPointContainer::Fire_OnLoginSuccess\] - @LoginMgr: #0, CLoginMgrConnectionPointContainer::Fire_OnLoginSuccess login, OnLoginSuccess"
    STARTED = r"Updating Authentication status to: AuthValid"
    PRESENCE_RECEIVED = r"First Self Presence Received"


class Contacts(object):

    __metaclass__ = MetaTags

    # START = r"\[ContactService-ContactsAdapter\] \[CSFUnified::ContactsAdapter::GetAllContacts\] - ContactsAdapter::GetAllContacts"
    START = r"\[ContactService-ContactsAdapter\] \[CSFUnified::ContactsAdapter::start\] - Starting feature set"
    STARTED = r"\[IMPServices\] \[CSFUnified::RosterManagerImpl::processContactFetched\] - processContactFetched its first time process contacts"


if __name__ == "__main__":
    print registry_list
    for key in to_list():
        print key



