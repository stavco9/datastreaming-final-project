#!/bin/bash

USERNAME=root
PASSWORD=Aa123456

## Part1 -> wikidb population

mysql -u $USERNAME -p$PASSWORD -e "CREATE DATABASE wiki_db;"
mysql -u $USERNAME -p$PASSWORD wiki_db -e "ALTER DATABASE wiki_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"

curl https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-redirect.sql.gz -O
curl https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page.sql.gz -O
curl https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-geo_tags.sql.gz -O

gzip -d enwiki-latest-geo_tags.sql.gz 
gzip -d enwiki-latest-page.sql.gz 
gzip -d enwiki-latest-redirect.sql.gz 

mysql -u $USERNAME -p$PASSWORD wiki_db < enwiki-latest-page.sql 
mysql -u $USERNAME -p$PASSWORD wiki_db < enwiki-latest-redirect.sql 
mysql -u $USERNAME -p$PASSWORD wiki_db < enwiki-latest-geo_tags.sql 

mysql -u $USERNAME -p$PASSWORD wiki_db -e "CREATE VIEW locs AS \
    SELECT DISTINCT page1.page_id, page1.page_title, page1.page_len, geo.gt_id, geo.gt_lat, geo.gt_lon, geo.gt_dim, geo.gt_type, geo.gt_country, geo.gt_name, geo.gt_region FROM page AS page1 \
    JOIN geo_tags AS geo on geo.gt_page_id=page1.page_id \
    WHERE page1.page_namespace=0 \
    AND page1.page_content_model="wikitext" \
    AND geo.gt_globe="earth";"

rm enwiki-latest-geo_tags.sql 
rm enwiki-latest-redirect.sql 
rm enwiki-latest-page.sql

## Part1 -> wiki Gazetteer population

mysql -u $USERNAME -p$PASSWORD -e "CREATE DATABASE wikiGazetteer;"
mysql -u $USERNAME -p$PASSWORD wikiGazetteer -e "ALTER DATABASE wikiGazetteer CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
mysql -u $USERNAME -p$PASSWORD wikiGazetteer -e "CREATE TABLE `altname` \
    ( \
    `id` int PRIMARY KEY, \
    `main_id` int, \
    `altname` varchar(255), \
    `source` varchar(255) \
    );"
mysql -u $USERNAME -p$PASSWORD wikiGazetter -e "CREATE TABLE `location` \
    ( \
    `id` int PRIMARY KEY, \
    `wiki_id` int, \
    `wikigt_id` int, \
    `geo_id` int, \
    `wiki_title` varchar(255), \
    `page_len` int, \
    `lat` float, \
    `lon` float, \
    `dim` int, \
    `type` varchar(255), \
    `country` varchar(255), \
    `region` varchar(255), \
    `population` int \
    );"
mysql -u $USERNAME -p$PASSWORD wikiGazetter -e "ALTER TABLE `altname` ADD FOREIGN KEY (`main_id`) REFERENCES `location` (`id`);"

curl http://download.geonames.org/export/dump/cities500.zip -O
curl http://download.geonames.org/export/dump/alternateNamesV2.zip -O
unzip cities500.zip
unzip alternateNamesV2.zip
rm cities500.zip
rm alternateNamesV2.zip

python3 addLocations.py
pytohn3 addRedirections.py

mysql -u $USERNAME -p$PASSWORD wikiGazetter -e "ALTER TABLE location ADD INDEX(id);"
mysql -u $USERNAME -p$PASSWORD wikiGazetter -e "ALTER TABLE altname ADD INDEX(altname);"