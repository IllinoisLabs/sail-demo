const BASE_URL = "http://localhost:5000";

fetch(`${BASE_URL}/welcome/test`)
  .then((resp) => {
    return resp.text();
  })
  .then((text) => {
    document.getElementById("welcome-text").innerText = text;
  })
  .catch((err) => {
    console.error(err);
  });
