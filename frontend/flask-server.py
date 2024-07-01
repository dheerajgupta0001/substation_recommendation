# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
import psycopg2

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
# ‘/’ URL is bound with main() function.
def main():
    return render_template('main.html')

@app.route('/view_details')
# ‘/’ URL is bound with main() function.
def view_details():
    return render_template('view_details.html')

@app.route('/review')
# ‘/’ URL is bound with main() function.
def review():
    return render_template('review.html')

@app.route('/review', methods = ['POST'])
def send_review():
    conn = psycopg2.connect(
        dbname="TestDB",
        user="aryanbhat",
        password="aryanbhat",
        host="localhost",
        port="5432"
    )

    # Create a cursor object using the connection
    cur = conn.cursor()
    
    # Fetch data from url params
    timestamp = request.args.get('timestamp')
    substation = request.args.get('substation')
    recommendation = request.args.get('recommendation')
    review = request.form.get('review')
    # convert review to bool
    review = (review == 'true')
    print(review)

    # Update the review (boolean) in Recommendation_History
    cur.execute('UPDATE "Recommendation_History" SET review = %s WHERE timestamp = %s AND substation_name = %s', (review, timestamp, substation))
    
    # Commit the changes
    conn.commit()

    # Close the cursor and the connection
    cur.close()
    conn.close()

    return render_template('review.html')

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(port=8000,debug=True)
