DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

DROP TABLE IF EXISTS env;
DROP TABLE IF EXISTS kms;
DROP TABLE IF EXISTS itms;
-- DROP TABLE IF EXISTS ccis;
-- DROP TABLE IF EXISTS pg;
-- DROP TABLE IF EXISTS iks;
DROP TABLE IF EXISTS agent;
-- DROP TABLE IF EXISTS pes;
-- DROP TABLE IF EXISTS reserved;

CREATE TABLE env (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,

  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  env_name TEXT UNIQUE NOT NULL,
  kms_id INTEGER UNIQUE,
  agent_id INTEGER,
  itms_id INTEGER UNIQUE,
--   iks_id INTEGER,
--   ccis_id INTEGER,
--   pg_id INTEGER,
--   pes_id INTEGER,

  priority_level INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (kms_id) REFERENCES kms (id),
  FOREIGN KEY (agent_id) REFERENCES agent (id),
  FOREIGN KEY (itms_id) REFERENCES itms (id)
--   FOREIGN KEY (iks_id) REFERENCES iks (id),
--   FOREIGN KEY (ccis_id) REFERENCES ccis (id),
--   FOREIGN KEY (pg_id) REFERENCES pg (id),
--   FOREIGN KEY (pes_id) REFERENCES pes (id)
);

CREATE TABLE kms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  env_id INTEGER,
  
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  kms_user TEXT NOT NULL,
  kms_password TEXT NOT NULL,
  kms_ip TEXT UNIQUE NOT NULL,
  domain_name TEXT NOT NULL,
  test_root_folder TEXT NOT NULL,
  branch TEXT NOT NULL,
  db_name TEXT NOT NULL,
  db_user TEXT NOT NULL,
  db_password TEXT NOT NULL,
  db_host TEXT NOT NULL,
  db_ip TEXT UNIQUE NOT NULL,
  sa_name TEXT NOT NULL,
  sa_password TEXT NOT NULL,
  private_device INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (env_id) REFERENCES env (id)
);

CREATE TABLE agent (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  env_id INTEGER,

  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  agent_ip TEXT UNIQUE NOT NULL,
  agent_port TEXT NOT NULL,
  private_device INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (env_id) REFERENCES env (id)
);

CREATE TABLE itms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  env_id INTEGER,

  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  env_name TEXT NOT NULL,
  itms_ip TEXT UNIQUE NOT NULL,
  itms_output_ip TEXT,
  itms_output_port TEXT,
  ecm_port1 TEXT, 
  ecm_port2 TEXT,
  emm_port1 TEXT, 
  emm_port2 TEXT,
  private_device INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (env_id) REFERENCES env (id)
);

-- CREATE TABLE iks (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   user_id INTEGER NOT NULL,
--   env_id INTEGER,

--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   cca_iks INTEGER NOT NULL,
--   connection_num INTEGER NOT NULL,
--   iks_ip TEXT UNIQUE NOT NULL,
--   private_device INTEGER NOT NULL,

--   FOREIGN KEY (user_id) REFERENCES user (id),
--   FOREIGN KEY (env_id) REFERENCES env (id)
-- );

-- CREATE TABLE pes (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   user_id INTEGER NOT NULL,
--   env_id INTEGER,

--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   pes_ip TEXT UNIQUE NOT NULL,
--   pes_port TEXT NOT NULL,
--   out_put_address TEXT,
--   private_device INTEGER NOT NULL,

--   FOREIGN KEY (user_id) REFERENCES user (id),
--   FOREIGN KEY (env_id) REFERENCES env (id)
-- );

-- CREATE TABLE ccis (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   user_id INTEGER NOT NULL,
--   env_id INTEGER,

--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   ccis_ip TEXT UNIQUE NOT NULL,
--   ccis_port TEXT NOT NULL,
--   private_device INTEGER NOT NULL,

--   FOREIGN KEY (user_id) REFERENCES user (id),
--   FOREIGN KEY (env_id) REFERENCES env (id)
-- );

-- CREATE TABLE pg (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   user_id INTEGER NOT NULL,
--   env_id INTEGER,

--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   pg_ip TEXT UNIQUE NOT NULL,
--   pg_port TEXT NOT NULL,
--   private_device INTEGER NOT NULL,

--   FOREIGN KEY (user_id) REFERENCES user (id),
--   FOREIGN KEY (env_id) REFERENCES env (id)
-- );