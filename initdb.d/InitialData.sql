-- DROP DATABASE IF EXISTS lsl_db;
CREATE SCHEMA IF NOT EXISTS marialsl;
USE marialsl;
DROP TABLE IF EXISTS sticker_list;
CREATE TABLE sticker_list
(
    id INTEGER PRIMARY KEY,         -- Sticker's unique number : https://store.line.me/stickershop/product/3104873/ja -> 3104873
    url VARCHAR(256),               -- All url text
    title VARCHAR(256),             -- Sticker's title (Replaced '/' and ' ')
    stored_directory VARCHAR(256)   -- Downloaded Sticker's stored location (local path)
);

DROP TABLE IF EXISTS sticker_detail;
CREATE TABLE sticker_detail
(
    parent_id INTEGER,              -- sticker_list.id
    local_id INTEGER,               -- https://stickershop.line-scdn.net/stickershop/v1/sticker/32258568/iPhone/sticker@2x.png -> 32258568
    url_sticker_l VARCHAR(256),     -- Larger size sticker's url
    url_sticker_m VARCHAR(256),     -- Middle size sticker's url
    url_sticker_s VARCHAR(256),     -- Small  size sticker's url
    PRIMARY KEY (parent_id, local_id)   -- Define composite key (Double id)
);

INSERT INTO sticker_list (id, url, title, stored_directory) VALUES (1206683, "https://store.line.me/stickershop/product/1206683/", "1206683_Poputepipick", "../img/icons/1206683_Poputepipick/");
INSERT INTO sticker_list (id, url, title, stored_directory) VALUES (1252985, "https://store.line.me/stickershop/product/1252985/", "1252985_Poputepipick_2", "../img/icons/1252985_Poputepipick_2/");
INSERT INTO sticker_list (id, url, title, stored_directory) VALUES (1412535, "https://store.line.me/stickershop/product/1412535/", "1412535_Poputepipick_3", "../img/icons/1412535_Poputepipick_3/");
INSERT INTO sticker_list (id, url, title, stored_directory) VALUES (1876792, "https://store.line.me/stickershop/product/1876792/", "1876792_Poputepipick_4", "../img/icons/1876792_Poputepipick_4/");

INSERT INTO sticker_detail (parent_id, local_id, url_sticker_l, url_sticker_m, url_sticker_s) VALUES (1252985, 10260256, "https://stickershop.line-scdn.net/stickershop/v1/sticker/10260256/iPhone/sticker@2x.png", "https://stickershop.line-scdn.net/stickershop/v1/sticker/10260256/android/sticker.png", "https://stickershop.line-scdn.net/stickershop/v1/sticker/10260256/iPhone/sticker_key@2x.png");
