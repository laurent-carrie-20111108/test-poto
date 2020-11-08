import os

from project import create_app

app = create_app(is_test=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8081)))
