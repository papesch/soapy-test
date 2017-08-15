#!/usr/bin/env python
import socket
import time
import sys
import re
import string
import pprint
import unittest
import xml.parsers.expat

global THISPY
THISPY = "swHarness.py"
REG = False
TRAN = 0
print
    
#host, port to be read from config file
global SWPORT
global SWHOST
config_file = "swConfig.py"
if config_file[-3:] == ".py":
   config_file = config_file[:-3]
data_config = __import__(config_file, globals(), locals(), [])
SWPORT = data_config.SWPORT
SWHOST = data_config.SWHOST


def main():

    if len(sys.argv) > 1:
        SWCOMMAND = string.lower(str(sys.argv[1]))
    else:
        SWCOMMAND = "show_help"

    if SWCOMMAND == "applycreditalteration" or SWCOMMAND == "a":
        print "ApplyCreditAlteration"
        do_apply_cred_alt()
    elif SWCOMMAND == "changemsisdn" or SWCOMMAND == "cm":
        print "ChangeMsisdn"
        do_change_msisdn()
    elif SWCOMMAND == "createsubscription" or SWCOMMAND == "c":
        print "CreateSubscription"
        do_create_sub()
    elif SWCOMMAND == "deletesubscription" or SWCOMMAND == "d":
        print "DeleteSubscription"
        do_delete_sub()
    elif SWCOMMAND == "modifysubscription" or SWCOMMAND == "m":
        print "ModifySubscription"
        do_mod_sub_plan()
    elif SWCOMMAND == "querycdredrs" or SWCOMMAND == "qc":
        print "QueryCDREDRs"
        do_query_cdredr()
    elif SWCOMMAND == "queryrechargecard" or SWCOMMAND == "rc":
        print "QueryRechargeCard"
        do_query_rech_card()
    elif SWCOMMAND == "queryrechargecardtype" or SWCOMMAND == "rt":
        print "QueryRechargeCardType"
        do_query_rech_card_type()
    elif SWCOMMAND == "queryrechargecardbatch" or SWCOMMAND == "rb":
        print "QueryRechCardBatch"
        do_query_rech_card_batch()
    elif SWCOMMAND == "queryresources" or SWCOMMAND == "qr":
        print "QueryResources"
        do_query_resources()
    elif SWCOMMAND == "querysubscription" or SWCOMMAND == "q":
        print "QuerySubscription"
        do_query_sub()
    elif SWCOMMAND == "userechargecard" or SWCOMMAND == "u":
        print "UseRechargeCard"
        do_use_rech_card()
    elif SWCOMMAND == "auto_regression" or SWCOMMAND == "auto":
        global REG
        REG = True
        run_auto_regression()
    else:
        print
        print "Usage: " + THISPY + " <soap_command> [arguments]"
        print
        print "Commands:"
        print "  ApplyCreditAlteration      a    <msisdn> <reason-code> <amount> <adj-type>"
        print "  ChangeMsisdn               cm   <old_msisdn> <new_msisdn>"
        print "  CreateSubscription         c    <msisdn>"
        print "  DeleteSubscription         d    <msisdn>"
        print "  ModifySubscription         m    <msisdn> <tariff-plan>"
        print "  QueryCDREDRs               qc   <msisdn>"
        print "  QueryRechargeCard          rc   <serial_no>"
        print "  QueryRechCardBatch         rb   <serial_no>"
        print "  QueryRechargeCardType      rt   <serial_no>"
        print "  QueryResources             qr   <msisdn>"
        print "  QuerySubscription          q    <msisdn>"
        print "  UseRechargeCard            u    <msisdn> <recharge_pin>"
        print "  auto_regression          auto   SoapWrapper automated test suite"
        print "                                  --should ALWAYS be run via swAutoRegression.sh"
        print
        print "For further help, type the command with no arguments, i.e."
        print "  " + THISPY + " <soap_command>"

        sys.exit(1)


def send_xml(XMLREQUEST):
    #host, port to be read from config file
    #SWHOST = '127.0.0.1'
    #SWPORT = 6060
    global TRAN
    
    #if auto-regression is running, keep count of transactions
    if REG:
        TRAN += 1
        print "[test no. " + str(TRAN) + "]"
    
    #send request
    print "[SOAP request, port " + str(SWPORT) + "]"
    parse_xml(XMLREQUEST)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SWHOST, SWPORT))
    s.send(XMLREQUEST)

    #get response
    print "[SOAPWrapper response]"
    global XMLRESULT
    XMLRESULT = s.recv(100000)

    #figuring out the frikking xml parser
    #debug# print XMLREQUEST
    #debug# print XMLRESULT
    lines = XMLRESULT.split('\n')
    SOAPRESPONSE = lines[7]
    parse_xml(SOAPRESPONSE)
    print "------"
    print
    print
    s.close()


def do_apply_cred_alt():
    if len(sys.argv) < 6:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " ApplyCreditAlteration <msisdn> <reason-code> <amount> <adj-type>"
        print "Example: " + THISPY + "  a  2101835313  8  3.2109  3"
        print
	print "Reason codes"
        print "   8 = general(?)"
        print " 153 = credit"
        print " 154 = debit"
        print
        print "Adjustment types"
        print "   1 = credit adj"
        print "   2 = debit adj"
        print "   3 = debit adj"
        print "   9 = credit card adj"
        print

        sys.exit(1)

    MSISDN = str(sys.argv[2]) 
    REASON = str(sys.argv[3]) 
    AMOUNT = str(sys.argv[4]) 
    ADJTYPE = str(sys.argv[5]) 
    apply_cred_alt(MSISDN,REASON,AMOUNT,ADJTYPE)


def apply_cred_alt(MSISDN,REASON,AMOUNT,ADJTYPE):
    f = open('xml/testApplyCreditAlteration.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 
    XMLREQUEST=re.sub('REASON_INPUT',REASON,XMLREQUEST) 
    XMLREQUEST=re.sub('AMOUNT_INPUT',AMOUNT,XMLREQUEST) 
    XMLREQUEST=re.sub('ADJTYPE_INPUT',ADJTYPE,XMLREQUEST) 

    send_xml(XMLREQUEST)
    

def do_change_msisdn():
    if len(sys.argv) < 4:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " ChangeMsisdn <old_msisdn> <new_msisdn>"
        print "Example: " + THISPY + "  cm  211344000  211344001"
        print
        sys.exit(1)

    OLDMSISDN = str(sys.argv[2])
    NEWMSISDN = str(sys.argv[3])
    change_msisdn(OLDMSISDN,NEWMSISDN)


def change_msisdn(OLDMSISDN,NEWMSISDN):
    f = open('xml/testChangeMsisdn.xml', 'r')
    XMLREQUEST=re.sub('OLDMSISDN_INPUT',OLDMSISDN,f.read())
    XMLREQUEST=re.sub('NEWMSISDN_INPUT',NEWMSISDN,XMLREQUEST)

    send_xml(XMLREQUEST)


def do_create_sub():
    #debug# print str(len(sys.argv))
    if len(sys.argv) < 3:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " CreateSubscription <msisdn>"
        print "Example: " + THISPY + "  c  2101333000"
        print
        sys.exit(1)

    MSISDN = str(sys.argv[2]) 
    create_sub(MSISDN)


def create_sub(MSISDN):
    f = open('xml/testCreateSubscription.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 

    send_xml(XMLREQUEST)


def create_sub_complex(MSISDN,TPLAN,LANG,SP,PIN,HOME,IMSI,CREDIT,CREDPER):
    f = open('xml/testCreateSubComplex.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 
    XMLREQUEST=re.sub('TPLAN_INPUT',TPLAN,XMLREQUEST) 
    XMLREQUEST=re.sub('LANG_INPUT',LANG,XMLREQUEST) 
    XMLREQUEST=re.sub('SP_INPUT',SP,XMLREQUEST) 
    XMLREQUEST=re.sub('PIN_INPUT',PIN,XMLREQUEST) 
    XMLREQUEST=re.sub('HOME_INPUT',HOME,XMLREQUEST) 
    XMLREQUEST=re.sub('IMSI_INPUT',IMSI,XMLREQUEST) 
    XMLREQUEST=re.sub('CREDIT_INPUT',CREDIT,XMLREQUEST) 
    XMLREQUEST=re.sub('CREDPER_INPUT',CREDPER,XMLREQUEST) 

    send_xml(XMLREQUEST)


def do_delete_sub():
    if len(sys.argv) < 3:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " DeleteSubscription <msisdn>"
        print "Example: " + THISPY + "  d  2101835310"
        print
        sys.exit(1)

    MSISDN = str(sys.argv[2]) 
    delete_sub(MSISDN)


def delete_sub(MSISDN):
    f = open('xml/testDeleteSubscription.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 

    send_xml(XMLREQUEST)


def do_mod_sub_plan():
    if len(sys.argv) < 4:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " ModifySubscription <msisdn> <tariff-plan>"
        print "Example: " + THISPY + "  m  2101835313  Supa_Prepay"
        print
        sys.exit(1)

    MSISDN = str(sys.argv[2])
    TPLAN = str(sys.argv[3])
    mod_sub_plan(MSISDN,TPLAN)


def mod_sub_plan(MSISDN,TPLAN):
    f = open('xml/testModifySubPLAN.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 
    XMLREQUEST=re.sub('TPLAN_INPUT',TPLAN,XMLREQUEST) 

    send_xml(XMLREQUEST)


def mod_sub_action(MSISDN,ACTION):
    f = open('xml/testModifySubACTION.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 
    XMLREQUEST=re.sub('ACTION_INPUT',ACTION,XMLREQUEST) 

    send_xml(XMLREQUEST)


def mod_sub_lang(MSISDN,LANG):
    f = open('xml/testModifySubLANG.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 
    XMLREQUEST=re.sub('LANG_INPUT',LANG,XMLREQUEST) 

    send_xml(XMLREQUEST)


def modify_sub(MSISDN,TPLAN,SP,PIN,IMSI,ACTION):
    f = open('xml/testModifySubscription.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 
    XMLREQUEST=re.sub('TPLAN_INPUT',TPLAN,XMLREQUEST) 
    XMLREQUEST=re.sub('SP_INPUT',SP,XMLREQUEST) 
    XMLREQUEST=re.sub('PIN_INPUT',PIN,XMLREQUEST) 
    XMLREQUEST=re.sub('IMSI_INPUT',IMSI,XMLREQUEST) 
    XMLREQUEST=re.sub('ACTION_INPUT',ACTION,XMLREQUEST) 
    #XMLREQUEST=re.sub('TELENO_INPUT',TELENO,XMLREQUEST) 
    #XMLREQUEST=re.sub('LANG_INPUT',LANG,XMLREQUEST) 

    send_xml(XMLREQUEST)


def do_query_cdredr():
    if len(sys.argv) < 3:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " QueryCDREDRs <msisdn>"
        print "Example: " + THISPY + "  qc  2101835313"
        print
        sys.exit(1)

    MSISDN = str(sys.argv[2]) 
    query_cdredr(MSISDN)


def query_cdredr(MSISDN):
    f = open('xml/testQueryCDREDRs.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 

    send_xml(XMLREQUEST)


def do_query_rech_card():
    if len(sys.argv) < 3:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " QueryRechargeCard <serial_no>"
        print "Example: " + THISPY + "  rc  0000000312-00003"
        print
        sys.exit(1)

    RSERIAL = str(sys.argv[2])
    query_rech_card(RSERIAL)


def query_rech_card(RSERIAL):
    f = open('xml/testQueryRechargeCard.xml', 'r')
    XMLREQUEST=re.sub('RSERIAL_INPUT',RSERIAL,f.read()) 

    send_xml(XMLREQUEST)


def do_query_rech_card_type():
    if len(sys.argv) < 3:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " QueryRechargeCardType <card_val>"
        print "Example: " + THISPY + "  rt  $50"
        print
        sys.exit(1)

    CARDVAL = str(sys.argv[2])
    query_rech_card(CARDVAL)


def query_rech_card_type(CARDVAL):
    f = open('xml/testQueryRechargeCardType.xml', 'r')
    XMLREQUEST=re.sub('CARDVAL_INPUT',CARDVAL,f.read()) 
    
    send_xml(XMLREQUEST)


def do_query_rech_card_batch():
    if len(sys.argv) < 3:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " QueryRechCardBatch <serial_no>"
        print "Example: " + THISPY + "  rb  0000000312-00003"
        print
        sys.exit(1)

    RSERIAL = str(sys.argv[2])
    query_rech_card_batch(RSERIAL)


def query_rech_card_batch(RSERIAL):
    f = open('xml/testQueryRechCardBatch.xml', 'r')
    XMLREQUEST=re.sub('RSERIAL_INPUT',RSERIAL,f.read()) 

    send_xml(XMLREQUEST)


def do_query_resources():
    if len(sys.argv) < 3:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " QueryResources <msisdn>"
        print "Example: " + THISPY + "  qr  2101835313"
        print
        sys.exit(1)

    MSISDN = str(sys.argv[2]) 
    query_resources(MSISDN)


def query_resources(MSISDN):
    f = open('xml/testQueryResources.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 

    send_xml(XMLREQUEST)


def do_query_sub():
    if len(sys.argv) < 3:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " QuerySubscription <msisdn>"
        print "Example: " + THISPY + "  q  2101835313"
        print
        sys.exit(1)

    MSISDN = str(sys.argv[2]) 
    query_sub(MSISDN)


def query_sub(MSISDN):
    f = open('xml/testQuerySubscription.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 

    send_xml(XMLREQUEST)
    

def do_use_rech_card():
    if len(sys.argv) < 4:
        print "ERROR: Not enough arguments (" + str(len(sys.argv)-1) + ")"
        print "Usage:   " + THISPY + " UseRechargeCard <msisdn> <recharge_pin>"
        print "Example: " + THISPY + "  u  2101835313  178480986333"
        print
        sys.exit(1)

    MSISDN = str(sys.argv[2])
    RECNUM = str(sys.argv[3])
    use_rech_card(MSISDN,RECNUM)


def use_rech_card(MSISDN,RECNUM):
    f = open('xml/testUseRechargeCard.xml', 'r')
    XMLREQUEST=re.sub('MSISDN_INPUT',MSISDN,f.read()) 
    XMLREQUEST=re.sub('RECNUM_INPUT',RECNUM,XMLREQUEST) 

    send_xml(XMLREQUEST)


#-----------------------------------------------------------------------------------------
#   
#   XML PARSER
# 
#-----------------------------------------------------------------------------------------


class Element(list):
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = attrs
 

class TreeBuilder:
    def __init__(self):
        self.root = Element("root", None)
        self.path = [self.root]
    def start_element(self, name, attrs):
        element = Element(name, attrs)
        self.path[-1].append(element)
        self.path.append(element)
    def end_element(self, name):
        assert name == self.path[-1].name
        self.path.pop()
    def char_data(self, data):
        self.path[-1].append(data)


def parse_xml(xmldata):
    # create parser and parsehandler
    parser = xml.parsers.expat.ParserCreate()
    treebuilder = TreeBuilder()
    # assign the handler functions
    parser.StartElementHandler  = treebuilder.start_element
    parser.EndElementHandler    = treebuilder.end_element
    parser.CharacterDataHandler = treebuilder.char_data
 
    # parse the data
    parser.Parse(xmldata, True)
    showtree(treebuilder.root)


def showtree(node, prefix=""):
    print prefix, node.name
    for e in node:
        if isinstance(e, Element):
            showtree(e, prefix + "  ")
        else:
            if e.strip():  #get rid of blank
                print prefix + "  ", e


#-----------------------------------------------------------------------------------------
#   
#   AUTOMATED TEST SUITE 
# 
#-----------------------------------------------------------------------------------------


def run_auto_regression():

    set_up_auto_test()
    test_cases_apply_cred_alt()
    test_cases_create_sub()
    test_cases_modify_sub()
    test_cases_delete_sub()
    test_cases_query_cdredr()
    test_cases_query_recharge_card()
    test_cases_query_subscription()
    test_cases_use_recharge()
    test_cases_query_resources()
    test_cases_num_portability()
    test_cases_change_msisdn()


def set_up_auto_test():
    print
    print " # ================================ #"
    print " #                                  #"
    print " # SOAPWrapper Automated Regression #"
    print " #                                  #"
    print " # ================================ #"
    print
    print 'To set up data, please go to Oscar:/apps/frodo/slcomm/reset_msisdns'
    print 'and run the script "do_reset_msisdns.sh soap.cfg"'
    print
    global MSISDN_STD     # 642101835005 ACTIVE MotorMouth 50.00
    global MSISDN_NON     # 642101835006 DELETED or NOTFOUND
    global MSISDN_LAST5   # 642101838039
    global MSISDN_PKG     # 642101835007 ACTIVE Supa_Prepay 50.00 +FreeBestMate etc.
    global MSISDN_DACTV   # 642101835008 DEACTIVE Supa_Prepay 43.21
    global MSISDN_NEW     # 642101835009 DELETED, used in create/delete test cases
    global RCC_SERIAL_OK
    global RCC_PIN_OK
    global RCC_PIN_USED
    
    #Get config data
    config_file = "swConfig.py"
    if config_file[-3:] == ".py":
        config_file = config_file[:-3]
    data_config = __import__(config_file, globals(), locals(), [])

    MSISDN_STD   = data_config.MSISDN_STD
    MSISDN_NON   = data_config.MSISDN_NON
    MSISDN_LAST5 = data_config.MSISDN_LAST5
    MSISDN_PKG   = data_config.MSISDN_PKG
    MSISDN_DACTV = data_config.MSISDN_DACTV
    MSISDN_NEW   = data_config.MSISDN_NEW
    RCC_SERIAL_OK= data_config.RCC_SERIAL_OK
    RCC_PIN_OK   = data_config.RCC_PIN_OK
    RCC_PIN_USED = data_config.RCC_PIN_USED

    #INPUT_STR = raw_input("hit [Enter] to continue : ")
    print

    
def test_cases_apply_cred_alt():
    print "#                                  #"
    print "# ApplyCreditAlteration Test Cases #"
    print "# - - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    print "test_apply_cred_alt_OK"
    apply_cred_alt(MSISDN_STD, '153', '43.21', '1')
    print "test_apply_cred_alt_ERR_LT_ZERO"
    apply_cred_alt(MSISDN_STD, '153', '-50.05', '1')
    print "test_apply_cred_alt_ERR_INVALID_MSISDN"
    apply_cred_alt('274855959', '8', '50.05', '1')
    print "test_apply_cred_alt_ERR_MSISDN_TOO_LONG"
    apply_cred_alt('2110000000000096666660', '8', '50.05', '1')
    print "test_apply_cred_alt_ERR_INVALID_REASON"
    apply_cred_alt(MSISDN_STD, '987654123154', '50.05', '1')
    print "test_apply_cred_alt_ERR_INVALID_ADJTYPEID"
    apply_cred_alt(MSISDN_STD, '8', '50.05', '99876543')
    print "test_apply_cred_alt_OK_CC_ADJ"
    apply_cred_alt(MSISDN_STD, '8', '50.05', '9')
    print "test_apply_cred_alt_OK_DEBIT_ADJ"
    apply_cred_alt(MSISDN_STD, '8', '99.9901', '3')
    print

   
def test_cases_create_sub():
    print "#                                #"
    print "# CreateSubscription Test Cases  #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print
    print "test_create_sub_MSISDN_INVALID"
    create_sub('211000096211000096211000096')
    print "test_create_sub_MSISDN_EXISTS"
    create_sub(MSISDN_STD)

    print "test_create_sub_MSISDN_MISSING"
    #succeeds in creating a subscriber with MSISDN '64'. 
    #this should be impossible - expect Siebel to prevent it
    #create_sub_complex(MSISDN,TPLAN,LANG,SP,PIN,HOME,IMSI,CREDIT,CREDPER)
    create_sub_complex('','CON3','National','1','0001','18','530011223523448','20.0','90')

    print "test_create_sub_TPLAN_TOO_LONG"
    create_sub_complex(MSISDN_NEW,'CON3WITHEXTRASTUFF','National','1','0001','18','530011223523448','20.0','90')
    print "test_create_sub_TPLAN_MISSING"
    create_sub_complex(MSISDN_NEW,'','National','1','0001','18','530011223523448','20.0','90')
    print "test_create_sub_SP_TOO_LONG"
    create_sub_complex(MSISDN_NEW,'CON3','National','1999999999888888888','0001','18','530011223523448','20.0','90')
    print "test_create_sub_SP_MISSING" 
    create_sub_complex(MSISDN_NEW,'CON3','National','','0001','18','530011223523448','20.0','90')
 
    #print "test_create_sub_SP_INVALID" #OMITTED: SP not validated that way (existing functionality)
    #create_sub_complex(MSISDN_NEW,'CON3','National','1_HELLO','0001','18','530011223523448','20.0','90')
    #print "test_create_sub_LANG_MISSING" #OMITTED: LANG is defaulted to National
    #create_sub_complex(MSISDN_NEW,'CON3','','1','0001','18','530011223523448','20.0','90')

    print "test_create_sub_LANG_TOO_LONG"
    create_sub_complex(MSISDN_NEW,'CON3','National_WITH_EXTRA_STUFF_THAT_MAKES_THE_STRING_WAY_TOO_LONG','1','0001','18','530011223523448','20.0','90')
    print "test_create_sub_PIN_TOO_LONG"
    create_sub_complex(MSISDN_NEW,'CON3','National','1','1999999999888888888','18','530011223523448','20.0','90')
    print "test_create_sub_HOME_TOO_LONG"
    create_sub_complex(MSISDN_NEW,'CON3','National','1','0001','1999999999888888888','530011223523448','20.0','90')
    print "test_create_sub_HOME_INVALID"
    create_sub_complex(MSISDN_NEW,'CON3','National','1','0001','181920','530011223523448','20.0','90')
    print "test_create_sub_CREDIT_INVALID"
    create_sub_complex(MSISDN_NEW,'CON3','National','1','0001','18','530011223523448','-20.0','90')
    
    #print "test_create_sub_CREDPER_INVALID"
    #succeeds in creating a subscriber with Credit expiry date = Today - 90
    #this should be impossible - expect Siebel to prevent it
    #create_sub_complex(MSISDN_NEW,'CON3','National','1','0001','18','530011223523448','20.0','-90')

    print "test_create_sub_OK"
    create_sub(MSISDN_NEW)
    print
    
    
def test_cases_modify_sub():
    print "#                                #"
    print "# ModifySubscription Test Cases  #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    # -- TPLAN --
    # TariffPlan changes
    print "test_modify_sub_TPLAN_OK"
    mod_sub_plan(MSISDN_STD,'BUS_001')
    print "test_modify_sub_TPLAN_MOTORMOUTH_OK"
    mod_sub_plan(MSISDN_STD,'CON3')
    print "test_modify_sub_TPLAN_INVALID"
    mod_sub_plan(MSISDN_STD,'GO_PREPAID')
    print "test_modify_sub_TPLAN_TOO_LONG"
    mod_sub_plan(MSISDN_STD,'GO_PREPAID_WITH_SPOT')
    
    # -- MSISDN --
    print "test_modify_sub_MSISDN_TOO_LONG"
    modify_sub('213001150999999999','BUS_001','1','0001','530011223523448','RESUME')
    print "test_modify_sub_MSISDN_NOT_FOUND" #note, MSISDN_NON should not exist
    modify_sub(MSISDN_NON,'BUS_001','1','0001','530011223523448','RESUME')
    
    # -- TELENO -- (deprecated)
    #print "test_modify_sub_TELENO_TOO_LONG"
    # No applicable use case in Soapwrapper design spec.
    #TeleNo screws things up so I'm taking it out of testModifySubscription.xml
    #modify_sub(MSISDN_STD,'BUS_001','National','1','0001','530011223523448','RESUME','213001150999999999')
    #modify_sub(MSISDN,TPLAN,SP,PIN,IMSI,ACTION)

    # -- LANG --
    print "test_modify_sub_LANG_INVALID"
    mod_sub_lang(MSISDN_STD,'ENGFEMALE')
    print "test_modify_sub_LANG_TOO_LONG"
    mod_sub_lang(MSISDN_STD,'en_01_abcdefghijklmnopqrstuvwxyz')
    print "test_modify_sub_LANG_EN01_OK"
    mod_sub_lang(MSISDN_STD,'en_01')
    print "test_modify_sub_LANG_NATIONAL_OK"
    mod_sub_lang(MSISDN_STD,'National')
    
    # -- ACTION --
    print "test_modify_sub_ACTION_SUSPEND_OK" #bar the subscriber
    mod_sub_action(MSISDN_STD,'SUSPEND')
    print "test_modify_sub_ACTION_RESUME_OK"  #unbar the subscriber
    mod_sub_action(MSISDN_STD,'RESUME')
    print "test_modify_sub_ACTION_RESUMERECHARGE_OK"
    mod_sub_action(MSISDN_STD,'RESUMERECHARGE')
    print "test_modify_sub_ACTION_INVALID"
    mod_sub_action(MSISDN_STD,'EATCAKE')
    print "test_modify_sub_ACTION_TOO_LONG" #long ACTION is not trapped -- just flagged invalid as above.
    mod_sub_action(MSISDN_STD,'RESUMERECHARGE_THIS_ACTION_IS_EXTRA_LONG_WHERE_IS_THE_BYTE_LIMIT')

    # -- PIN -- (deprecated)
    # No applicable use case in Soapwrapper design spec.
    # PIN changes are not passed to the PSL or validated.
    #print "test_modify_sub_PIN_OK"
    #modify_sub(MSISDN_STD,'CON3','1','1337','530011223523448','RESUME')
    #print "test_modify_sub_PIN_TOO_LONG"
    #modify_sub(MSISDN_STD,'CON3','1','26001337','530011223523448','RESUME')

    # -- MTROAM -- (deprecated)
    # No applicable use case in Soapwrapper design spec.
    # MTROAM changes are not passed to the PSL or validated.
    #print "test_modify_sub_MTROAM_ALLOW"
    
    # -- SP -- (deprecated)
    # No applicable use case in Soapwrapper design spec.
    # SP changes are not passed to the PSL or validated.
    # (this test case includes a PIN change which is also deprecated)
    print "test_modify_sub_SP_DEPRECATED"
    modify_sub(MSISDN_STD,'CON3','SP10','1337','530011223523448','RESUME')
    
    # -- SUBSCRIBE -- (deprecated)
    # Obsolescent Logica/INSS data, not required for PSL/Surepay

    # -- IMSI -- (deprecated)
    # No applicable use case in Soapwrapper design spec.
    # IMSI changes are not passed to the PSL or validated.
    #print "test_modify_sub_IMSI_OK" #not passed to the PSL!
    #modify_sub(MSISDN_STD,'CON3','SP10','1337','530011100515400','RESUME')
    #print "test_modify_sub_IMSI_INVALID" #not validated!
    #modify_sub(MSISDN_STD,'CON3','SP10','1337','X30011223523448','RESUME')
    print "test_modify_sub_IMSI_TOO_LONG"
    modify_sub(MSISDN_STD,'CON3','SP10','1337','9930011223523448','RESUME')
    print 


def test_cases_delete_sub():
    print "#                                #"
    print "# DeleteSubscription Test Cases  #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    print "test_delete_sub_MSISDN_TOO_LONG"
    delete_sub('213001150999999999')
    print "test_delete_sub_MSISDN_NOT_FOUND"
    delete_sub(MSISDN_NON)
    # The following tests are redundant -- there's no such validation. 
    #print "test_delete_sub_MSISDN_BAD_PREFIX_64021" 
    #print "test_delete_sub_MSISDN_BAD_PREFIX_646421"
    #print "test_delete_sub_MSISDN_DEACTIVE"
    #print "test_delete_sub_MSISDN_PREACTIVE"
    print "test_delete_sub_MSISDN_BLANK"  # may actually work, if subscriber created wit hblank msisdn.
    delete_sub('')                        # assume that Siebel won't allow this
    print "test_delete_sub_OK"
    delete_sub(MSISDN_NEW)
    print


def test_cases_query_cdredr():
    print "#                                #"
    print "#    QueryCDREDRs Test Cases     #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    print "test_query_cdredr_OK"
    query_cdredr(MSISDN_LAST5)
    print "test_query_cdredr_MSISDN_TOO_LONG"
    query_cdredr('213001150999999999')
    print "test_query_cdredr_MSISDN_NOT_FOUND"
    query_cdredr(MSISDN_NON)
    print "test_query_cdredr_NODATA_OK"
    query_cdredr(MSISDN_STD)             #function also returns OK when no CDRs returned 
    print


def test_cases_query_recharge_card():
    print "#                                #"
    print "#    QueryRecharge Test Cases    #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    # -- Recharge Card --
    print "test_query_rech_card_OK"
    query_rech_card('0000000312-00189')
    print "test_query_rech_card_INVALID"
    query_rech_card('100000-00312-00189')
    print "test_query_rech_card_NUM_TOO_LONG"
    query_rech_card('1234567890123456789012345678901234567890-00000-00312-00189')
    
    # -- Recharge Card Type --
    print "test_query_rech_card_type_50_OK"   
    query_rech_card_type('$50') 
    print "test_query_rech_card_type_20_OK"   
    query_rech_card_type('$20') 
    print "test_query_rech_card_type_LEGACY"
    query_rech_card_type('RC-20-CARD-CC')
    
    # -- Recharge Card Batch --          #deprecated function, always returns OK
    print "test_query_rech_card_batch_OK"
    query_rech_card_batch(RCC_SERIAL_OK)
    print "test_query_rech_card_batch_INVALID"
    query_rech_card_batch('') 
    print
    

def test_cases_query_subscription():
    print "#                                #"
    print "#  QuerySubscription Test Cases  #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    print "test_query_sub_OK"
    query_sub(MSISDN_STD)
    print "test_query_sub_MSISDN_INVALID"
    query_sub('213001150999999999')
    print "test_query_sub_MSISDN_NOT_FOUND"
    query_sub(MSISDN_NON)
    print
    
    
def test_cases_use_recharge():    
    print "#                                #"
    print "#   UseRechargecard Test Cases   #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    print "test_use_recharge_CARD_INVALID"
    use_rech_card(MSISDN_STD,'156135-0001-0001')
    print "test_use_recharge_CARD_USED"
    use_rech_card(MSISDN_STD,RCC_PIN_USED)
    print "test_use_recharge_MSISDN_NOT_FOUND"
    use_rech_card(MSISDN_NON,RCC_PIN_USED)
    print "test_use_recharge_OK"
    use_rech_card(MSISDN_STD,RCC_PIN_OK)
    print
    
    
def test_cases_query_resources():
    print "#                                #"
    print "#   QueryResources Test Cases    #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    print "test_query_resources_OK"
    query_resources(MSISDN_PKG)


def test_cases_num_portability():
    print "#                                #"
    print "# Number Portability Test Cases  #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    print "test_port_in_OK"
    change_msisdn(MSISDN_STD,'274319682')
    print "--check that " + MSISDN_STD + " is no longer valid"
    query_sub(MSISDN_STD)
    print "--check that 64274319682 is now valid"
    query_sub('274319682')
    print "--reset data"
    change_msisdn('274319682',MSISDN_STD)
    print "test_port_in_ERROR_TARGMSISDN_DEACTIVE"
    change_msisdn(MSISDN_DACTV,'274319682')
    print "test_port_in_ERROR_BOTH_EXIST"
    change_msisdn(MSISDN_STD,MSISDN_PKG)
    print


def test_cases_change_msisdn():
    print "#                                #"
    print "#    ChangeMsisdn Test Cases     #"
    print "# - - - - - - - - - - - - - - -  #"
    INPUT_STR = raw_input("hit [Enter] to continue : ")
    print 
    print "test_change_msisdn_OK"
    change_msisdn(MSISDN_STD,MSISDN_NON)
    print "--reset data"
    change_msisdn(MSISDN_NON,MSISDN_STD)
    print "test_change_msisdn_NOT_FOUND"
    change_msisdn(MSISDN_NON,MSISDN_STD)
    print "test_change_msisdn_INVALID"
    change_msisdn('',MSISDN_NON)
    print "test_change_msisdn_NEWMSISDN_NULL"
    change_msisdn(MSISDN_STD,'')
    #print "test_change_msisdn_IMSI_NULL" #--imsi, reason fields not used.
    print "test_change_msisdn_OLDMSISDN_TOO_LONG"
    change_msisdn('213001150999999999',MSISDN_NON)
    print "test_change_msisdn_NEWMSISDN_TOO_LONG"
    change_msisdn(MSISDN_STD,'213001150999999999')
    print "test_change_msisdn_EXISTS"
    change_msisdn(MSISDN_STD,MSISDN_PKG)
    print "test_change_msisdn_SAME"
    change_msisdn(MSISDN_STD,MSISDN_STD)
    print


main()
sys.exit(0)

