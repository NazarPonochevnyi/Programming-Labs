import pymongo
from datetime import datetime, timedelta


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
print("\nAll items:")
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
print("\nPhone products between 500 and 700:")
for item in db.items.find(query):
    print(item)

# model or one or the other
models = ["iPhone 6", "Samsung QLED"]
query = {"$or": [{"model": models[0]}, {"model": models[1]}]}
print("\nProducts model iPhone 6, Samsung QLED:")
for item in db.items.find(query):
    print(item)

# manufacturers from the list
manufacturers = ["Apple", "Samsung"]
query = {"manufacturer": {"$in": manufacturers}}
print("\nProducts by Apple and Sumsung:")
for item in db.items.find(query):
    print(item)

# update price for all products in the "Phone" category
db.items.update_many({"category": "Phone"}, {"$set": {"price": 650}})

# add a new property "color" to all products in the "TV" category
db.items.update_many({"category": "TV"}, {"$set": {"color": "black"}})

# find all products with the "color" property
print("\nAll products with the 'color' property")
for item in db.items.find({"color": {"$exists": True}}):
    print(item)

# increase the price of all products with the "color" property by $50
db.items.update_many({"color": {"$exists": True}}, {"$inc": {"price": 50}})

# create some orders with different products
item1, item2 = db.items.find({"manufacturer": "Apple"}, {"_id": 1})
item3 = db.items.find_one({"model": "Fitbit Versa 3"}, {"_id": 1})
item4, item5, item6 = db.items.find({"category": "TV"}, {"_id": 1})
order1 = {
    "order_number" : 201513,
    "date" : datetime.now(),
    "total_sum" : 1923.4,
    "customer" : {
        "name" : "Andrii",
        "surname" : "Rodionov",
        "phone_numbers" : [9876543, 1234567],
        "address" : "PTI, Peremohy 37, Kyiv, UA"
    },
    "payment" : {
        "card_owner" : "Andrii Rodionov",
        "card_id" : 12345678
    },
    "order_items" : [
        {"$ref": "items", "$id": item1["_id"]},
        {"$ref": "items", "$id": item2["_id"]},
    ]
}
order2 = {
    "order_number" : 201514,
    "date" : datetime.now() - timedelta(days=1),
    "total_sum" : 900,
    "customer" : {
        "name" : "John",
        "surname" : "Doe",
        "phone_numbers" : [1111111],
        "address" : "New York, USA"
    },
    "payment" : {
        "card_owner" : "John Doe",
        "card_id" : 11111111
    },
    "order_items" : [
        {"$ref": "items", "$id": item3["_id"]},
        {"$ref": "items", "$id": item2["_id"]},
    ]
}
order3 = {
    "order_number" : 201515,
    "date" : datetime.now() - timedelta(days=2),
    "total_sum" : 1200,
    "customer" : {
        "name" : "Jane",
        "surname" : "Doe",
        "phone_numbers" : [2222222],
        "address" : "Chicago, USA"
    },
    "payment" : {
        "card_owner" : "Jane Doe",
        "card_id" : 22222222
    },
    "order_items" : [
        {"$ref": "items", "$id": item4["_id"]},
        {"$ref": "items", "$id": item5["_id"]},
    ]
}
db.orders.insert_many([order1, order2, order3])

# print all orders
print("\nAll orders:")
for order in db.orders.find():
    print(order)

# print orders with cost more than a certain value
print("\nOrders with cost more than 1500:")
for order in db.orders.find({"total_sum": {"$gt": 1500}}):
    print(order)

# find orders made by one customer
print("\nOrders made by A. Rodionov:")
for order in db.orders.find({"customer.name": "Andrii", "customer.surname": "Rodionov"}):
    print(order)

# find all orders with a certain product(s) (by ObjectId)
print("\nAll orders with a certain product:")
for order in db.orders.find({"order_items": {"$elemMatch": {"$id": item2["_id"]}}}):
    print(order)

# add one more product to all orders with a certain product and increase the existing order value by some value X
x = 50
db.orders.update_many({"order_items": {"$elemMatch": {"$id": item5["_id"]}}}, {"$push": {"order_items": {"$ref": "items", "$id": item6["_id"]}}, "$inc": {"total_sum": x}})

# print the number of products in some order
order = db.orders.find_one({"order_number": 201515})
print(f"\nNumber of products in order: {len(order['order_items'])}")

# print only information about the customizer and credit card numbers for orders whose cost exceeds a certain amount
amount = 1100
print("\nCustomizer and credit card numbers for orders whose cost exceeds 1100:")
for order in db.orders.find({"total_sum": {"$gt": amount}}, {"_id": 0, "customer.name": 1, "customer.surname": 1, "payment.card_id": 1}):
    print(order)

# remove the product from orders made for a certain period of dates
start_date = datetime.now() - timedelta(days=3)
end_date = datetime.now() - timedelta(days=1)
db.orders.update_many({"date": {"$gte": start_date, "$lte": end_date}, "order_items": {"$elemMatch": {"$id": item6["_id"]}}}, {"$pull": {"order_items": {"$id": item6["_id"]}}})

# rename the name (surname) of the customer in all orders
new_name = "Alex"
new_surname = "Smith"
db.orders.update_many({"customer.name": "Andrii", "customer.surname": "Rodionov"}, {"$set": {"customer.name": new_name, "customer.surname": new_surname}})

# find the orders made by one customer, and print only information about the customer and the products in the order substituting the names of the products and their cost instead of ObjectId("***")
customer_name = "Alex"
customer_surname = "Smith"
pipeline = [
    {"$match": {"customer.name": customer_name, "customer.surname": customer_surname}},
    {"$lookup": {
        "from": "items",
        "localField": "order_items.$id",
        "foreignField": "_id",
        "as": "order_items"
    }},
    {"$project": {
        "customer": 1,
        "total_sum": { "$sum": { "$map": {
                        "input": "$order_items",
                        "as": "item",
                        "in": "$$item.price"
                    } } },
        "order_items": {
            "$map": {
                "input": "$order_items",
                "as": "item",
                "in": {
                    "name": "$$item.model",
                    "price": "$$item.price"
                }
            }
        }
    }}
]
print("\nCustomer stats:")
for order in db.orders.aggregate(pipeline):
    print(f"Customer: {order['customer']['name']} {order['customer']['surname']}")
    print(f"Total cost: {order['total_sum']}")
    print("Order items:")
    for item in order['order_items']:
        print(f"  {item['name']} - {item['price']}")

# create a capped collection with a max size of 100MB and max of 5 documents
db.create_collection("reviews", capped=True, size=100000, max=5)

# insert reviews into the collection
item = db.items.find_one({"model": "Fitbit Versa 3"}, {"_id": 1})
review1 = {
    "name": "Jane Doe",
    "item_id": item["_id"],
    "rating": 5,
    "review_text": "Great product, highly recommend!",
    "date": datetime.now()
}
review2 = {
    "name": "Alex Smith",
    "item_id": item["_id"],
    "rating": 4,
    "review_text": "Good product, but a bit expensive",
    "date": datetime.now() - timedelta(days=1),
}
review3 = {
    "name": "Emily Johnson",
    "item_id": item["_id"],
    "rating": 3,
    "review_text": "Just okay, not worth the price",
    "date": datetime.now() - timedelta(days=2),
}
review4 = {
    "name": "Michael Brown",
    "item_id": item["_id"],
    "rating": 5,
    "review_text": "Love it! The best smartphone out there",
    "date": datetime.now() - timedelta(days=3),
}
review5 = {
    "name": "David Smith",
    "item_id": item["_id"],
    "rating": 4,
    "review_text": "Great phone, but the sound could be better",
    "date": datetime.now() - timedelta(days=4),
}
review6 = {
    "name": "Andrii Rodionov",
    "item_id": item["_id"],
    "rating": 5,
    "review_text": "Excellent picture quality, highly recommend!",
    "date": datetime.now() - timedelta(days=5),
}
db.reviews.insert_many([review1, review2, review3, review4, review5, review6])

# check the number of reviews in the collection
review_count = db.reviews.count_documents({})
print("\nNumber of reviews:", review_count)

# close the connection
client.close()
