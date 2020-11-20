# HOMER code challenge
A Code challenge for a data task.

The goal is to process a data file in json format, extract some field information, calculate metadata, and persist the outcome in a PostgreSQL database. To serve this purpose, components for the Python processing script are created:

1. `models.py` as the object relational mapping for data model in the table
2. `etl_utl.py` as the utility library for the workflow
3. `config.py` as the store for configuration items
4. `test.py` as the unit test set for utility functions
5. `entry.py` as the entry point to contain the business logic

The data file is not included in this repo.

The project uses `pipenv` to manage Python environment. A `requirements.txt` file is also provided if the user prefers using `pip` alone for installing dependencies.

### Setup

1. Clone this repo to your local: `git clone https://github.com/ruoyuz/hmr_code_challenge`.
2. Change working directory of the terminal to the repo directory.
3. Install Python dependencies with `pipenv install`.
4. Run `sql/setup_database.sql` in your PostgreSQL to create the database, role, and table. Modify the file if you need to change the credentials.
5. Modify `config.py` with the target data file and your database configurations.

## Usage

1. Invoke the script with `pipenv run python3 ./entry.py` to start processing the data file.
2. Alternatively, without saving to the database, you can test run the script with `pipenv run python3 ./entry.py --test`. Processing result will be printed in the terminal.
3. Run `sql/list_status.sql` in your PostgreSQL client to list number of subscriptions in each status.

