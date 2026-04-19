from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 🔐 API KEY (from .env locally OR Render environment variables)
API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_game(name, genre, character, enemy):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 🎮 GAME NAME PROMPT
    name_prompt = f"""
Create a short and powerful game name.

Player: {name}
Genre: {genre}
Character: {character}
Enemy: {enemy}

Give ONLY one game name.
"""

    name_data = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": name_prompt}],
        "temperature": 0.9
    }

    name_res = requests.post(url, headers=headers, json=name_data)

    if name_res.status_code == 200:
        game_name = name_res.json()["choices"][0]["message"]["content"]
    else:
        game_name = "UNKNOWN GAME"

    # 🎮 STORY PROMPT (UNCHANGED LOGIC)
    story_prompt = f"""
You are a game story writer.

Game Name: {game_name}
Player: {name}
Genre: {genre}
Character: {character}
Enemy: {enemy}

Write a simple game story.

Format:

GAME INTRO
MISSION
ENEMY
WORLD
ENDING

Rules:
- Simple English
- Short sentences
- Clear ending required
"""

    story_data = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": story_prompt}],
        "temperature": 0.8
    }

    story_res = requests.post(url, headers=headers, json=story_data)

    if story_res.status_code == 200:
        story = story_res.json()["choices"][0]["message"]["content"]
    else:
        story = "Error generating story"

    # 📦 RETURN ALL DATA
    return {
        "game_name": game_name,
        "story": story,
        "genre": genre
    }


# 🌐 HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# ⚡ API ENDPOINT
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    result = generate_game(
        data["name"],
        data["genre"],
        data["character"],
        data["enemy"]
    )

    return jsonify(result)


# 🚀 DEPLOYMENT SAFE RUN (IMPORTANT PART)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)