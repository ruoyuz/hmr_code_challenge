# HOMER code challenge
A Code challenge for a data task.

The goal is to process a data file in json format, extract some field information, calculate metadata, and persist the outcome in a PostgreSQL database. To serve this purpose, components for the Python processing script are created:

* `models.py` as the object relational mapping for data model in the table
* `etl_utl.py` as the utility library for the workflow
* `config.py` as the store for configuration items
* `test.py` as the unit test set for utility functions
* `entry.py` as the entry point to contain the business logic

The data file is not included in this repo.

The project uses `pipenv` to manage Python environment. A `requirements.txt` file is also provided if the user prefers using `pip` alone for installing dependencies.

### Setup

* Clone this repo to your local: `git clone https://github.com/ruoyuz/hmr_code_challenge`.
* Change working directory of the terminal to the repo directory.
* Install Python dependencies with `pipenv install`.
* Run `sql/setup_database.sql` in your PostgreSQL to create the database, role, and table. Modify the file if you need to change the credentials.
* Modify `config.py` with the target data file and your database configurations.

## Usage

* Invoke the script with `pipenv run python3 ./entry.py` to start processing the data file.
* Alternatively, without saving to the database, you can test run the script with `pipenv run python3 ./entry.py --test`. Processing result will be printed in the terminal.
* Run `sql/list_status.sql` in your PostgreSQL client to list number of subscriptions in each status.

