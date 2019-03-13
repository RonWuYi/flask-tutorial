DROP TABLE IF EXISTS files;


CREATE TABLE files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  file_name TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  checked INTEGER NOT NULL,
  strong TEXT
--  FOREIGN KEY (author_id) REFERENCES user (id)
);