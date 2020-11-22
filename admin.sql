DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
	username varchar(50) NOT NULL UNIQUE PRIMARY KEY,
	password varchar(50) NOT NULL
);