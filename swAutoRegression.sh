#!/bin/sh
# SOAPWrapper automated regression test

ME=swAutoRegression
INSTANCE=host3
[ $1 ] && { INSTANCE=$1 ; }
if [ $INSTANCE != host3 ] && [ $INSTANCE != host4 ]
then 
  echo "$INSTANCE is not a valid SOAPWrapper instance for this script"
  echo "Valid instances are host3 or host4."
  echo
  exit 1
fi
NOW=`date +"%Y%m%d.%H%M%S"`
LOGFILE=log/log.$ME.$NOW

#BSLFILE = baseline for comparison
BSLFILE=$ME.bsl
DIFFILE=log/dif.$ME.$NOW

main()
{
  echo "Using SOAPWrapper instance: $INSTANCE"
  echo 
  echo "$NOW Started test" 
  python -u swHarness.py auto

  NOW2=`date +"%Y%m%d.%H%M%S"`
  echo "$NOW2 Finished" 
  echo "================================" 
  echo
  diffcount=`sdiff -s $BSLFILE $LOGFILE | wc -l | awk '{print $1}'`
  echo "$diffcount differences found."
  echo
  echo "Diff file : $DIFFILE"
  echo "Log file : $LOGFILE"
  echo "Baseline : $BSLFILE"
  sdiff -w200 $BSLFILE $LOGFILE > $DIFFILE
  echo
  echo "To compare results with Vimdiff, type this command:"
  echo "  vimdiff $BSLFILE $LOGFILE"
  echo
  echo "done."
}

main $@ | tee -a $LOGFILE

