/*
docker network create my-mongo-cluster
docker run --name mongo-node1 -d --rm --net my-mongo-cluster mongo --replSet rs0
docker run --name mongo-node2 -d --rm --net my-mongo-cluster mongo --replSet rs0
docker run --name mongo-node3 -d --rm --net my-mongo-cluster mongo --replSet rs0
docker exec -it mongo-node1 mongosh
docker exec -it mongo-node2 mongosh
docker exec -it mongo-node3 mongosh
*/
config = {
      "_id" : "rs0",
      "members" : [
          {
              "_id" : 0,
              "host" : "mongo-node1:27017"
          },
          {
              "_id" : 1,
              "host" : "mongo-node2:27017"
          },
          {
              "_id" : 2,
              "host" : "mongo-node3:27017"
          }
      ]
  }
rs.initiate(config)
rs.status()


// create db
use store
db.dropDatabase()

// read preference
db.collection.find({}).readPref("secondary")

// write with one node disabled and write concern equal to 3 and infinite timeout
// try to enable the disabled node during the timeout
db.collection.insertOne({"key1": "value1"}, {writeConcern: {w: 3, wtimeout: 0}})

// set a finite timeout and wait for it to expire
// check if data is written and available for reading with readConcern level: "majority"
db.collection.insertOne({"key2": "value2"}, {writeConcern: {w: 3, wtimeout: 5000}})
db.collection.find({}, {readConcern: {level: "majority"}})

// demonstrate re-election of the primary node by disabling the current primary (Replica Set Elections)
rs.status()
db.collection.insertOne({"key3": "value3"}, {writeConcern: {w: 2, wtimeout: 5000}})
db.collection.find({}, {readConcern: {level: "local"}}).readPref("secondary")

// bring the cluster to an inconsistent state using the moment when the primary node does not immediately notice the absence of the secondary node
db.collection.insertOne({"key4": "value4"}, {w: 1})
db.collection.find({}, {readConcern: {level: "majority"}})
db.collection.find({}, {readConcern: {level: "local"}})
db.collection.find({}, {readConcern: {level: "linearizable"}})
rs.status()
db.collection.find({}, {readConcern: {level: "local"}}).readPref("secondary")

// enforce eventual consistency by setting the replication delay for the replica
cfg = rs.conf()
cfg.members[1].priority = 0
cfg.members[1].hidden = true
cfg.members[1].secondaryDelaySecs = 10
rs.reconfig(cfg)

// leave the primary and secondary for which the replication delay is configured
// write several values
// try to read values from readConcern: {level: "linearizable"}
db.collection.insertMany([{"key5": "value5"},{"key6": "value6"},{"key7": "value7"}])
db.collection.find({}, {readConcern: {level: "linearizable"}})
