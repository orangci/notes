let random_message_element = "random_message";
const messages = ["example random message"];
document.getElementById(random_message_element).textContent = messages[Math.floor(Math.random() * messages.length)];