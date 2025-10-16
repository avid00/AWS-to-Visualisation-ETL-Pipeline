import psycopg2
conn = psycopg2.connect(
    host="strokeetl-db.c7iguuus6617.eu-west-1.rds.amazonaws.com",
    database="strokeetl",
    user="postgres",
    password="Secretpassword!",
    port=5432
)
print("Connected successfully!")
conn.close()


# psql -h strokeetl-db.c7iguuus6617.eu-west-1.rds.amazonaws.com -U postgres -d strokeetl
