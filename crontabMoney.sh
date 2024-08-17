#!/bin/sh

MONEY=$1;
FILE=$2;
shift 2;

# get a date for the transaction in case we use it more than once
tDate=$(/bin/date -Is);

if [ $FILE != 'loan' -a $FILE != 'transfer' ]; then
	echo $MONEY $tDate $* >> $FILE;
elif [ $FILE = 'transfer' ]; then
	TO=$1
	FROM=$2
	DATE_CODE=$3
	if [ -z "${DATE_CODE##*-*}" ]; then
		DATE_CODE=$(date -Is --date=${DATE_CODE});
		echo -$MONEY $DATE_CODE transfer to $TO >> $FROM
		echo $MONEY $DATE_CODE transfer from $FROM >> $TO
	else
		echo -$MONEY $tDate transfer to $TO $DATE_CODE >> $FROM
		echo $MONEY $tDate transfer from $FROM $DATE_CODE >> $TO
	fi
else
	# get to the money directory to make this easier
	cd $(dirname $0);
	# get the loan file, the transaction file, and the escrow amount
	interest=$1;
	LFILE=$2;
	TFILE=$3;
	escrow=$4;
	# clear these
	shift 4;

	# use current to get the balance of the loan as of now
	balance=$(./current --today --hide --files=$LFILE | grep $LFILE | cut -f 2 -d :);
	# calculate the interest accrued
	interest=$(python3 -c "print(round($balance*$interest/100/12,2))");

	# now add the breakout of payment, interest, and escrow
	echo >> $LFILE;
	echo $MONEY $tDate $* home payment >> $LFILE;
	echo $interest $tDate $* interest >> $LFILE;
	echo $escrow $tDate $* escrow >> $LFILE;

	# PLus the payment to the transaction file
	echo $MONEY $tDate $* home payment >> $TFILE;
fi
