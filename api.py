# from flask import Flask, request, jsonify,render_template,redirect,url_for
# from app.group import Group
# from app.member import Member

# app = Flask(__name__, template_folder="templates", static_folder="static")

# @app.route("/")
# def home():
#     return render_template("index.html")
# @app.route("/dashboard")
# def dashboard():
#     return render_template("dashboard.html")


# # In-memory stores
# members = {}
# groups = {}

# # Set key range
# Group.set_key_range(127, 128)
# Member.set_key_range(127, 128)

# @app.route("/sign_up", methods=["POST"])
# def sign_up():
#     data = request.json
#     name = data.get("name")
#     password = data.get("password")
#     if not name or not password:
#         return jsonify({"error": "Name and password required"}), 400

#     for member in members.values():
#         if member.name == name:
#             return jsonify({"error": "Member already exists"}), 400

#     mem_id = len(members) + 1
#     m = Member(mem_id, name, password)
#     members[mem_id] = m
#     return jsonify({"message": "Signup successful", "member_id": mem_id})

# @app.route("/log_in", methods=["POST"])
# def log_in():
#     data = request.json
#     name = data.get("name")
#     password = data.get("password")

#     for member in members.values():
#         if member.name == name and member.password == password:
#             return jsonify({
#                 "success": True,
#                 "member_id": member.id,
#                 "name": member.name
#             })
#     return jsonify({"success": False, "error": "Invalid credentials"}), 401

# def create_member():
#     mem_id = len(members) + 1
#     name = request.json.get("name", f"Member {mem_id}")
#     m = Member(mem_id, name)

#     members[mem_id] = m
#     return jsonify({"message": f"Member {mem_id} created", "member_id": mem_id})

# @app.route("/create_group", methods=["POST"])
# def create_group():
#     data = request.json
#     mem_id = data.get("member_id")
    
#     if mem_id not in members:
#         return jsonify({"error": "Invalid member ID"}), 400

#     group_id = len(groups) + 1
#     group_name = data.get("name", f"Group {group_id}")
#     g = Group(group_id, group_name)

#     g.add_member(members[mem_id])
#     groups[group_id] = g

#     return jsonify({"message": f"Group {group_id} created with member {mem_id} as admin", "group_id": group_id})

# @app.route("/add_member", methods=["POST"])
# def add_member():
#     data = request.json
#     admin_id = data.get("admin_id")
#     target_id = data.get("target_id")
#     group_id = data.get("group_id")

#     if group_id not in groups or admin_id not in members or target_id not in members:
#         return jsonify({"error": "Invalid input"}), 400

#     success = members[admin_id].add_member_to_group(members[target_id], groups[group_id])
#     return jsonify({"success": success})

# @app.route("/send_message", methods=["POST"])
# def send_message():
#     data = request.json
#     sender_id = int(data.get("sender_id"))
#     group_id = int(data.get("group_id"))
#     message = data.get("message")

#     if sender_id not in members or group_id not in groups:
#         return jsonify({"error": "Invalid input"}), 400

#     members[sender_id].add_message_to_group(groups[group_id], message)
#     return jsonify({"message": "Message sent"})

# @app.route("/read_messages", methods=["GET"])
# def read_messages():
#     member_id = int(request.args.get("member_id"))

#     if member_id not in members:
#         return jsonify({"error": "Invalid member ID"}), 400

#     return jsonify({
#         "messages": [
#             {"text": msg[0], "source": msg[1]}
#             for msg in members[member_id].message_history
#         ]
#     })

# @app.route("/view_members", methods=["GET"])
# def view_members():
#     return jsonify([
#         {"id": mem.id, "name": mem.name}
#         for mem in members.values()
#     ])

# @app.route("/view_groups", methods=["GET"])
# def view_groups():
#     return jsonify([
#         {"id": g.id, "name": g.name, "admin": g.admin_id}
#         for g in groups.values()
#     ])

# @app.route("/group_members/<int:group_id>", methods=["GET"])
# def group_members(group_id):
#     group = groups.get(group_id)
#     if not group:
#         return jsonify({"error": "Group not found"}), 404
#     return jsonify([
#         {"id": m.id, "name": m.name}
#         for m in group.members.values()
#     ])



# api.py (fully corrected and verified with explicit HTTP methods)
from flask import Flask, request, jsonify, render_template
from app.member import Member
from app.group import Group

app = Flask(__name__)

members = {}
groups = {}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/sign_up", methods=["POST"])
def sign_up():
    try:
        data = request.get_json(force=True)
        name = data.get("name")
        password = data.get("password")
        if not name or not password:
            return jsonify({"error": "Name and password required"}), 400

        for member in members.values():
            if member.name == name:
                return jsonify({"error": "Member already exists"}), 400

        mem_id = len(members) + 1
        m = Member(mem_id, name, password)
        members[mem_id] = m
        return jsonify({"message": "Signup successful", "member_id": mem_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/log_in", methods=["POST"])
def log_in():
    try:
        data = request.get_json(force=True)
        name = data.get("name")
        password = data.get("password")

        for member in members.values():
            if member.name == name and member.password == password:
                return jsonify({"success": True, "member_id": member.id, "name": member.name})
        return jsonify({"success": False, "error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/create_group", methods=["POST"])
def create_group():
    try:
        data = request.get_json(force=True)
        name = data.get("name")
        member_id = int(data.get("member_id"))
        if not name or member_id not in members:
            return jsonify({"error": "Invalid data"}), 400

        group_id = len(groups) + 1
        group = Group(group_id, name)
        group.add_member(members[member_id])
        group.set_admin(member_id)
        groups[group_id] = group
        return jsonify({"message": "Group created", "id": group_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/add_member", methods=["POST"])
def add_member():
    try:
        data = request.get_json(force=True)
        admin_id = int(data.get("admin_id"))
        target_id = int(data.get("target_id"))
        group_id = int(data.get("group_id"))
        if admin_id not in members or target_id not in members or group_id not in groups:
            return jsonify({"error": "Invalid data"}), 400

        result = groups[group_id].add_member(members[target_id], admin_id)
        return jsonify({"success": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/remove_member", methods=["POST"])
def remove_member():
    try:
        data = request.get_json(force=True)
        admin_id = int(data.get("admin_id"))
        target_id = int(data.get("target_id"))
        group_id = int(data.get("group_id"))
        if admin_id not in members or target_id not in members or group_id not in groups:
            return jsonify({"error": "Invalid data"}), 400

        result = groups[group_id].remove_member(members[target_id], admin_id)
        return jsonify({"success": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/send_message", methods=["POST"])
def send_message():
    try:
        data = request.get_json(force=True)
        sender_id = int(data.get("sender_id"))
        group_id = int(data.get("group_id"))
        message = data.get("message")
        if not message or sender_id not in members or group_id not in groups:
            return jsonify({"error": "Invalid input"}), 400

        result = groups[group_id].send_message(sender_id, message)
        return jsonify({"message": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/read_messages", methods=["GET"])
def read_messages():
    try:
        member_id = int(request.args.get("member_id"))
        if member_id not in members:
            return jsonify({"error": "Invalid member ID"}), 400

        messages = members[member_id].message_history
        return jsonify({"messages": messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/view_members", methods=["GET"])
def view_members():
    try:
        return jsonify([{"id": m.id, "name": m.name} for m in members.values()])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/view_groups", methods=["GET"])
def view_groups():
    try:
        return jsonify([{"id": g.id, "name": g.name} for g in groups.values()])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/group_members/<int:group_id>", methods=["GET"])
def group_members(group_id):
    try:
        if group_id not in groups:
            return jsonify([])
        group = groups[group_id]
        return jsonify([{"id": m.id, "name": m.name} for m in group.members])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


