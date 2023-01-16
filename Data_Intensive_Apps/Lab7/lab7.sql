/*
docker network create cassandra-network
docker run --name node1 --net cassandra-network -d --rm cassandra
docker run --name node2 --net cassandra-network -d --rm cassandra
docker run --name node3 --net cassandra-network -d --rm cassandra
docker exec -it node1 cqlsh
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
nodetool status;

-- select all rows from the table 'items'
SELECT * FROM keyspace1.items WHERE category='Phone' AND manufacturer = 'Apple';

-- display the nodes on which the data is stored
nodetool getendpoints keyspace1 items "Phone";
nodetool getendpoints keyspace2 items "Phone";
nodetool getendpoints keyspace3 items "Phone";

-- disable the gossip and thrift protocol on the node
nodetool disablegossip;
nodetool disablethrift;

-- select all rows from the table 'items' in keyspace 'mykeyspace' where the category is 'Phone' and the color property is 'Gray' with a consistency level of QUORUM
SELECT * FROM mykeyspace.items WHERE category='Phone' AND properties['color'] = 'Gray' ALLOW FILTERING;

-- insert a new row into the table 'items' in keyspace 'mykeyspace' with a consistency level of TWO
INSERT INTO mykeyspace.items (id, name, price, manufacturer, category, properties) VALUES (4, 'LG V60', 900, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'White'}) USING CONSISTENCY TWO;

-- alter the keyspace 'mykeyspace'  with a replication factor of 3 and sets durable writes, default time to live, gc grace seconds and read repair chance.
ALTER KEYSPACE mykeyspace WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3} AND DURABLE_WRITES = true AND default_time_to_live = 0 AND gc_grace_seconds = 864000 AND read_repair_chance = 1.0;

-- insert values into the table 'items' in keyspace 'mykeyspace' with different properties
INSERT INTO mykeyspace.items (id, name, price, manufacturer, category, properties) VALUES (5, 'LG V60', 800, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'White'});
INSERT INTO mykeyspace.items (id, name, price, manufacturer, category, properties) VALUES (5, 'LG V60', 900, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'Black'});

-- lightweight transaction that will insert a new row into the table 'items' in keyspace 'mykeyspace' only if it does not already exist
INSERT INTO mykeyspace.items (id, name, price, manufacturer, category, properties) VALUES (6, 'LG V60', 900, 'LG', 'Phone', {'screen_size':'6.8 inches','storage':'128GB','color':'White'}) IF NOT EXISTS;

