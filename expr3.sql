drop database if exists SocialNetwork;
create database SocialNetwork;
use SocialNetwork;
drop table if exists user;
CREATE TABLE user (
	name varchar(10),
	gender char(1),
	birth date,
	email varchar(30),
	address varchar(50),
	passwd varchar(30),
	PRIMARY KEY ( email )
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
drop table if exists edu_experience;
create table edu_experience (
	email varchar(30),
	level varchar(10),
	school varchar(30),
	degree varchar(10),
	start_date date,
	end_date date,
	PRIMARY KEY(email, level),
	foreign key(email) references user(email)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
drop table if exists work_experience;
create table work_experience (
	email varchar(30),
	workplace varchar(10),
	title varchar(10) DEFAULT "职员",
	start_date date,
	end_date date,
	PRIMARY KEY(email, workplace, title),
	foreign key(email) references user(email)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

drop table if exists friend;
create table friend (
	usr_email varchar(30),
	fri_email varchar(30),
	group_name varchar(30) DEFAULT "默认分组",
	PRIMARY KEY(usr_email, fri_email, group_name),
	foreign key(usr_email) references user(email),
	foreign key(fri_email) references user(email)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

drop table if exists journal;
create table journal (
	email varchar(30),
	title varchar(20),
	content text,
	publish_time timestamp,
	PRIMARY KEY(email, publish_time),
	foreign key(email) references user(email)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

drop table if exists comment;
create table comment (
	replyer_email varchar(30),
	reply_content text,
	reply_time timestamp,
	to_email varchar(30),
	to_time timestamp,
	PRIMARY KEY(replyer_email, to_email, to_time),
	foreign key(replyer_email) references user(email)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

