import rethinkdb as r

# Connect
conn = r.connect(host='50.116.0.34', port=28015, db='CheeseTornado')

# Create a new table
#r.table_create('Cheese').run(conn)

# Insert some records into the table
r.table('Cheese').insert([
    {'flavor': 'Yellow',
     'status': 'Moved'
     }
]).run(conn)
