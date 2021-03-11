from app import app

@app.route("/")
@app.route("/index")
def index():
    return "Hello World!"

@app.route("/api/users")
def get_users():
    """ This returns users """
    data = {
        "id": 123,
        "username": "test"
    }
    return data