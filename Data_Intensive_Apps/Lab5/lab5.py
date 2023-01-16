import json
import time
import uuid
from cassandra.cluster import Cluster
from datetime import datetime, timedelta


# Docker: docker run -it --rm -p 9042:9042 -v "C:\Users\Nazar\PythonWorkspace\Programming-Labs\Data_Intensive_Apps\Lab5\cassandra.yaml":/etc/cassandra/cassandra.yaml --name test-cassandra cassandra
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect()

# create keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS store 
    WITH replication = {
        'class': 'SimpleStrategy', 
        'replication_factor': 1
    }
""")
session.execute("USE store")

session.execute("DROP INDEX IF EXISTS properties_idx")
session.execute("DROP INDEX IF EXISTS order_items_idx")
session.execute("DROP INDEX IF EXISTS total_sum_idx")
session.execute("DROP MATERIALIZED VIEW IF EXISTS items_by_price")
session.execute("DROP MATERIALIZED VIEW IF EXISTS items_by_name")
session.execute("DROP MATERIALIZED VIEW IF EXISTS items_by_price_manufacturer")
session.execute("DROP MATERIALIZED VIEW IF EXISTS orders_by_date")
session.execute("DROP TABLE IF EXISTS items")
session.execute("DROP TABLE IF EXISTS orders")

# create items
session.execute("""
    CREATE TABLE items (
        id uuid,
        name text,
        price float,
        manufacturer text,
        category text,
        properties map<text, text>,
        PRIMARY KEY ((category), manufacturer, id)
    )
""")
session.execute("CREATE INDEX IF NOT EXISTS properties_idx ON items (KEYS(properties))")
session.execute("""
    CREATE MATERIALIZED VIEW items_by_price AS
        SELECT category, price, manufacturer, name, id
        FROM items
        WHERE category IS NOT NULL AND price IS NOT NULL AND manufacturer IS NOT NULL AND id IS NOT NULL
        PRIMARY KEY ((category), price, manufacturer, id)
""")
session.execute("""
    CREATE MATERIALIZED VIEW items_by_name AS
        SELECT category, price, manufacturer, name, id
        FROM items
        WHERE category IS NOT NULL AND name IS NOT NULL AND manufacturer IS NOT NULL AND id IS NOT NULL
        PRIMARY KEY ((category), name, manufacturer, id)
""")
session.execute("""
    CREATE MATERIALIZED VIEW items_by_price_manufacturer AS
        SELECT category, price, manufacturer, name, id
        FROM items
        WHERE category IS NOT NULL AND price IS NOT NULL AND manufacturer IS NOT NULL AND id IS NOT NULL
        PRIMARY KEY ((category), manufacturer, price, id)
""")

phones = [
    {
        "category": "Phone",
        "model": "iPhone 6",
        "manufacturer": "Apple",
        "price": 600,
        "properties": {
            "screen_size": "4.7 inches",
            "storage": "64GB",
            "color": "Silver"
        },
    },
    {
        "category": "Phone",
        "model": "Samsung Galaxy S21",
        "manufacturer": "Samsung",
        "price": 800,
        "properties": {
            "screen_size": "6.2 inches",
            "storage": "128GB",
            "color": "Gray"
        },
    },
    {
        "category": "Phone",
        "model": "Google Pixel 5",
        "manufacturer": "Google",
        "price": 700,
        "properties": {"screen_size": "6 inches", "storage": "64GB", "color": "Black"},
    },
]
tvs = [
    {
        "category": "TV",
        "model": "Samsung QLED",
        "manufacturer": "Samsung",
        "price": 1500,
        "properties": {
            "screen_size": "65 inches",
            "resolution": "4K",
            "smart_tv": "Yes"
        },
    },
    {
        "category": "TV",
        "model": "LG OLED",
        "manufacturer": "LG",
        "price": 1700,
        "properties": {
            "screen_size": "55 inches",
            "resolution": "4K",
            "smart_tv": "Yes"
        },
    },
    {
        "category": "TV",
        "model": "Sony Bravia",
        "manufacturer": "Sony",
        "price": 1600,
        "properties": {
            "screen_size": "50 inches",
            "resolution": "4K",
            "smart_tv": "Yes"
        },
    },
]
smart_watches = [
    {
        "category": "Smart Watch",
        "model": "Apple Watch Series 6",
        "manufacturer": "Apple",
        "price": 400,
        "properties": {
            "display": "Retina",
            "storage": "32GB",
            "water_resistant": "Yes",
            "heart_rate_monitor": "Yes"
        },
    },
    {
        "category": "Smart Watch",
        "model": "Samsung Galaxy Watch",
        "manufacturer": "Samsung",
        "price": 350,
        "properties": {
            "display": "AMOLED",
            "storage": "16GB",
            "water_resistant": "Yes",
            "heart_rate_monitor": "Yes"
        },
    },
    {
        "category": "Smart Watch",
        "model": "Fitbit Versa 3",
        "manufacturer": "Fitbit",
        "price": 300,
        "properties": {"display": "LCD", "storage": "4GB", "water_resistant": "Yes"}
    },
]
for item in sum([phones, tvs, smart_watches], []):
    session.execute(f"INSERT INTO items (id, name, price, manufacturer, category, properties) VALUES ({uuid.uuid1()},'{item['model']}', {item['price']}, '{item['manufacturer']}', '{item['category']}', {item['properties']})")


# describe the table structure
print(f'\nTable structure:')
result = session.execute("DESCRIBE TABLE items")
for row in result:
    print(row)

# select all items where category is "Phone" and order by price
print(f'\nAll items where category is "Phone" and order by price:')
result = session.execute("SELECT * FROM items_by_price WHERE category = 'Phone' ORDER BY price")
for row in result:
    print(row)

# select all items where category is "Phone" and name is "Samsung Galaxy S21"
print(f'\nAll items where category is "Phone" and name is "Samsung Galaxy S21":')
result = session.execute("SELECT * FROM items_by_name WHERE category = 'Phone' AND name = 'Samsung Galaxy S21'")
for row in result:
    print(row)

# select all items where category is "Phone" and price is between 700 and 800
print(f'\nAll items where category is "Phone" and name is between 700 and 800:')
result = session.execute("SELECT * FROM items_by_price WHERE category = 'Phone' AND price >= 700 AND price <= 800")
for row in result:
    print(row)

# select all items by category, price and manufacturer where category is "TV" and price is between 1600 and 1700 and manufacturer is "LG"
print(f'\nAll items where category is "TV" and price is between 1600 and 1700 and manufacturer is "LG":')
result = session.execute("SELECT * FROM items_by_price_manufacturer WHERE category = 'TV' AND price >= 1600 AND price <= 1700 AND manufacturer = 'LG'")
for row in result:
    print(row)

# select products that have the property "color"
print(f'\nProducts that have the property "color":')
results = session.execute("SELECT * FROM items WHERE category='Phone' AND properties CONTAINS 'color' ALLOW FILTERING")
for row in results:
    print(row)

# select products that have the property "color" with the value "Silver"
print(f'\nProducts that have the property "color" with the value "Silver":')
results = session.execute("SELECT * FROM items WHERE category='Phone' AND properties['color'] = 'Silver' ALLOW FILTERING")
for row in results:
    print(row)

# set properties['color'] to "white"
phone_id = session.execute("SELECT id FROM items_by_price WHERE category='Phone' ORDER BY price DESC LIMIT 1").one().id
session.execute("UPDATE items SET properties['color'] = 'White' WHERE category='Phone' AND manufacturer = 'Samsung' AND id = %s", (phone_id,))

# add new property "battery life" with value "2 days"
session.execute("UPDATE items SET properties = properties + {'battery life': '2 days'} WHERE category='Phone' AND manufacturer = 'Samsung' AND id = %s", (phone_id,))

# remove property "color"
session.execute("UPDATE items SET properties = properties - {'color'} WHERE category='Phone' AND manufacturer = 'Samsung' AND id = %s", (phone_id,))


# create orders
session.execute("""
    CREATE TABLE orders (
        order_number int,
        date timestamp,
        total_sum float,
        customer_name text,
        order_items list<uuid>,
        PRIMARY KEY (customer_name, order_number)
    )
""")
session.execute("CREATE INDEX IF NOT EXISTS order_items_idx ON orders (order_items)")
session.execute("CREATE INDEX IF NOT EXISTS total_sum_idx ON orders (total_sum)")
session.execute("""
    CREATE MATERIALIZED VIEW orders_by_date AS
        SELECT customer_name, date, total_sum, order_number
        FROM orders
        WHERE customer_name IS NOT NULL AND date IS NOT NULL AND order_number IS NOT NULL
        PRIMARY KEY (customer_name, date, order_number)
""")

result = session.execute("SELECT id FROM items_by_price WHERE category = 'Phone' AND price >= 700 AND price <= 800")
item1, item2 = [row.id for row in result]
result = session.execute("SELECT id FROM items_by_price WHERE category = 'Smart Watch' AND price = 300")
item3 = result.one().id
result = session.execute("SELECT id FROM items WHERE category = 'TV'")
item4, item5, item6 = [row.id for row in result]
session.execute("INSERT INTO orders (order_number, date, total_sum, customer_name, order_items) VALUES (%s, %s, %s, %s, %s)", (201513, datetime.now(), 1923.4, 'Andrii Rodionov', [item1, item2]))
session.execute("INSERT INTO orders (order_number, date, total_sum, customer_name, order_items) VALUES (%s, %s, %s, %s, %s)", (201514, datetime.now() - timedelta(days=1), 900, 'John Doe', [item3, item2]))
session.execute("INSERT INTO orders (order_number, date, total_sum, customer_name, order_items) VALUES (%s, %s, %s, %s, %s)", (201515, datetime.now() - timedelta(days=2), 1200, 'Jane Doe', [item4, item5]))

# describe the table structure
print(f'\n\nTable structure:')
result = session.execute("DESCRIBE orders")
for row in result:
    print(row)

# all orders of a customer sorted by the time when they were made
customer_name = 'Andrii Rodionov'
print(f'\nOrders of a customer sorted by the time when they were made:')
result = session.execute("SELECT * FROM orders_by_date WHERE customer_name = %s ORDER BY date", (customer_name,))
for row in result:
    print(row)

# find the order with a certain product for a customer
print(f'\nOrder with a certain product for a customer:')
result = session.execute("SELECT * FROM orders WHERE customer_name = %s AND order_items CONTAINS %s", (customer_name, item1,))
for row in result:
    print(row)

# find the orders for a certain period of time and their quantity for a customer
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)
print(f'\nOrders for a certain period of time and their quantity for a customer:')
result = session.execute("SELECT COUNT(*) as count, SUM(total_sum) as total_sum FROM orders_by_date WHERE customer_name = %s AND date >= %s AND date <= %s", (customer_name, start_date, end_date,))
for row in result:
    print(row)

# determine the amount for which all his orders were made for each customer
print(f'\nTotal amount for each customer:')
result = session.execute("SELECT customer_name, SUM(total_sum) as total_sum FROM orders GROUP BY customer_name")
for row in result:
    print(row)

# determine the order with the maximum value for each customer
print(f'\nThe order with the maximum value for each customer:')
result = session.execute("SELECT customer_name, MAX(total_sum) as total_sum FROM orders GROUP BY customer_name")
for row in result:
    cn, mts = row.customer_name, row.total_sum
    r = session.execute("SELECT * FROM orders WHERE customer_name = %s AND total_sum = %s", (cn, mts,)).one()
    print(r)

# modify a specific order by adding one item while also changing the order value
order_number = 201513
phone_id_price = session.execute("SELECT price FROM items WHERE category='Phone' AND manufacturer = 'Samsung' AND id = %s", (phone_id,)).one().price
result = session.execute("SELECT total_sum FROM orders WHERE customer_name = %s AND order_number = %s", (customer_name, order_number))
total_sum = result.one().total_sum + phone_id_price
session.execute("UPDATE orders SET order_items = order_items + [%s], total_sum = %s WHERE customer_name = %s AND order_number = %s", (phone_id, total_sum, customer_name, order_number,))

# display the time when the price was entered into the database (SELECT WRITETIME)
print(f'\nThe time when the price was entered into the database:')
result = session.execute("SELECT WRITETIME(total_sum) FROM orders WHERE customer_name = %s AND order_number = %s", (customer_name, order_number,))
for row in result:
    print(row)

# create an order with a certain time to live (TTL), after which it will be deleted
order_number = 201516
customer_name = 'Mike Johnson'
order_items = [item6]
total_sum = 800
date = datetime.now()
ttl = 5 # 5 seconds
session.execute("INSERT INTO orders (order_number, date, total_sum, customer_name, order_items) VALUES (%s, %s, %s, %s, %s) USING TTL %s", (order_number, date, total_sum, customer_name, order_items, ttl,))
time.sleep(6)

# return the order in JSON format
print(f'\nThe order in JSON format:')
result = session.execute("SELECT JSON * FROM orders WHERE customer_name = %s AND order_number = %s", (customer_name, order_number,))
for row in result:
    print(row)

# add an order in JSON format
json_order = json.dumps({
    "order_number": str(order_number), 
    "date": date.isoformat(), 
    "total_sum": total_sum, 
    "customer_name": customer_name,
    "order_items": list(map(str, order_items))
})
session.execute("INSERT INTO orders JSON %s", (json_order,))


# close the session
session.shutdown()
cluster.shutdown()
