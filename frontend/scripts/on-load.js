fetch("http://localhost:5000/welcome/test").then((resp) => {
    return resp.text()
}).then((text) => {
    document.getElementById("welcome-text").innerText = text;
}).catch((err) => {
    console.error(err)
})