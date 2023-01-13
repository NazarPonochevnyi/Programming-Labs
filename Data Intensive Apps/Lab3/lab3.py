import pymongo


# Docker: docker run -it --rm -p 27017:27017 --name test-mongo mongo
client = pymongo.MongoClient("mongodb://localhost:27017/")

# create db
client.drop_database("store")
db = client["store"]

# create items
phones = [
    {"category": "Phone", "model": "iPhone 6", "manufacturer": "Apple", "price": 600},
    {"category": "Phone", "model": "Samsung Galaxy S21", "manufacturer": "Samsung", "price": 800},
    {"category": "Phone", "model": "Google Pixel 5", "manufacturer": "Google", "price": 700}
]
tvs = [
    {"category": "TV", "model": "Samsung QLED", "manufacturer": "Samsung", "price": 1500},
    {"category": "TV", "model": "LG OLED", "manufacturer": "LG", "price": 1700},
    {"category": "TV", "model": "Sony Bravia", "manufacturer": "Sony", "price": 1600}
]
smart_watches = [
    {"category": "Smart Watch", "model": "Apple Watch Series 6", "manufacturer": "Apple", "price": 400},
    {"category": "Smart Watch", "model": "Samsung Galaxy Watch", "manufacturer": "Samsung", "price": 350},
    {"category": "Smart Watch", "model": "Fitbit Versa 3", "manufacturer": "Fitbit", "price": 300}
]
db.items.insert_many(sum([phones, tvs, smart_watches], []))

# list all items
for item in db.items.find():
    print(item)

# count how many products in Phone category
count = db.items.count_documents({"category": "Phone"})
print(f"\nThere are {count} products in the 'Phone' category.")

# count how many different categories of goods there are
categories = db.items.distinct("category")
print(f"\nThere are {len(categories)} different categories of goods.")

# list of all manufacturers of goods without duplicates
manufacturers = db.items.distinct("manufacturer")
print(f"\nManufacturers: {manufacturers}")

# write queries that select products by different criteria and their combination: 
# category and price (in between)
category = "Phone"
price_range = (500, 700)
query = {"$and": [{"category": category}, {"price": {"$gte": price_range[0], "$lte": price_range[1]}}]}
print()
for item in db.items.find(query):
    print(item)

# model or one or the other
models = ["iPhone 6", "Samsung QLED"]
query = {"$or": [{"model": models[0]}, {"model": models[1]}]}
print()
for item in db.items.find(query):
    print(item)

# manufacturers from the list
manufacturers = ["Apple", "Samsung"]
query = {"manufacturer": {"$in": manufacturers}}
print()
for item in db.items.find(query):
    print(item)

# update price for all products in the "Phone" category
db.items.update_many({"category": "Phone"}, {"$set": {"price": 650}})

# add a new property "color" to all products in the "TV" category
db.items.update_many({"category": "TV"}, {"$set": {"color": "black"}})

# find all products with the "color" property
print()
for item in db.items.find({"color": {"$exists": True}}):
    print(item)

# increase the price of all products with the "color" property by $50
db.items.update_many({"color": {"$exists": True}}, {"$inc": {"price": 50}})


# close the connection
client.close()
