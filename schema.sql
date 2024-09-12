-- create table users(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     full_name TEXT,
--     email TEXT,
--     password TEXT
-- )
-- create table products(
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     product_name TEXT,
--     product_type TEXT,
--     price TEXT,
--     file_name TEXT
-- )
create table usercart(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
     user_id TEXT,
     item_id TEXT,
     quantity TEXT
)




