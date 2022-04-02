fetch("http://localhost:5000/welcome/Message%20Board").then((resp) => {
    return resp.text()
}).then((text) => {
    document.getElementById("welcome-text").innerText = text;
}).catch((err) => {
    console.error(err)
})