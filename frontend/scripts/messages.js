function getMessages() {
  fetch(`${BASE_URL}/messages`)
    // parse json response
    .then((resp) => resp.json())
    .then((messages) => {
      // write messages into HTML to display
      const messagesAsHTML = messages.map(
        (message) => `
        <div class="message">
          <h4>From: ${message.author}</h4>
          <p>${message.content}</p>
        </div>
      `
      );

      messagesAsHTML.reverse();
      const html = messagesAsHTML.join("");

      // replace current message feed with new server response
      document.getElementById("messages").innerHTML = html;
    })
    .catch((err) => {
      console.error(err);
    });
}

function postMessage(e) {
  e.preventDefault();

  // get author and content from form
  const author = document.getElementById("author").value;
  const content = document.getElementById("content").value;

  // tell the api that we want to send this message
  fetch(`${BASE_URL}/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content, author }),
  })
    .then(() => getMessages())
    .catch((err) => {
      console.error(err);
    });
}
