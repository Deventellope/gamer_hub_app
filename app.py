from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    featured_games = [
        {"title": "NEON OVERDRIVE", "genre": "FPS", "players": "42.1K"},
        {"title": "VOID WALKER", "genre": "RPG", "players": "12.5K"},
        {"title": "CORE COMMAND", "genre": "STRATEGY", "players": "8.9K"}
    ]
    return render_template('index.html', games=featured_games)

if __name__ == '__main__':
    app.run(debug=True)
