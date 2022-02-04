
-- DB schema 

DROP TABLE IF EXISTS urls;
CREATE TABLE urls (
id INTEGER PRIMARY KEY AUTOINCREMENT,
url_original TEXT NOT NULL,
url_short TEXT DEFAULT NULL,
creation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
count_original INTEGER NOT NULL DEFAULT 0
)


-- id: The URL id, this will be a unique integer value for each URL entry. It will be needed to get the OG url from a hash string.
-- creation_time: The date the URL was shortened.
-- url_original: The og long URL to which users will be redirected to.
-- count_original: The number of times a URL was resolved back to the original