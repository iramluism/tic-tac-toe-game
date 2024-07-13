


const startGame = () => {
    const myHeaders = new Headers();
    
    const userSession = localStorage.getItem("userSession");
    myHeaders.append("Authorization", userSession)

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        redirect: "follow"
    };

    return fetch("/api/v1/game/start", requestOptions)
    .then((response) => {
        if (!response.ok) {
            throw new Error("Invalid User");
        }
        return response.json()
    })
    .then((result) => {
        localStorage.setItem("gameSessionId", result.game_session_id)
        // window.location.href = "/game"
    })
    .catch((error) => console.error(error));
}