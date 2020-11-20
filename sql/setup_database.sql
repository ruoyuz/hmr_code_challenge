-- create database --
CREATE DATABASE subscription;

COMMENT ON DATABASE subscription
    IS 'Database for user subscriptions.';

-- create role --
CREATE ROLE homer LOGIN ENCRYPTED PASSWORD 'password' NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;

GRANT CONNECT ON DATABASE subscription TO homer;

-- connect to database --
\connect subscription;

-- create table --
CREATE TABLE public.itunes_subscription (
    id VARCHAR(64) NOT NULL,
    transactions JSONB NOT NULL,
    trial_start_date TIMESTAMPTZ,
    subscription_start_date TIMESTAMPTZ,
    expiration_date TIMESTAMPTZ NOT NULL,
    current_status VARCHAR(64) NOT NULL,

    PRIMARY KEY(id)
);

COMMENT ON TABLE public.itunes_subscription
    IS 'Itunes subscription';

COMMENT ON COLUMN public.itunes_subscription.id
    IS 'Id: unique identifier for a subscription, should not change for the lifetime';

COMMENT ON COLUMN public.itunes_subscription.transactions
    IS 'Transactions: a list of transactions in a subscription, usually in json format';

COMMENT ON COLUMN public.itunes_subscription.trial_start_date
    IS 'Trial start date: purchase_date for the transaction where is_trial_period is true';

COMMENT ON COLUMN public.itunes_subscription.subscription_start_date
    IS 'Subscription start date: purchase_date for the transaction immediately following a trial transaction';

COMMENT ON COLUMN public.itunes_subscription.expiration_date
    IS 'Expiration date: expires_date of the last transaction';

COMMENT ON COLUMN public.itunes_subscription.current_status
    IS 'Current status: could be Active Trial / Expired Trial / Active Subscription / Expired Subscription';

-- grant crud operations to homer --
GRANT INSERT, UPDATE, DELETE, SELECT ON ALL TABLES IN SCHEMA public to homer;
