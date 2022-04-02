const BASE_URL = "http://18.234.185.12:5000";

fetch(`${BASE_URL}/welcome/Message%20Board`)
  .then((resp) => {
    return resp.text();
  })
  .then((text) => {
    document.getElementById("welcome-text").innerText = text;
  })
  .catch((err) => {
    console.error(err);
  });
