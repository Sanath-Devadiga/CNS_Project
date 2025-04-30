from flask import Flask, request, jsonify
from app.group import Group
from app.member import Member

app = Flask(__name__)

# In-memory stores
members = {}
groups = {}

# Set key range
Group.set_key_range(127, 128)
Member.set_key_range(127, 128)

@app.route("/create_member", methods=["POST"])
def create_member():
    mem_id = len(members) + 1
    m = Member(mem_id)
    members[mem_id] = m
    return jsonify({"message": f"Member {mem_id} created", "member_id": mem_id})

@app.route("/create_group", methods=["POST"])
def create_group():
    data = request.json
    mem_id = data.get("member_id")
    
    if mem_id not in members:
        return jsonify({"error": "Invalid member ID"}), 400

    group_id = len(groups) + 1
    g = Group(group_id)
    g.add_member(members[mem_id])
    groups[group_id] = g

    return jsonify({"message": f"Group {group_id} created with member {mem_id} as admin", "group_id": group_id})

@app.route("/add_member", methods=["POST"])
def add_member():
    data = request.json
    admin_id = data.get("admin_id")
    target_id = data.get("target_id")
    group_id = data.get("group_id")

    if group_id not in groups or admin_id not in members or target_id not in members:
        return jsonify({"error": "Invalid input"}), 400

    success = members[admin_id].add_member_to_group(members[target_id], groups[group_id])
    return jsonify({"success": success})

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    sender_id = data.get("sender_id")
    group_id = data.get("group_id")
    message = data.get("message")

    if sender_id not in members or group_id not in groups:
        return jsonify({"error": "Invalid input"}), 400

    members[sender_id].add_message_to_group(groups[group_id], message)
    return jsonify({"message": "Message sent"})

@app.route("/read_messages", methods=["GET"])
def read_messages():
    member_id = int(request.args.get("member_id"))

    if member_id not in members:
        return jsonify({"error": "Invalid member ID"}), 400

    return jsonify({
        "messages": [
            {"text": msg[0], "source": msg[1]}
            for msg in members[member_id].message_history
        ]
    })

if __name__ == "__main__":
    app.run(debug=True)
