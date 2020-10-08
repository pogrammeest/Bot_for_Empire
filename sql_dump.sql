PRAGMA FOREIGN_KEYS=ON;

drop table IF EXISTS person;--это можно потом убрать, нужно, чтоб не прописывать руками
drop table IF EXISTS weapons;--при каждом чтении дампа
drop table IF EXISTS armor;
drop table IF EXISTS locations;
drop table IF EXISTS mobs;


CREATE TABLE person(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    HP REAL NOT NULL,
    LVL INTEGER NOT NULL ,
    curent_loc INTEGER NOT NULL ,
    inventory_weapons TEXT ,--У нас разные таблицы с оружием
    inventory_armor TEXT ,--и бронёй, поэтому инвентаря два.
    in_hand INTEGER NOT NULL ,--текущее оружие в руках
    on_body INTEGER NOT NULL ,--текущая броня
    XP REAL NOT NULL,
    on_rest DATETIME NOT NULL,
    FOREIGN KEY (curent_loc) REFERENCES locations(id),
    FOREIGN KEY (in_hand) REFERENCES weapons(id),
    FOREIGN KEY (on_body) REFERENCES armor(id)
);

CREATE TABLE weapons(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    LVL INTEGER NOT NULL,
    damage INTEGER NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE armor(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    LVL INTEGER NOT NULL,
    DT REAL NOT NULL,--Порог урона
    protection REAL NOT NULL,--поглощение урона в процентах
    price INTEGER NOT NULL
);

CREATE TABLE locations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    max_lvl INTEGER NOT NULL
);

CREATE TABLE mobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT
);

insert into mobs(description) values("1");--мобы для первых 10-ти локаций ещё не готовы
insert into mobs(description) values("2");
insert into mobs(description) values("3");
insert into mobs(description) values("4");
insert into mobs(description) values("5");
insert into mobs(description) values("6");
insert into mobs(description) values("7");
insert into mobs(description) values("8");
insert into mobs(description) values("9");
insert into mobs(description) values("10");

