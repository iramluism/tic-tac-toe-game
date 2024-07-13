


const isUserAuthenticated = () => {
    const userSession = localStorage.getItem("userSession")

    if (!userSession && window.location.pathname !== "/web/login") {
        window.location.href = "/web/login"
    }

    return userSession
}

const onLogin = () => {
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    debugger

    const raw = JSON.stringify({
        "name": username,
        "password": password
      });

    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
        
    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
        };      

    debugger
    return fetch("/api/v1/player/auth", requestOptions)
    .then((response) => {
        if (!response.ok) {
            throw new Error("Invalid User");
        }
        return response.json()
    })
    .then((result) => {
        localStorage.setItem("userSession", result.user_session)
        window.location.href = "/web"
    })
    .catch((error) => console.error(error));
}


isUserAuthenticated()

