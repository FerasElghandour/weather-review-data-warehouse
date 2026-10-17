# Validation

Run `python smoke_test.py` for the included offline behavior checks. These use synthetic inputs or an in-memory database. They do not recertify historical benchmark metrics or test a live external service.

The portable schema is exercised on SQLite. It does not certify a live Snowflake ingestion or cloud warehouse deployment.

## Executed checks — October 17, 2026

Dimension/fact integrity, geographic weather join, monthly aggregation, and rating bounds passed on SQLite.

Executed locally on Python 3.14.3. The hosted workflow repeats these checks on Python 3.12.
