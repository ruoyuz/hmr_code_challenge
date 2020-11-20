"""Utilities for ETL process."""

import json
import datetime
from enum import Enum
from typing import List
from collections import OrderedDict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import ItunesSubscription


class SubscriptionStatus(Enum):
    """Enums for subscription status."""

    def __str__(self):
        return str(self.value)

    active_trial = "Active Trial"
    expired_trial = "Expired Trial"
    active_subscription = "Active Subscription"
    expired_subscription = "Expired Subscription"


def check_dict_duplicates(pairs) -> OrderedDict:
    """Reject duplicated keys when parsing json."""
    res_dict = OrderedDict()
    for key, val in pairs:
        if key in res_dict:
            raise ValueError("duplicated key found: %s" % (key,))
        else:
            res_dict[key] = val
    return res_dict


def validate_subscription(subscription: ItunesSubscription, field_validation_set: set):
    """Validate data format (transactions) in a subscription."""
    id = subscription.id
    transactions = subscription.transactions

    # transactions should have at least one record
    if not transactions:
        raise ValueError("Empty transaction for subscription: id=%s" % (id,))

    # each transaction should contain exact fields in field_validation_set
    for tx in transactions:
        if set(tx.keys()) != field_validation_set:
            raise ValueError("Invalid transaction found in subscription: id=%s" % (id,))


def read_subscription_file(filename: str) -> List[ItunesSubscription]:
    """Read the json data file and return a list of data model objects."""
    with open(filename, "r") as f_data:
        data = json.load(f_data, object_pairs_hook=check_dict_duplicates)

    subscriptions = []
    for id, transactions in data.items():
        sub = ItunesSubscription(id=id, transactions=transactions)
        subscriptions.append(sub)

    return subscriptions


def get_trial_start_date(transactions: list) -> datetime.datetime:
    """Get trial start date from the trial transaction."""
    trial_tx = list(filter(lambda t: t["is_trial_period"] == "true", transactions))
    if trial_tx:
        ts_seconds = int(trial_tx[0]["purchase_date_ms"]) / 1000.0
        dt = datetime.datetime.fromtimestamp(ts_seconds)
        return dt
    else:
        return None


def get_subscription_start_date(transactions: list) -> datetime.datetime:
    """Get subscription start date from the first non-trial transaction."""
    for trial, subs in zip(transactions[::2], transactions[1::2]):
        if trial["is_trial_period"] == "true" and subs["is_trial_period"] == "false":
            ts_seconds = int(subs["purchase_date_ms"]) / 1000.0
            dt = datetime.datetime.fromtimestamp(ts_seconds)
            return dt
    return None


def get_expiration_date(transactions: list) -> datetime.datetime:
    """Get trial/subscription expiration date from the latest transaction."""
    ts_seconds = int(transactions[-1]["expires_date_ms"]) / 1000.0
    dt = datetime.datetime.fromtimestamp(ts_seconds)
    return dt


def get_current_status(
    now: datetime.datetime,
    trial_start_date: datetime.datetime,
    subscription_start_date: datetime.datetime,
    expiration_date: datetime.datetime,
) -> SubscriptionStatus:
    """Decide current subscription status according to dates."""
    if subscription_start_date:
        if expiration_date > now:
            return SubscriptionStatus.active_subscription
        return SubscriptionStatus.expired_subscription

    elif trial_start_date:
        if expiration_date > now:
            return SubscriptionStatus.active_trial
        return SubscriptionStatus.expired_trial

    else:
        raise ValueError(
            "Could not find a valid status: trial: %s, subs: %s, exp: %s"
            % (trial_start_date, subscription_start_date, expiration_date),
        )


def update_subscription_details(subscription: ItunesSubscription) -> ItunesSubscription:
    """Enrich the subscription entity with calculated details."""
    transactions = subscription.transactions

    # get trial_start_date
    subscription.trial_start_date = get_trial_start_date(transactions)

    # get subscription_start_date
    subscription.subscription_start_date = get_subscription_start_date(transactions)

    # get expiration_date
    subscription.expiration_date = get_expiration_date(transactions)

    # get current status
    now = datetime.datetime.now()
    current_status_enum = get_current_status(
        now,
        subscription.trial_start_date,
        subscription.subscription_start_date,
        subscription.expiration_date,
    )

    subscription.current_status = current_status_enum.value

    return subscription


def save_to_database(subscriptions: list, database_uri: str):
    """Save (upsert) subscriptions to database."""
    # database config
    engine = create_engine(database_uri)
    Session = sessionmaker(bind=engine)
    session = Session()

    for sub in subscriptions:
        session.merge(sub)

    session.commit()
    session.close()
