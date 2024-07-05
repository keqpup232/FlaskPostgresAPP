DROP TABLE IF EXISTS books;
CREATE TABLE books (id serial PRIMARY KEY,
                    title varchar (150) NOT NULL,
                    author varchar (50) NOT NULL,
                    pages_num integer NOT NULL,
                    review text,
                    date_added date DEFAULT CURRENT_TIMESTAMP
                    );
DROP TABLE IF EXISTS users;
CREATE TABLE users (id serial PRIMARY KEY,
                    name varchar (60) NOT NULL,
                    email varchar (120) UNIQUE NOT NULL,
                    record_date timestamp DEFAULT CURRENT_TIMESTAMP
                    );