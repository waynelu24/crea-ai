DROP TABLE word_tbl;
DROP TABLE word_POS_tbl;
DROP TABLE chapter_tbl;
DROP TABLE sentence_tbl;
DROP TABLE sentence_phrase_rel_tbl;
DROP TABLE sentence_phrase_tbl;
DROP TABLE book_tbl;
DROP TABLE noun_tbl;
DROP TABLE verb_tbl;
DROP TABLE cond_tbl;



CREATE TABLE book_tbl (
book_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
book_title TEXT,
cur_timestamp TIMESTAMP);


CREATE TABLE chapter_tbl (
chapter_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
book_id INT,
chapter_title TEXT,
cur_timestamp TIMESTAMP,
INDEX (book_id));


CREATE TABLE sentence_tbl (
sentence_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
chapter_id INT,
sentence_body TEXT,
sentence_sequence INT, -- sent #
cur_timestamp TIMESTAMP,
INDEX (chapter_id));


CREATE TABLE sentence_phrase_tbl (
sentence_phrase_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
sentence_id INT,
word_POS_id INT,
sentence_phrase_text TEXT,
sentence_phrase_text_TAG VARCHAR(16),
cur_timestamp TIMESTAMP,
INDEX (word_POS_id),
INDEX (sentence_id));


CREATE TABLE sentence_phrase_rel_tbl (
sentence_phrase_rel_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
sentence_id INT,
object_phrase_id INT,
target_phrase_id INT,
phrase_rel_level_vert INT,
phrase_rel_level_horz INT,
cur_timestamp TIMESTAMP,
INDEX (sentence_id));


CREATE TABLE word_tbl (   -- entries should be unique
word_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
word_name VARCHAR(128),
cur_timestamp TIMESTAMP);


CREATE TABLE word_POS_tbl (  -- entries should be unique
word_POS_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
word_id INT,
word_name VARCHAR (128),
word_POS VARCHAR(64),
cur_timestamp TIMESTAMP,
INDEX (word_id));






CREATE TABLE noun_tbl(
noun_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
sentence_id INT,
noun_seq INT, -- seq # is relative to that sentence
word_POS_id INT,  -- link to the word_POS_tbl that contains the actual text
noun_text TEXT,
cur_timestamp TIMESTAMP);


CREATE TABLE verb_tbl(
verb_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
word_POS_id INT, -- link to the word_POS_tbl that contains the actual text
sentence_id INT,
verb_seq INT,  -- seq # is relative to that sentence
noun_seq INT, -- link to the same field in noun_tbl
-- cond_seq INT, -- link to the same field in cond_tbl; could be NULL
descriptor_seq INT, -- word_POS_id
cur_timestamp TIMESTAMP);  


CREATE TABLE cond_tbl( -- incomplete
cond_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
sentence_id INT,
verb_seq INT, -- link to the same field in verb_tbl
word_POS_id INT, -- link to the word_POS_tbl that contains the actual text
-- INCOMPLETE
cur_timestamp TIMESTAMP); 
