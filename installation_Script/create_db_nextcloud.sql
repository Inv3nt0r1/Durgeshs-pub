CREATE DATABASE nextclouddb;

CREATE USER 'nextclouduser'@'localhost' IDENTIFIED BY 'NextCloudPassword';

GRANT ALL PRIVILEGES ON nextclouddb.* TO 'nextclouduser'@'localhost';

FLUSH PRIVILEGES;

