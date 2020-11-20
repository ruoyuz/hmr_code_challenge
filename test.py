#!/usr/bin/env python3
"""Unit test cases for ETL functions."""

import unittest
import datetime

from models import ItunesSubscription

from etl_util import (
    SubscriptionStatus,
    validate_subscription,
    get_trial_start_date,
    get_subscription_start_date,
    get_expiration_date,
    get_current_status,
    update_subscription_details,
)


class TestEtlUtil(unittest.TestCase):
    def setUp(self):
        # TODO: rewrite to use a factory
        self.transaction_factory = {
            "trial_only": {
                "purchase_date_ms": "1520176996000",
                "expires_date_ms": "1522851796000",
                "is_trial_period": "true",
            },
            "subscription_only": {
                "purchase_date_ms": "1577836800000",
                "expires_date_ms": "1583020800000",
                "is_trial_period": "false",
            },
        }

        self.validation_set = set(
            ("purchase_date_ms", "expires_date_ms", "is_trial_period")
        )

        self.subscription = ItunesSubscription(
            id="subscription_1",
            transactions=[],
            trial_start_date=None,
            subscription_start_date=None,
            expiration_date=None,
            current_status=None,
        )

    def test_validate_subscription__valid(self):
        self.subscription.transactions = [self.transaction_factory.get("trial_only")]
        self.assertEqual(
            validate_subscription(self.subscription, self.validation_set), True
        )

    def test_validate_subscription__no_transactions(self):
        self.subscription.transactions = []
        self.assertRaises(
            ValueError, validate_subscription, self.subscription, self.validation_set
        )

    def test_validate_subscription__missing_field(self):
        self.validation_set.add("some_random_field")
        self.assertRaises(
            ValueError, validate_subscription, self.subscription, self.validation_set
        )

    def test_get_trial_start_date__trial_only(self):
        self.subscription.transactions = [self.transaction_factory.get("trial_only")]
        self.assertTrue(get_trial_start_date(self.subscription.transactions) != None)

    def test_get_trial_start_date__subscription_only(self):
        self.subscription.transactions = [
            self.transaction_factory.get("subscription_only")
        ]
        self.assertTrue(get_trial_start_date(self.subscription.transactions) == None)

    def test_get_trial_start_date__has_both(self):
        self.subscription.transactions = [
            self.transaction_factory.get("trial_only"),
            self.transaction_factory.get("subscription_only"),
        ]
        self.assertTrue(get_trial_start_date(self.subscription.transactions) != None)

    def test_get_subscription_start_date__trial_only(self):
        self.subscription.transactions = [self.transaction_factory.get("trial_only")]
        self.assertTrue(
            get_subscription_start_date(self.subscription.transactions) == None
        )

    def test_get_subscription_start_date__subscription_only(self):
        # TODO: is subscription only without trial a valid business case?
        self.subscription.transactions = [
            self.transaction_factory.get("subscription_only")
        ]
        self.assertTrue(
            get_subscription_start_date(self.subscription.transactions) == None
        )

    def test_get_subscription_start_date__has_both(self):
        self.subscription.transactions = [
            self.transaction_factory.get("trial_only"),
            self.transaction_factory.get("subscription_only"),
        ]
        self.assertTrue(
            get_subscription_start_date(self.subscription.transactions) != None
        )

    def test_get_expiration_date__trial_only(self):
        self.subscription.transactions = [self.transaction_factory.get("trial_only")]
        self.assertTrue(get_expiration_date(self.subscription.transactions) != None)

    def test_get_expiration_date__subscription_only(self):
        self.subscription.transactions = [
            self.transaction_factory.get("subscription_only")
        ]
        self.assertTrue(get_expiration_date(self.subscription.transactions) != None)

    def test_get_expiration_date__has_both(self):
        self.subscription.transactions = [
            self.transaction_factory.get("trial_only"),
            self.transaction_factory.get("subscription_only"),
        ]
        self.assertTrue(get_expiration_date(self.subscription.transactions) != None)

    def test_get_current_status__active_trial(self):
        now = datetime.datetime.strptime("2020-11-01", "%Y-%m-%d")
        trial_start_date = datetime.datetime.strptime("2020-10-01", "%Y-%m-%d")
        subscription_start_date = None
        expiration_date = datetime.datetime.strptime("2020-12-01", "%Y-%m-%d")

        current_status = get_current_status(
            now, trial_start_date, subscription_start_date, expiration_date
        )
        self.assertEqual(current_status, SubscriptionStatus.active_trial)

    def test_get_current_status__expired_trial(self):
        now = datetime.datetime.strptime("2020-11-01", "%Y-%m-%d")
        trial_start_date = datetime.datetime.strptime("2020-10-01", "%Y-%m-%d")
        subscription_start_date = None
        expiration_date = datetime.datetime.strptime("2020-10-31", "%Y-%m-%d")

        current_status = get_current_status(
            now, trial_start_date, subscription_start_date, expiration_date
        )
        self.assertEqual(current_status, SubscriptionStatus.expired_trial)

    def test_get_current_status__active_subscription(self):
        now = datetime.datetime.strptime("2020-11-01", "%Y-%m-%d")
        trial_start_date = datetime.datetime.strptime("2020-10-01", "%Y-%m-%d")
        subscription_start_date = datetime.datetime.strptime("2020-10-31", "%Y-%m-%d")
        expiration_date = datetime.datetime.strptime("2020-12-01", "%Y-%m-%d")

        current_status = get_current_status(
            now, trial_start_date, subscription_start_date, expiration_date
        )
        self.assertEqual(current_status, SubscriptionStatus.active_subscription)

    def test_get_current_status__expired_subscription(self):
        now = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")
        trial_start_date = datetime.datetime.strptime("2020-10-01", "%Y-%m-%d")
        subscription_start_date = datetime.datetime.strptime("2020-10-31", "%Y-%m-%d")
        expiration_date = datetime.datetime.strptime("2020-12-01", "%Y-%m-%d")

        current_status = get_current_status(
            now, trial_start_date, subscription_start_date, expiration_date
        )
        self.assertEqual(current_status, SubscriptionStatus.expired_subscription)

    def test_get_current_status__invalid_status(self):
        # TODO: is subscription only without trial a valid business case?
        # if a subscription only has one non-trial transaction, we will get something like this
        now = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")
        trial_start_date = None
        subscription_start_date = None
        expiration_date = datetime.datetime.strptime("2020-12-01", "%Y-%m-%d")

        self.assertRaises(
            ValueError,
            get_current_status,
            now,
            trial_start_date,
            subscription_start_date,
            expiration_date,
        )

    def test_update_subscription_details__valid(self):
        self.subscription.transactions = [
            self.transaction_factory.get("trial_only"),
            self.transaction_factory.get("subscription_only"),
        ]
        subscription = update_subscription_details(self.subscription)
        self.assertTrue(subscription.id != None)
        self.assertTrue(subscription.transactions != None)
        self.assertTrue(subscription.trial_start_date != None)
        self.assertTrue(subscription.subscription_start_date != None)
        self.assertTrue(subscription.expiration_date != None)
        self.assertTrue(subscription.current_status != None)


if __name__ == "__main__":
    unittest.main()
