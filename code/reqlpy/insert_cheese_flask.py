import rethinkdb as r

# Connect
conn = r.connect(host='50.116.0.34', port=28015, db='CheeseFlask')

# Insert some records into the table
r.table('Cheese').insert([
    {'id':1,
        'flavor': 'Swiss',
     'status': 'Moved'
     }
]).run(conn)
