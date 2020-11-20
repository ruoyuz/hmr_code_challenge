"""Configuration items for the ETL script."""

# ETL config
ETL_FILENAME = "data.json"
ETL_TRANSACTION_FIELDS = (
    "quantity",
    "product_id",
    "transaction_id",
    "original_transaction_id",
    "purchase_date",
    "purchase_date_ms",
    "purchase_date_pst",
    "original_purchase_date",
    "original_purchase_date_ms",
    "original_purchase_date_pst",
    "expires_date",
    "expires_date_ms",
    "expires_date_pst",
    "web_order_line_item_id",
    "is_trial_period",
    "is_in_intro_offer_period",
)

# database config
USERNAME = "homer"
PASSWORD = "password"
IP_ADDRESS = "127.0.0.1"
PORT = "5432"
DATABASE_NAME = "subscription"
# scheme: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{IP_ADDRESS}:{PORT}/{DATABASE_NAME}"

# logging config
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOGGING_DATEFMT = "%Y-%m-%d %H:%M:%S"
