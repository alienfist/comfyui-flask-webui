from app import create_app
from config import WEB_PORT

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=WEB_PORT, host="0.0.0.0")
