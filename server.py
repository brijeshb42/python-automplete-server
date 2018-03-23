try:
    from flask_server import app
    application = app;
except Exception as e:
    from base_server import app
    application = app


if __name__ == '__main__':
    application.run(debug=True)
