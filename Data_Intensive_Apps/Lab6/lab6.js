/*
docker network create my-mongo-cluster
docker run --name mongo-node1 -d --rm --net my-mongo-cluster mongo --replSet rs0
docker run --name mongo-node2 -d --rm --net my-mongo-cluster mongo --replSet rs0
docker run --name mongo-node3 -d --rm --net my-mongo-cluster mongo --replSet rs0
docker exec -it mongo-node1 mongosh
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
db.collection.find({ }).readPref("secondary")

// write with one node disabled and write concern equal to 3 and infinite timeout
// try to enable the disabled node during the timeout
rs.stepDown()
// set write concern
db.getMongo().setWriteConcern(3)
// perform write operation
db.my_collection.insertOne({"key": "value"})
// try to enable the disabled node during the timeout
rs.freeze(0)


// set a finite timeout and wait for it to expire
// check if data is written and available for reading with readConcern level: "majority"
db.getMongo().setWriteConcern({"w": "majority", "wtimeout": 5000})
// perform write operation
db.my_collection.insertOne({"key": "value"})
// check if data is available for reading with readConcern level "majority"
db.my_collection.findOne({"$readConcern": {"level": "majority"}})

// demonstrate re-election of the primary node by disabling the current primary (Replica Set Elections)
rs.stepDown()
// wait for a new primary to be elected
rs.status()
// restore the old primary
rs.freeze(0)
// check if new data is replicated to the old primary
db.my_collection.findOne({"$readConcern": {"level": "majority"}})

// bring the cluster to an inconsistent state using the moment when the primary node does not immediately notice the absence of the secondary node
rs.stepDown("mongo-secondary-1:27017", {force: true})
rs.stepDown("mongo-secondary-2:27017", {force: true})
// write a value with write concern of 1
db.my_collection.insertOne({"key": "value"}, {w: 1})
// try to read this value with different levels of read concern
db.my_collection.findOne({"$readConcern": {"level": "majority"}})
db.my_collection.findOne({"$readConcern": {"level": "local"}})
db.my_collection.findOne({"$readConcern": {"level": "linearizable"}})
// enable the two secondary nodes
rs.freeze("mongo-secondary-1:27017", {timeoutSecs: 0})
rs.freeze("mongo-secondary-2:27017", {timeoutSecs: 0})
// wait for a new primary to be elected
rs.status()
// connect the previous primary node to the cluster and check the value written to it
db.my_collection.findOne()

// enforce eventual consistency by setting the replication delay for the replica
rs.status()
// set replication delay
rs.configure({"settings": {"catchUpTimeoutMillis": 10000}})

// leave the primary and secondary for which the replication delay is configured
// write several values
// try to read values from readConcern: {level: "linearizable"}
db.my_collection.insertMany([{"key1": "value1"},{"key2": "value2"},{"key3": "value3"}])
// try to read values with readConcern "linearizable"
db.my_collection.find({"$readConcern": {"level": "linearizable"}})
// there should be a delay until values are replicated to most nodes
