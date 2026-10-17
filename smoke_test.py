import sqlite3
from pathlib import Path
db=sqlite3.connect(':memory:');db.execute('PRAGMA foreign_keys=ON');db.executescript(Path('sql/warehouse.sql').read_text())
db.execute("INSERT INTO dim_business VALUES ('b1','Example business','station1')")
db.execute("INSERT INTO dim_customer VALUES ('c1')")
db.execute("INSERT INTO dim_date VALUES ('2024-01-01',2024,1)")
db.execute("INSERT INTO dim_weather VALUES ('w1','station1','2024-01-01',80,60,0)")
db.execute("INSERT INTO dim_weather VALUES ('w2','station2','2024-01-01',20,10,1)")
db.execute("INSERT INTO fact_review VALUES ('r1','b1','c1','2024-01-01',4)")
assert db.execute('SELECT max_temp_f FROM review_weather').fetchone()[0]==80
assert db.execute('SELECT review_count,average_stars FROM monthly_review_summary').fetchone()==(1,4.)
try:db.execute("INSERT INTO fact_review VALUES ('r2','b1','c1','2024-01-01',9)")
except sqlite3.IntegrityError:pass
else:raise AssertionError('Invalid rating accepted')
db.close();print('Dimension/fact integrity, geographic weather join, monthly aggregation, and rating bounds passed on SQLite.')
