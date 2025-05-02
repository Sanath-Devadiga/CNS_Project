console.log("✅ script.js loaded");

function signUp() {
  const name = document.getElementById("signup-name").value;
  const password = document.getElementById("signup-password").value;

  if (!name || !password) {
    alert("Name and password required");
    return;
  }

  fetch("/sign_up", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.member_id) {
        alert("✅ Signup successful! You can now log in.");
      } else {
        alert("❌ " + data.error);
      }
    })
    .catch(err => {
      console.error(err);
      alert("❌ Signup failed.");
    });
}

function logIn() {
  const name = document.getElementById("login-name").value;
  const password = document.getElementById("login-password").value;

  if (!name || !password) {
    alert("Name and password required");
    return;
  }

  fetch("/log_in", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, password })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        localStorage.setItem("user", JSON.stringify(data));
        window.location.href = "/dashboard";
      } else {
        alert("❌ " + data.error);
      }
    })
    .catch(err => {
      console.error(err);
      alert("❌ Login failed.");
    });
}

function logout() {
  localStorage.removeItem("user");
  window.location.href = "/";
}
 
function authId() {
    const user = JSON.parse(localStorage.getItem("user"));
    return user?.member_id;
  }
  
  async function createGroup() {
    const name = document.getElementById("group-name").value;
    const member_id = authId();
    const res = await fetch("/create_group", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, member_id })
    });
    const data = await res.json();
    alert(res.ok ? "Group created." : data.error);
  }
  
  async function addMemberToGroup() {
    const admin_id = authId();
    const group_id = document.getElementById("group-id-add").value;
    const target_id = document.getElementById("member-id-add").value;
    const res = await fetch("/add_member", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ admin_id, target_id, group_id })
    });
    const data = await res.json();
    alert(data.success ? "Member added." : data.error || "Failed");
  }
  
  async function removeMemberFromGroup() {
    const admin_id = authId();
    const group_id = document.getElementById("group-id-remove").value;
    const target_id = document.getElementById("member-id-remove").value;
    const res = await fetch("/remove_member", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ admin_id, target_id, group_id })
    });
    const data = await res.json();
    alert(data.success ? "Member removed." : data.error || "Failed");
  }
  
  async function sendMessage() {
    const sender_id = authId();
    const group_id = document.getElementById("message-group-id").value;
    const message = document.getElementById("message-text").value;
    const res = await fetch("/send_message", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender_id, group_id, message })
    });
    const data = await res.json();
    alert(data.message || data.error);
  }
  
  async function readMessages() {
    const member_id = authId();
    const res = await fetch(`/read_messages?member_id=${member_id}`);
    const data = await res.json();
    const list = document.getElementById("message-list");
    list.innerHTML = "";
    (data.messages || []).forEach(m => {
      const li = document.createElement("li");
      li.textContent = `"${m.text}" from ${m.source}`;
      list.appendChild(li);
    });
  }
  
  async function viewMembers() {
    const res = await fetch("/view_members");
    const data = await res.json();
    alert(data.map(m => `${m.name} (ID: ${m.id})`).join("\n"));
  }
  
  async function viewGroups() {
    const res = await fetch("/view_groups");
    const data = await res.json();
    alert(data.map(g => `${g.name} (ID: ${g.id})`).join("\n"));
  }
  
  async function viewGroupMembers() {
    const group_id = document.getElementById("group-id-view").value;
    const res = await fetch(`/group_members/${group_id}`);
    const data = await res.json();
    if (res.ok && Array.isArray(data)) {
      alert(data.map(m => `${m.name} (ID: ${m.id})`).join("\n"));
    } else {
      alert("Group not found or empty");
    }
  }
  