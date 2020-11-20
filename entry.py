#!/usr/bin/env python3
"""ETL entry script for processing data.json."""

import logging
import sys
import functools
import argparse

from config import (
    DATABASE_URI,
    ETL_FILENAME,
    ETL_TRANSACTION_FIELDS,
    LOGGING_FORMAT,
    LOGGING_DATEFMT,
)

from etl_util import (
    read_subscription_file,
    validate_subscription,
    update_subscription_details,
    save_to_database,
)

if __name__ == "__main__":
    # config arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test",
        help="execute a test run to print out result without saving to database",
        action="store_true",
    )
    args = parser.parse_args()

    # config logging
    logging.basicConfig(
        level=logging.INFO,
        format=LOGGING_FORMAT,
        datefmt=LOGGING_DATEFMT,
    )

    # read file and hanlde errors
    logging.info("Reading file: %s", ETL_FILENAME)
    try:
        subscriptions = read_subscription_file(ETL_FILENAME)
        logging.info("Record amount in the file: %d", len(subscriptions))
    except Exception as exc:
        logging.error("Some other error happened: %s", exc)
        sys.exit(1)

    # validate subscriptions
    # Exception will be raised if any transaction is invalid
    logging.info("Validating subscriptions...")
    fields_set = set(ETL_TRANSACTION_FIELDS)
    map(
        functools.partial(validate_subscription, field_validation_set=fields_set),
        subscriptions,
    )

    # update details to subscriptions
    logging.info("Enriching details to subscriptions...")
    subscriptions = map(update_subscription_details, subscriptions)

    if args.test:
        for sub in subscriptions:
            logging.info("----")
            logging.info("Subscription ID: %s", sub.id)
            logging.info("Trial start date: %s", sub.trial_start_date)
            logging.info("Subscription start date: %s", sub.subscription_start_date)
            logging.info("Expiration date: %s", sub.expiration_date)
            logging.info("Current status: %s", sub.current_status)
    else:
        # save to database
        logging.info("Saving to database...")
        save_to_database(subscriptions, DATABASE_URI)

    logging.info("Done.")
