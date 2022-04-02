const BASE_URL = "http://localhost:5000";

// TODO: Make the title "Message Board"
fetch(`${BASE_URL}/welcome/Not%20%A%20Message%20Board`)
  .then((resp) => {
    return resp.text();
  })
  .then((text) => {
    document.getElementById("welcome-text").innerText = text;
  })
  .catch((err) => {
    console.error(err);
  });
