-- Portable analytical warehouse core. Input values are supplied by the operator.
CREATE TABLE dim_business (business_id VARCHAR(64) PRIMARY KEY, name VARCHAR(200) NOT NULL, station_id VARCHAR(64) NOT NULL);
CREATE TABLE dim_customer (customer_id VARCHAR(64) PRIMARY KEY);
CREATE TABLE dim_date (date_key DATE PRIMARY KEY, year INTEGER NOT NULL, month INTEGER NOT NULL CHECK(month BETWEEN 1 AND 12));
CREATE TABLE dim_weather (
 weather_id VARCHAR(100) PRIMARY KEY, station_id VARCHAR(64) NOT NULL,
 date_key DATE NOT NULL REFERENCES dim_date(date_key), max_temp_f REAL, min_temp_f REAL,
 precipitation_inch REAL CHECK(precipitation_inch IS NULL OR precipitation_inch >= 0),
 UNIQUE(station_id,date_key), CHECK(max_temp_f IS NULL OR min_temp_f IS NULL OR max_temp_f>=min_temp_f)
);
CREATE TABLE fact_review (
 review_id VARCHAR(64) PRIMARY KEY, business_id VARCHAR(64) NOT NULL REFERENCES dim_business(business_id),
 customer_id VARCHAR(64) NOT NULL REFERENCES dim_customer(customer_id),
 date_key DATE NOT NULL REFERENCES dim_date(date_key), stars INTEGER NOT NULL CHECK(stars BETWEEN 1 AND 5)
);
CREATE VIEW review_weather AS
 SELECT r.review_id,b.business_id,b.name,r.date_key,r.stars,w.max_temp_f,w.min_temp_f,w.precipitation_inch
 FROM fact_review r JOIN dim_business b ON b.business_id=r.business_id
 LEFT JOIN dim_weather w ON w.station_id=b.station_id AND w.date_key=r.date_key;
CREATE VIEW monthly_review_summary AS
 SELECT business_id,substr(CAST(date_key AS VARCHAR(30)),1,7) AS month,
 COUNT(*) AS review_count,AVG(stars) AS average_stars,
 COUNT(max_temp_f) AS reviews_with_temperature,AVG(max_temp_f) AS mean_max_temperature
 FROM review_weather GROUP BY business_id,substr(CAST(date_key AS VARCHAR(30)),1,7);
