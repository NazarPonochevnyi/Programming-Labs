/*
docker network create cassandra-network
docker run --name node1 -e CASSANDRA_CLUSTER_NAME=MyCluster -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e CASSANDRA_DC=datacenter1 --net cassandra-network -d --rm cassandra
docker run --name node2 -e CASSANDRA_SEEDS=node1 -e CASSANDRA_CLUSTER_NAME=MyCluster -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e CASSANDRA_DC=datacenter1 --net cassandra-network -d --rm cassandra
docker run --name node3 -e CASSANDRA_SEEDS=node1 -e CASSANDRA_CLUSTER_NAME=MyCluster -e CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch -e CASSANDRA_DC=datacenter2 --net cassandra-network -d --rm cassandra
docker exec -it node1 bash (cqlsh, nodetool status)
*/


-- create keyspace
CREATE KEYSPACE keyspace1 WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};
CREATE KEYSPACE keyspace2 WITH replication = {'class':'SimpleStrategy', 'replication_factor':2};
CREATE KEYSPACE keyspace3 WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};

-- create db
CREATE TABLE keyspace1.items (
    id int,
    name text,
    price float,
    manufacturer text,
    category text,
    properties map<text, text>,
    PRIMARY KEY ((category), manufacturer, id)
);
CREATE TABLE keyspace2.items (
    id int,
    name text,
    price float,
    manufacturer text,
    category text,
    properties map<text, text>,
    PRIMARY KEY ((category), manufacturer, id)
);
CREATE TABLE keyspace3.items (
    id int,
    name text,
    price float,
    manufacturer text,
    category text,
    properties map<text, text>,
    PRIMARY KEY ((category), manufacturer, id)
);

-- insert data
BEGIN BATCH
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (0,'iPhone 6', 600, 'Apple', 'Phone', {'screen_size':'4.7 inches','storage':'64GB','color':'Silver'});
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (1,'Samsung Galaxy S21', 800, 'Samsung', 'Phone', {'screen_size':'6.2 inches','storage':'128GB','color':'Gray'});
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (2,'Google Pixel 5', 700, 'Google', 'Phone', {'screen_size':'6 inches','storage':'64GB','color':'Black'});
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (3,'Samsung QLED', 1500, 'Samsung', 'TV', {'screen_size':'65 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (4,'LG OLED', 1700, 'LG', 'TV', {'screen_size':'55 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (5,'Sony Bravia', 1600, 'Sony', 'TV', {'screen_size':'50 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (6,'Apple Watch Series 6', 400, 'Apple', 'Smart Watch', {'display':'Retina','storage':'32GB','water_resistant':'Yes','heart_rate_monitor':'Yes'});
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (7,'Samsung Galaxy Watch', 350, 'Samsung', 'Smart Watch', {'display':'AMOLED','storage':'16GB','water_resistant':'Yes','heart_rate_monitor':'Yes'});
INSERT INTO keyspace1.items (id, name, price, manufacturer, category, properties) VALUES (8,'Fitbit Versa 3', 300, 'Fitbit', 'Smart Watch', {'display':'LCD','storage':'4GB','water_resistant':'Yes'});
APPLY BATCH;
BEGIN BATCH
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (0,'iPhone 6', 600, 'Apple', 'Phone', {'screen_size':'4.7 inches','storage':'64GB','color':'Silver'});
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (1,'Samsung Galaxy S21', 800, 'Samsung', 'Phone', {'screen_size':'6.2 inches','storage':'128GB','color':'Gray'});
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (2,'Google Pixel 5', 700, 'Google', 'Phone', {'screen_size':'6 inches','storage':'64GB','color':'Black'});
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (3,'Samsung QLED', 1500, 'Samsung', 'TV', {'screen_size':'65 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (4,'LG OLED', 1700, 'LG', 'TV', {'screen_size':'55 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (5,'Sony Bravia', 1600, 'Sony', 'TV', {'screen_size':'50 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (6,'Apple Watch Series 6', 400, 'Apple', 'Smart Watch', {'display':'Retina','storage':'32GB','water_resistant':'Yes','heart_rate_monitor':'Yes'});
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (7,'Samsung Galaxy Watch', 350, 'Samsung', 'Smart Watch', {'display':'AMOLED','storage':'16GB','water_resistant':'Yes','heart_rate_monitor':'Yes'});
INSERT INTO keyspace2.items (id, name, price, manufacturer, category, properties) VALUES (8,'Fitbit Versa 3', 300, 'Fitbit', 'Smart Watch', {'display':'LCD','storage':'4GB','water_resistant':'Yes'});
APPLY BATCH;
BEGIN BATCH
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (0,'iPhone 6', 600, 'Apple', 'Phone', {'screen_size':'4.7 inches','storage':'64GB','color':'Silver'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (1,'Samsung Galaxy S21', 800, 'Samsung', 'Phone', {'screen_size':'6.2 inches','storage':'128GB','color':'Gray'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (2,'Google Pixel 5', 700, 'Google', 'Phone', {'screen_size':'6 inches','storage':'64GB','color':'Black'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (3,'Samsung QLED', 1500, 'Samsung', 'TV', {'screen_size':'65 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (4,'LG OLED', 1700, 'LG', 'TV', {'screen_size':'55 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (5,'Sony Bravia', 1600, 'Sony', 'TV', {'screen_size':'50 inches','resolution':'4K','smart_tv':'Yes'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (6,'Apple Watch Series 6', 400, 'Apple', 'Smart Watch', {'display':'Retina','storage':'32GB','water_resistant':'Yes','heart_rate_monitor':'Yes'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (7,'Samsung Galaxy Watch', 350, 'Samsung', 'Smart Watch', {'display':'AMOLED','storage':'16GB','water_resistant':'Yes','heart_rate_monitor':'Yes'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (8,'Fitbit Versa 3', 300, 'Fitbit', 'Smart Watch', {'display':'LCD','storage':'4GB','water_resistant':'Yes'});
APPLY BATCH;

-- select all rows from the table 'items'
SELECT * FROM keyspace1.items WHERE category = 'Phone' AND manufacturer = 'Apple';

/*
- display the nodes on which the data is stored
nodetool getendpoints keyspace1 items "Phone"
nodetool getendpoints keyspace2 items "Phone"
nodetool getendpoints keyspace3 items "Phone"
*/

CONSISTENCY;
CONSISTENCY ONE;
SELECT * FROM keyspace1.items;
UPDATE keyspace1.items SET price = 900 WHERE category = 'Phone' AND manufacturer = 'Apple' AND id = 0 IF EXISTS;
CONSISTENCY TWO;
SELECT * FROM keyspace2.items;
UPDATE keyspace2.items SET price = 900 WHERE category = 'Phone' AND manufacturer = 'Apple' AND id = 0 IF EXISTS;
CONSISTENCY THREE;
SELECT * FROM keyspace3.items;
UPDATE keyspace3.items SET price = 900 WHERE category = 'Phone' AND manufacturer = 'Apple' AND id = 0 IF EXISTS;

/*
docker network disconnect cassandra-network node1
docker network disconnect cassandra-network node2
docker network disconnect cassandra-network node3
*/

-- alter the keyspace3 with a replication factor of 3
CONSISTENCY ONE;

INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (5, 'LG V60', 800, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'White'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (5, 'LG V60', 900, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'Black'});
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (5, 'LG V60', 950, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'Gray'});

-- lightweight transaction 
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (6, 'LG V70', 950, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'White'}) IF NOT EXISTS;
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (6, 'LG V70', 990, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'Black'}) IF NOT EXISTS;
INSERT INTO keyspace3.items (id, name, price, manufacturer, category, properties) VALUES (6, 'LG V70', 999, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'Gray'}) IF NOT EXISTS;

/*
docker network connect cassandra-network node1
docker network connect cassandra-network node2
docker network connect cassandra-network node3
*/

-- check how cassandra resolved the conflict
SELECT * FROM keyspace3.items WHERE category = 'Phone' AND manufacturer = 'LG' AND id >= 5 AND id <= 6;
