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

CREATE TABLE manufacturers (
  manufacturer_id        serial PRIMARY KEY,
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
  access_name       varchar (100) NOT NULL,
  display_name      varchar (100) NOT NULL,
  japanese_name     varchar (100) UNIQUE,
  sku               varchar (100) UNIQUE,
  info              varchar (3000),
  info_source       varchar (200),
  release_date      date,
  timeline_id       int REFERENCES timelines (timeline_id),
  series_id         int REFERENCES series (series_id),
  product_line_id   int REFERENCES product_lines (product_line_id),
  manufacturer_id   int REFERENCES manufacturers (manufacturer_id),
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
  ('cosmic_era', 'cosmic era', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('post_disaster', 'post disaster', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('advanced_generation', 'advanced generation', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('build', 'build', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('anno_domini', 'anno domini', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)

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

INSERT INTO manufacturers (access_name, display_name, created_date, updated_date, user_update_id)
VALUES
  ('bandai', 'bandai', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('kotobukiya', 'kotobukiya', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;

INSERT INTO series (access_name, display_name, created_date, updated_date, user_update_id)
VALUES
  ('00', '00', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('08th_ms_team', '08th ms team', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('age', 'age', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('build_fighters', 'build fighters', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('build_divers', 'build divers', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('endless_waltz', 'endless waltz', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('iron_blooded_orphans', 'iron blooded orphans', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('narrative', 'narrative', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('reconguista_in_g', 'reconguista in g', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('seed', 'seed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('seed_destiny', 'seed destiny', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('the origin', 'the origin', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('thunderbolt', 'thunderbolt', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('wing', 'wing', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('zeta', 'zeta', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1),
  ('zz', 'zz', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 1)
;
