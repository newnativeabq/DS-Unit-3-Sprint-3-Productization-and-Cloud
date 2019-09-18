from twittoff import create_app


app = create_app()

@app.route('/')
def home():
    return 'Home Page'

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)