from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

STATE_FILE = Path("bowl_state.json")

def load_state():
    with STATE_FILE.open() as f:
        return json.load(f)

def save_state(state):
    with STATE_FILE.open("w") as f:
        json.dump(state, f)

@app.route("/get_state", methods=["GET"])
def get_state():
    return jsonify(load_state())

@app.route("/move_clip", methods=["POST"])
def move_clip():
    try:
        data = request.get_json()
        print(data)
        clip_id = int(data.get("id"))
        direction = data.get("direction")

        bowl_state = load_state()

        if direction == "left_to_right":
            source, target = "left", "right"
        elif direction == "right_to_left":
            source, target = "right", "left"
        else:
            return jsonify({"error": "Invalid direction"}), 400

        # Find the clip in the source bowl
        clip_to_move = next((clip for clip in bowl_state[source] if clip["id"] == clip_id), None)

        if not clip_to_move:
            return jsonify({"error": f"Clip with id {clip_id} not found in {source} bowl"}), 404

        # Remove from source and add to target
        bowl_state[source] = [clip for clip in bowl_state[source] if clip["id"] != clip_id]
        bowl_state[target].append(clip_to_move)

        save_state(bowl_state)

        return jsonify(bowl_state), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

