async function createMember() {
    const name = document.getElementById("member-name").value;
    const res = await fetch("/create_member", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name })
    });
    const data = await res.json();
    alert("Created: " + JSON.stringify(data));
  }
  
  async function createGroup() {
    const name = document.getElementById("group-name").value;
    const admin = parseInt(document.getElementById("group-admin").value);
    const res = await fetch("/create_group", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, member_id: admin })
    });
    const data = await res.json();
    alert("Group created: " + JSON.stringify(data));
  }
  
  async function sendMessage() {
    const sender_id = parseInt(document.getElementById("sender-id").value);
    const group_id = parseInt(document.getElementById("target-group").value);
    const message = document.getElementById("message").value;
    const res = await fetch("/send_message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender_id, group_id, message })
    });
    const data = await res.json();
    alert("Message sent: " + JSON.stringify(data));
  }
  
  async function readMessages() {
    const member_id = parseInt(document.getElementById("reader-id").value);
    const res = await fetch(`/read_messages?member_id=${member_id}`);
    const data = await res.json();
    const list = data.messages.map(msg => `<li>${msg.text} (from: ${msg.source})</li>`).join("");
    document.getElementById("messages").innerHTML = `<ul>${list}</ul>`;
  }
  