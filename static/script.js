const form = document.getElementById("form");
const input = document.getElementById("input");
const messages = document.getElementById("messages");

const GREETING = "Hello. I'm FlexyBio-Ki! How can I help you today?";

// Build one message row: avatar + author label + text.
function addRow(text, who) {
    const row = document.createElement("div");
    row.className = "row " + who;

    const avatar = document.createElement("div");
    avatar.className = "avatar";
    avatar.textContent = who === "user" ? "You" : "FK";

    const body = document.createElement("div");
    body.className = "body";

    const author = document.createElement("div");
    author.className = "author";
    author.textContent = who === "user" ? "You" : "FlexyBio-Ki";

    const content = document.createElement("div");
    content.className = "content";
    content.textContent = text;

    body.append(author, content);
    row.append(avatar, body);
    messages.appendChild(row);
    messages.scrollTop = messages.scrollHeight;
    return content;
}

function reset() {
    messages.innerHTML = "";
    addRow(GREETING, "bot");
    input.focus();
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    addRow(text, "user");
    input.value = "";

    const pending = addRow("", "bot");
    pending.classList.add("typing");
    pending.innerHTML = "<span></span><span></span><span></span>";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text }),
        });
        const data = await res.json();
        pending.classList.remove("typing");
        pending.textContent = data.reply;
    } catch {
        pending.classList.remove("typing");
        pending.textContent = "Something went wrong. Please try again.";
    }
    messages.scrollTop = messages.scrollHeight;
});

document.getElementById("new-chat").addEventListener("click", reset);

// Dismiss the announcement bar.
document.getElementById("announce-close").addEventListener("click", () => {
    document.getElementById("announce").classList.add("hidden");
});

reset();
