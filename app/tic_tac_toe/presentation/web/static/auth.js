


const isUserAuthenticated = () => {
    const userSession = localStorage.getItem("userSession")

    if (!userSession && window.location.pathname !== "/web/login") {
        window.location.href = "/web/login"
    }

    return userSession
}

function saveUserSession(userSession) {
    localStorage.setItem("userSession", userSession)
    setCookie("userSession", userSession, 900)
}

function getUserSession() {
    return localStorage.getItem("userSession")
}

function removeUserSession() {
    localStorage.removeItem("userSession")
    setCookie("userSession", "", 0)
    window.location.href = "/web/login"
}


function setCookie(cname, cvalue, expSeconds) {
    const d = new Date();
    d.setTime(d.getTime() + (expSeconds*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }


function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}

const onLogin = () => {
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

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

    return fetch("/api/v1/player/auth", requestOptions)
    .then((response) => {
        if (!response.ok) {
            throw new Error("Invalid User");
        }
        return response.json()
    })
    .then((result) => {
        saveUserSession(result.user_session)
        window.location.href = "/web"
    })
    .catch((error) => console.error(error));
}


const onSignUp = () => {
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

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

    return fetch("/api/v1/player", requestOptions)
    .then((response) => {
        if (!response.ok) {
            throw new Error("Invalid User");
        }
        return response.json()
    })
    .then((result) => {
        saveUserSession(result.user_session)
        window.location.href = "/web"
    })
    .catch((error) => console.error(error));
}

