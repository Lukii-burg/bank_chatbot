let token = "";

function authHeaders() {
  return token ? { "Authorization": "Bearer " + token } : {};
}

async function login() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  // OAuth2 form login (x-www-form-urlencoded)
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body
  });

  const data = await res.json();
  if (!res.ok) {
    document.getElementById("loginStatus").innerText = "Login failed: " + (data.detail || res.status);
    return;
  }
  token = data.access_token;
  document.getElementById("loginStatus").innerText = "✅ Logged in. Token stored.";
}

async function predictTx() {
  const payload = {
    customer_id: document.getElementById("customer_id").value.trim(),
    amount: Number(document.getElementById("amount").value),
    currency: document.getElementById("currency").value.trim(),
    merchant: document.getElementById("merchant").value.trim(),
    channel: document.getElementById("channel").value.trim(),
    location: document.getElementById("location").value.trim()
  };

  const res = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  document.getElementById("predictOut").innerText = JSON.stringify(data, null, 2);
}

async function loadAlerts() {
  const res = await fetch("/alerts", { headers: authHeaders() });
  const data = await res.json();
  document.getElementById("alertsOut").innerText = JSON.stringify(data, null, 2);
}

async function loadCases() {
  const res = await fetch("/cases", { headers: authHeaders() });
  const data = await res.json();
  document.getElementById("casesOut").innerText = JSON.stringify(data, null, 2);
}

async function createCase() {
  const alertId = Number(document.getElementById("caseAlertId").value);
  const res = await fetch("/cases", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify({ alert_id: alertId, priority: "high" })
  });
  const data = await res.json();
  document.getElementById("casesOut").innerText = JSON.stringify(data, null, 2);
}

async function sendChat() {
  const payload = {
    message: document.getElementById("chatMsg").value,
    prediction_id: toIntOrNull("chatContextPred"),
    alert_id: toIntOrNull("chatContextAlert"),
    case_id: toIntOrNull("chatContextCase")
  };

  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  document.getElementById("chatOut").innerText = JSON.stringify(data, null, 2);
}

function toIntOrNull(id) {
  const v = document.getElementById(id).value.trim();
  if (!v) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}
