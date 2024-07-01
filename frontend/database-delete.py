# DELETE FROM public.webpage

import psycopg2

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    dbname="TestDB",
    user="aryanbhat",
    password="aryanbhat",
    host="localhost",
    port="5432"
)

# Create a cursor object using the connection
cur = conn.cursor()

# Delete all rows in the table
cur.execute('DELETE FROM public."Latest_Recommendation"')
cur.execute('DELETE FROM public."Recommendation_History"')

# Commit the changes
conn.commit()

# Close the cursor and the connection
cur.close()
conn.close()