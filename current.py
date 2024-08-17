#!/usr/bin/python3

import sys
import yaml
from argparse import ArgumentParser, Namespace

CONFIG_FILE_NAME=".spend-analyzer.yaml"

# parse command line options
def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Calculate account balance.")

    parser.add_argument(
        "--all", action="store_true", help="Do all accounts, including the kids."
    )
    parser.add_argument(
        "--today", action="store_true", help="Only until today, not future entries."
    )
    parser.add_argument(
        "--until-date", action="store", type=str, help="Calculate until given date."
    )
    parser.add_argument("--no-total", action="store_true", help="Don't display totals.")
    parser.add_argument(
        "--hide-skipped",
        action="store_true",
        help="Show the lines that are skipped due to UNTIL_DATE.",
    )
    parser.add_argument(
        "--files", action="append", type=str, help="File names to work on."
    )

    args = parser.parse_args()

    # if they want to get the total until today, get a date string for tomorrow
    if args.today:
        from datetime import date, timedelta

        oneDay = timedelta(days=1)
        args.until_date = (date.today() + oneDay).isoformat()

    return args


def parse_configuration() -> yaml:

    with open(CONFIG_FILE_NAME, "r") as configfile:
        config = yaml.safe_load(configfile)

    return config


def get_accounts(config: yaml, args: ArgumentParser) -> list[str]:
    accounts: tuple[str, str, bool] = []
    max_label_length = 0
    for key, value in config.get("accounts").items():
        filename = value.get("filename", key)

        if not args.files or filename in args.files:
            if not value.get("hidden", False) or args.all:
                accounts.append(
                    (
                        filename,
                        value.get("label", filename),
                        value.get("debit", True),
                    )
                )
                max_label_length = max(max_label_length, len(value.get("label")))
    return accounts, max_label_length


# main routine that does all of the work
def main():
    config = parse_configuration()
    args = parse_arguments()
    total = 0

    fileDir = config.get("directory")

    # get the accounts the user wants to summarize
    accounts, max_label_length = get_accounts(config, args)

    # set up the labels for displaying to the screen
    max_label_length += 2
    format_str = f"{{0:{max_label_length}}}: {{1:10.2f}}"
    format_str_sep = f"{{0:{max_label_length}}}: {{1:10}}"

    # loop over the accounts
    for account in accounts:
        ftotal = 0
        with open(f"{fileDir}/{account[0]}", "r") as inf:
            # loop over the file
            for line in inf:
                # get the first field which is the dollar value
                s = line.split()

                # skip comment lines
                if len(s) > 0 and s[0] == "0":
                    continue

                # check and make sure that this line isn't greater than the until_date
                if args.until_date and len(s) > 1 and s[1] > args.until_date:
                    if not args.hide_skipped:
                        print("Skipping ", line.strip())
                    continue

                # try and add the first field to the total
                try:
                    ftotal = round(float(s[0]) + ftotal, 2)
                except:
                    pass

        # print out the file total
        print(format_str.format(account[1], round(ftotal, 2)))
        if account[2] == 1:
            total += ftotal
        elif account[2] == -1:
            total -= ftotal

    if not args.no_total:
        # print out the complete total
        print(format_str_sep.format("___________", "__________"))
        print(format_str.format("Total", total))


if __name__ == "__main__":
    main()
