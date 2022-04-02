function getMessages() {
  fetch("http://localhost:5000/messages")
    .then((resp) => resp.json())
    .then((messages) => {
      const html = messages
        .map(
          (message) => `
        <div class="message">
          <h2>From: ${message.author}</h2>
          <p>${message.content}</p>
        </div>
      `
        )
        .join("");
      document.getElementById("messages").innerHTML = html;
    })
    .catch((err) => {
      console.error(err);
    });
}
