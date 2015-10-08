import rethinkdb as r

# Connect, defaults are 'localhost', 28015, and the 'test' db.
conn = r.connect(host='50.116.0.34', port=28015, db='CheeseFlask')

# Create a new table
r.table_create('Cheese').run(conn)

# Insert some records into the table
r.table('Cheese').insert([
    {'flavor': 'Cheddar',
     'status': 'Available'
     },
    {'flavor': 'Swiss',
     'status': 'Gone'
     }
]).run(conn)


# Get all records back from the table using cursor
cheese_cursor = r.table('Cheese').run(conn)
for cheese in cheese_cursor:
    print(cheese)

# or just r.table('Cheese').run(conn) for display


# Now let's only find the cheeses that are moved
moved_cheese = r.table('Cheese').filter(r.row['status'] == 'Gone').run(conn)
for cheese in moved_cheese:
    print(cheese)



