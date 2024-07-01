import asyncio
import websockets
import json
import psycopg2

# Function to fetch data from the PostgreSQL database
async def fetch_data_from_database():
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

    # Fetch data from the database
    cur.execute('SELECT * FROM "Recommendation_History" ORDER BY timestamp DESC')
    data = cur.fetchall()

    # Close the cursor and the connection
    cur.close()
    conn.close()

    return data

# WebSocket server handler
async def websocket_server(websocket, path):
    while True:
        # Fetch data from the database
        webpageData = await fetch_data_from_database()

        # Convert data to JSON format
        json_data = json.dumps(webpageData)

        # Send the JSON data to the client
        await websocket.send(json_data)

        # Wait for 10 second before fetching data again
        await asyncio.sleep(10)

# Start the WebSocket server
start_server = websockets.serve(websocket_server, "localhost", 8766)

# Run the event loop
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
