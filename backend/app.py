from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory state with paperclip objects
bowl_state = {
    "left": [
        {"id": 1, "name": "clipA", "size": 1},
        {"id": 2, "name": "clipB", "size": 2},
        {"id": 3, "name": "clipC", "size": 3},
        {"id": 4, "name": "clipD", "size": 2},
        {"id": 5, "name": "clipE", "size": 1},
        {"id": 6, "name": "clipF", "size": 2},
        {"id": 7, "name": "clipG", "size": 1}
    ],
    "right": []
}

@app.route("/get_state", methods=["GET"])
def get_state():
    return jsonify(bowl_state)

@app.route("/move_clip", methods=["POST"])
def move_clip():
    try:
        data = request.get_json()
        print(data)
        clip_id = int(data.get("id"))
        direction = data.get("direction")

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

        return jsonify(bowl_state), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

