# Spend Analyzer

These scripts are used to show the current value of your various
accounts. They do require you to input every transaction

## Configuration

There must exist a file called .spend-analyzer.config which is in yaml
format. Included is an example file showing a few accounts

### directory

Location where your data files are located

### accounts

Listing of accounts and their configuration. Each account must have a
unique key/name

#### filename

Override for the account name/key in case the filename is different from
the key used

#### label

Label to be used when printing the total

#### debit

Whether this account is a loan or credit card

#### hidden

Whether this account should be shown by default

## Scripts

There are scripts to total up the current accounts, add new values into
each data file, and handle calls from crontab to add new values into the
data files

### current.py

This script allows you to get the totals of your accounts at any day in
time and for the accounts that you want to see

### lt.sh

This file does the data entry of spending or depositing funds. This does
support some tab completion, but that portion is not currently included
in the repo

### crontabMoney.sh

This is a script that should be called by cron at specified date/times
to do recurring entries such as cable bills and loan interest. Also
supports a special case for a transfer from one account to another