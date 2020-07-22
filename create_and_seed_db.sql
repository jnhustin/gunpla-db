-- create the database
DROP DATABASE IF EXISTS gunpla_db;
CREATE DATABASE gunpla_db;

-- connect to the database
\c gunpla_db;


-- create tables
CREATE TABLE users (
  user_id       serial PRIMARY KEY,
  user_name     varchar (50) UNIQUE NOT NULL,
  created_date  date NOT NULL,
  updated_date  date NOT NULL
);


CREATE TABLE timelines (
  timeline_id     serial PRIMARY KEY,
  timeline_name   varchar (100) UNIQUE NOT NULL,
  created_date    date NOT NULL,
  updated_date    date NOT NULL,
  user_update_id  int REFERENCES users (user_id)
);

CREATE TABLE scales (
  scale_id        serial PRIMARY KEY,
  scale_value     varchar(10) UNIQUE NOT NULL,
  created_date    date NOT NULL,
  updated_date    date NOT NULL,
  user_update_id  int REFERENCES users (user_id)
);

CREATE TABLE product_lines (
  product_line_id     serial PRIMARY KEY,
  product_line_long   varchar(15) NOT NULL,
  product_line_short  varchar(3) NOT NULL,
  created_date        date NOT NULL,
  updated_date        date NOT NULL,
  user_update_id      int REFERENCES users (user_id)
);

CREATE TABLE brands (
  brand_id        serial PRIMARY KEY,
  brand_name      varchar(40) UNIQUE NOT NULL,
  created_date    date NOT NULL,
  updated_date    date NOT NULL,
  user_update_id  int REFERENCES users (user_id)
);

CREATE TABLE franchises (
  franchise_id      serial PRIMARY KEY,
  franchise_name    varchar(40) UNIQUE NOT NULL,
  created_date      date NOT NULL,
  updated_date      date NOT NULL,
  user_update_id    int REFERENCES users (user_id)
);


CREATE TABLE models (
  model_id          serial PRIMARY KEY,
  timeline_id       int REFERENCES timelines (timeline_id),
  franchise_id      int REFERENCES franchises (franchise_id),
  product_line_id   int REFERENCES product_lines (product_line_id),
  brand_id          int REFERENCES brands (brand_id),
  scale_id          int REFERENCES scales (scale_id),

  model_name        varchar (100) UNIQUE NOT NULL,
  japanese_name     varchar (100) UNIQUE NOT NULL,
  SKU               varchar (100) UNIQUE NOT NULL,
  info              varchar (500),
  info_source       varchar (200),
  release_date      date,
  created_date      date,
  updated_date      date
);


INSERT INTO users (user_name, created_date, updated_date)
VALUES
  ('initial_user', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
;

INSERT INTO timelines (timeline_name, created_date, updated_date, user_update_id)
VALUES
  ('after colony', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('universal century', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('cosmic era', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;


INSERT INTO scales (scale_value, created_date, updated_date, user_update_id)
VALUES
  ('1/144', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('1/100', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('1/60', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;

INSERT INTO product_lines (product_line_long, product_line_short, created_date, updated_date, user_update_id)
VALUES
  ('high', 'hg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('real', 'rg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('master', 'mg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('perfect', 'mg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;

INSERT INTO brands (brand_name, created_date, updated_date, user_update_id)
VALUES
  ('bandai', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('kotobukiya', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;

INSERT INTO franchises (franchise_name, created_date, updated_date, user_update_id)
VALUES
  ('gundam wing', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('00 gundam', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('zeta gundam', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;
