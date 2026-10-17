"""Offline example using the public implementation; see README for evidence scope."""
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
os.chdir(ROOT)

import sqlite3
from pathlib import Path
# Fictional rows deliberately include two stations on the same date.
db = sqlite3.connect(':memory:')
db.execute('PRAGMA foreign_keys=ON')
db.executescript(Path('sql/warehouse.sql').read_text())
db.execute("INSERT INTO dim_business VALUES ('b1','Example business','station1')")
db.execute("INSERT INTO dim_customer VALUES ('c1')")
db.execute("INSERT INTO dim_date VALUES ('2024-01-01',2024,1)")
db.execute("INSERT INTO dim_weather VALUES ('w1','station1','2024-01-01',80,60,0)")
db.execute("INSERT INTO dim_weather VALUES ('w2','station2','2024-01-01',20,10,1)")
db.execute("INSERT INTO fact_review VALUES ('r1','b1','c1','2024-01-01',4)")
result = {'matched_max_temperature_f': db.execute('SELECT max_temp_f FROM review_weather').fetchone()[0], 'monthly_summary': db.execute('SELECT review_count,average_stars,reviews_with_temperature FROM monthly_review_summary').fetchone()}
db.close()

import json
print(json.dumps(result, indent=2))

