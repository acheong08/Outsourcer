DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
	username varchar(50) NOT NULL UNIQUE PRIMARY KEY,
	password varchar(50) NOT NULL
);

DROP TABLE IF EXISTS items;
CREATE TABLE items (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name int NOT NULL,
	details TEXT NOT NULL,
	contact varchar(20) NOT NULL,
	price FLOAT(6) NOT NULL,
	pic TEXT NOT NULL
	
);
