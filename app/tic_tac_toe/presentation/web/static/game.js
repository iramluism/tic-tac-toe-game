


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
        window.location.href = "/web/game"
    })
    .catch((error) => console.error(error));
}


const startGameChannel = () => {
    const userSession = localStorage.getItem("userSession");
    const gameSessionId = localStorage.getItem("gameSessionId");

    const url = `ws://${window.location.host}/ws/game/${gameSessionId}/?user_session=${userSession}`;
    const chatSocket = new WebSocket(url);

    chatSocket.onmessage = function(e) {
        console.log(e);
        const data = JSON.parse(e.data);
        document.querySelector('#chat-log').value += (data.message + '\n');
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}