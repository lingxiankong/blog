DROP DATABASE IF EXISTS blog;
CREATE DATABASE blog;
USE blog;
DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
    id varchar(36) PRIMARY KEY NOT NULL,
    title varchar(255) NOT NULL,
    content varchar(255) NOT NULL,
    created datetime DEFAULT NULL
);