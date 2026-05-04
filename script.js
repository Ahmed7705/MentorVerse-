function sendMessage(e) {
    e.preventDefault();
    alert("Message Sent");
}

function toggleFAQ(el) {
    let p = el.querySelector("p");
    p.style.display = (p.style.display === "block") ? "none" : "block";
}