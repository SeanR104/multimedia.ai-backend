from system import create_app

app = create_app("local")

if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"])
