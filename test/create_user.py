from models import create_user
from manage import app
from config import USER_INFO

with app.app_context():
    username = USER_INFO["username"]
    password = USER_INFO["password"]
    email = USER_INFO["email"]
    role = 1
    USER = create_user(username, password, email, role)
    print(USER)
