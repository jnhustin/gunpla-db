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
  access_name     varchar (100) UNIQUE NOT NULL,
  display_name    varchar (100) UNIQUE NOT NULL,
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
  access_name         varchar(15) NOT NULL,
  display_name        varchar(15) NOT NULL,
  short_name  varchar(3) NOT NULL,
  created_date        date NOT NULL,
  updated_date        date NOT NULL,
  user_update_id      int REFERENCES users (user_id)
);

CREATE TABLE brands (
  brand_id        serial PRIMARY KEY,
  access_name     varchar(40) UNIQUE NOT NULL,
  display_name    varchar(40) UNIQUE NOT NULL,
  created_date    date NOT NULL,
  updated_date    date NOT NULL,
  user_update_id  int REFERENCES users (user_id)
);

CREATE TABLE series (
  series_id         serial PRIMARY KEY,
  access_name       varchar(40) UNIQUE NOT NULL,
  display_name      varchar(40) UNIQUE NOT NULL,
  created_date      date NOT NULL,
  updated_date      date NOT NULL,
  user_update_id    int REFERENCES users (user_id)
);


CREATE TABLE models (
  model_id          serial PRIMARY KEY,
  model_name        varchar (100) UNIQUE NOT NULL,
  japanese_name     varchar (100) UNIQUE NOT NULL,
  SKU               varchar (100) UNIQUE NOT NULL,
  info              varchar (3000),
  info_source       varchar (200),
  release_date      date,
  timeline_id       int REFERENCES timelines (timeline_id),
  series_id         int REFERENCES series (series_id),
  product_line_id   int REFERENCES product_lines (product_line_id),
  brand_id          int REFERENCES brands (brand_id),
  scale_id          int REFERENCES scales (scale_id),
  updated_date      date,
  created_date      date,
  user_update_id    int REFERENCES users (user_id)
);


INSERT INTO users (user_name, created_date, updated_date)
VALUES
  ('initial_user', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
;

INSERT INTO timelines (access_name, display_name, created_date, updated_date, user_update_id)
VALUES
  ('after_colony', 'after colony', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('universal_century', 'universal century', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('cosmic_era', 'cosmic era', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;


INSERT INTO scales (scale_value, created_date, updated_date, user_update_id)
VALUES
  ('1/144', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('1/100', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('1/60', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;

INSERT INTO product_lines (access_name, display_name, short_name, created_date, updated_date, user_update_id)
VALUES
  ('high_grade', 'high grade', 'hg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('real_grade', 'real grade', 'rg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('master_grade', 'master grade', 'mg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('perfect_grade', 'perfect grade', 'mg', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;

INSERT INTO brands (access_name, display_name, created_date, updated_date, user_update_id)
VALUES
  ('bandai', 'bandai', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('kotobukiya', 'kotobukiya', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;

INSERT INTO series (access_name, display_name, created_date, updated_date, user_update_id)
VALUES
  ('gundam_wing', 'gundam wing', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('00_gundam', '00 gundam', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('zeta gundam', 'zeta gundam', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;

INSERT INTO models (
  model_name,
  japanese_name,
  SKU,
  info,
  info_source,
  release_date,
  timeline_id,
  series_id,
  product_line_id,
  brand_id,
  scale_id,
  updated_date,
  created_date,
  user_update_id
)
VALUES
  (
    'Gundam Sandrock Ver EW',
    'ガンダムサンドロック',
    '4543112715364', -- SKU
    'Copyright Sotsu Agency / Sunrize\n- From the manga series Mobile Suit Gundam Wing: Endless Waltz: The Glory of Losers comes the Desert Combat ace Suit- the Sandrock!\n- Uses the XXXG frame utilized by the Gundam Wing!\n- Design based on new designs from mechanical designer Hajime Katoki, with redesigned decals also created by Katoki.\n- Recreate the Cross Crusher with combining gimmick, using the Shield with the Heat Shotel.\n- Cockpit hatch opens to reveal detailed cockpit.\n- Rear verniers included in high detail, and Beam Machine Gun can be mounted at the rear skirt.\n- Heat Shotel combine into a huge double-bladed weapon.\n- Beam Machine Gun features folding stock and grip.',
    'https://www.1999.co.jp/eng/10156350',
    '2011-10-01', -- release_date
    1, -- after_colony
    1, -- gundam_wing
    3, -- master_grade
    1, -- bandai
    2, -- 1/100
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    1
  )
;
