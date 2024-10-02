show databases;

create database project;

show databases;
create database project;

use project;
create table items (
    IName varchar(50),
    ICode char(4) primary key,
    price int,
    stock int
);

desc items;

insert into items values
("toothbrush", "BR01", 25, 10),
("toothpaste", "TP01",40, 13),
("pentonic", "PN10", 90, 3),
("butterflow","BT01", 75, 0);

select * from items
