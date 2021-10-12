from flask import Flask

# get the flask object
app = Flask(__name__)
# constructor is called when object is created 

# create the route and bind this route to a function
@app.route('/')

def home():
    return "you are on homepage"

# run the application
if __name__ == '__main__':
    app.run()