import rethinkdb as r

# Connect, defaults are 'localhost', 28015, and the 'test' db.
conn = r.connect(host='50.116.0.34', port=28015, db='CheeseRealtime')

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


# Start a changefeed
cheese_cursor = r.table('Cheese').changes().run(conn)
for cheese in cheese_cursor:
    print(cheese)

