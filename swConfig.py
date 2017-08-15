#!/usr/bin/env python
#SoapWrapper Test Harness config data
SWHOST='127.0.0.1'
SWPORT=6060

#these MSISDNs should not need to be changed.
#note that SoapWrapper expects MSISDN *WITHOUT* 64 prefix

MSISDN_STD   = '2101835005'  #basic subscriber (originally 2101835313)
MSISDN_NON   = '2101835006'  #MSISDN should not exist (was 210031415)
MSISDN_LAST5 = '2101838039'  #includes last 5 call data
MSISDN_PKG   = '2101835007'  #has packages, FCNs
MSISDN_DACTV = '2101835008'  #deactive 

#these Recharge cards should not need to be changed.
#CardSerialNumber=0000000312-00119 CardPin=396679374739 -- OK
#CardSerialNumber=0000000312-00120 CardPin=211899934825 -- USED
RCC_SERIAL_OK = '0000000312-00119' 
RCC_PIN_OK = '396679374739'
RCC_PIN_USED  = '211899934825'

#increment this number
#for testing createSub/deleteSub -- range is 2101835170 to 2101835189
#-------EDIT THIS VALUE-------
MSISDN_NEW   = '2101835170' 
#-----------------------------
