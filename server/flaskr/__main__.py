from flaskr import config

if __name__ == "__main__":
    print("this running")
    app = config.create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

