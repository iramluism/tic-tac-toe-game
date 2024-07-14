


const startGame = () => {
    const myHeaders = new Headers();
    
    const userSession = localStorage.getItem("userSession");

    myHeaders.append("Authorization", userSession)

    const requestOptions = {
        method: "POST",
        headers: myHeaders,
        redirect: "follow"
    };

    return fetch("/api/v1/games/start", requestOptions)
    .then((response) => {
        if (!response.ok) {
            throw new Error("Invalid User");
        }
        return response.json()
    })
    .then((result) => {
        localStorage.setItem("is_host", true)
        localStorage.setItem("gameSessionId", result.game_session_id)
        window.location.href = "/web/game"
    })
    .catch((error) => console.error(error));
}



const GameSessionComponent = ({host, bottonMessage, onClickButton}) => {
    let sessionElement = document.createElement('li')
        
    let hostElement = document.createElement('span')
    hostElement.textContent = host

    let connectButton = document.createElement("button")
    connectButton.className = 'connect-button';
    connectButton.textContent = bottonMessage;

    connectButton.addEventListener('click', onClickButton);

    sessionElement.appendChild(hostElement);
    sessionElement.appendChild(connectButton);

    return sessionElement;
}


const resolveGameChannelMessage = (message) => {
    


}


const renderOpenGameSessions = (openSessions) => {
    const openSessionsList = document.querySelector('.open-sessions-list')

    openSessions.forEach(session => {
        let component = GameSessionComponent({
            host: session.host, 
            bottonMessage: 'Connect',
            onClickButton: () => ConnectSession(session.id)
        })

        openSessionsList.appendChild(component)
    })
}


const fetchOpenSessions = () => {
    const myHeaders = new Headers();
    
    const userSession = localStorage.getItem("userSession");
    myHeaders.append("Authorization", userSession)

    const requestOptions = {
        method: "GET",
        headers: myHeaders,
        redirect: "follow"
    };

    return fetch("/api/v1/games", requestOptions)
    .then((response) => {
        if (!response.ok) {
            throw new Error("Invalid User");
        }
        return response.json()
    })
    .then((result) => {
        renderOpenGameSessions(result.game_sessions)
    })
    .catch((error) => console.error(error));
}


const startGameChannel = (gameSessionId) => {
    const userSession = localStorage.getItem("userSession");
    const is_user_host = localStorage.getItem("is_host")

    gameSessionId = gameSessionId || localStorage.getItem("gameSessionId");

    const url = `ws://${window.location.host}/ws/game/${gameSessionId}/?user_session=${userSession}`;
    const channel = new WebSocket(url);

    channel.onmessage = (e) => {
        debugger
        let data = JSON.parse(e.data)

        let message = data.message

        if(message.game_session_status === "RUNNING") {
            runningMessage(channel, message)
        } else if (message.game_session_status == "OVER") {
            overMessage(channel, message)
        }
    }

    channel.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    return channel;
}


const RenderPlayerRequestComponent = (player, onClick) => {
    let requestElement = document.querySelector('.game-requests-list')

    let component = GameSessionComponent({
        host: player, 
        bottonMessage: 'Accept',
        onClickButton: onClick
    })
    requestElement.appendChild(component)

}

const cleanPlayerRequestsComponents = () => {
    let requestElement = document.querySelector('.game-requests-list')
    requestElement.innerHTML = ''
}


const changeGameHead = (head) => {
    let gameHead = document.querySelector(".game-head")
    gameHead.innerHTML = head
}

const waitingForHostApprovalMessage = (channel, message) => {
    RenderPlayerRequestComponent(message.player, () => {

        let admit_message = JSON.stringify({
            action: "admit_player", 
            player_name: message.player
        })

        channel.send(admit_message)
    })
}


const updateGameBoard = (channel, board) => {
    let boardElement = document.querySelector('.tic-tac-toe-container');
    boardElement.style.display = 'grid'

    board.map((y_axis, x_index) => {
        y_axis.map((item, y_index) => {
            let boardItemCardElement = document.querySelector(`.x-${x_index}.y-${y_index}`)
            if(item) {
                boardItemCardElement.innerHTML = item
            }
        }) 
    })

}

const changePlayerTurn = (player) => {
    let playerTurnComponent = document.querySelector('.player-turn')
    playerTurnComponent.innerHTML = `turn: ${player}`
}

const runningMessage = (channel, message) => {
    cleanPlayerRequestsComponents()
    changeGameHead("Let's Go !!")
    changePlayerTurn(message.next_turn)
    updateGameBoard(channel, message.board)
}

const overMessage = (channel, message) => {
    changeGameHead(`Game Over, ${message.change_status_reason}`)
    changePlayerTurn(message.player)
    updateGameBoard(channel, message.board)
    channel.close()
}


const addChannelToGame = (channel) => {
    const positions = [
        [0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]
    ]

    const is_host = localStorage.getItem("is_host")

    const item = is_host === "true"?"X":"O"

    positions.forEach(position => {
        const [x, y] = position
        let element = document.querySelector(`.x-${x}.y-${y}`)

        element.addEventListener('click', () => {
            channel.send(JSON.stringify({action: "mark", item: item, position: position}))
        });
    })
}

const initChannelForPlayer = () => {
    debugger
    let channel = startGameChannel()
    addChannelToGame(channel)
     channel.addEventListener("open", () => {
        channel.send(JSON.stringify({action: "resume"}))
    })
}


const findPlayers = (gameSessionId, onAdmitRedirectTo) => {

    channel = startGameChannel(gameSessionId)

    channel.onmessage = (e) => {
        let data = JSON.parse(e.data)

        let message = data.message

        if(message.game_session_status === "WAITING_FOR_HOST_APPROVAL") {
            waitingForHostApprovalMessage(channel, message)
        } else if(message.game_session_status === "RUNNING") {
            localStorage.setItem("is_host", true)
            localStorage.setItem("gameSessionId", gameSessionId)
            location.href = onAdmitRedirectTo
        }
    }

}

const waitForHostApproval = (gameSessionId, on_admit_redirect_to, on_reject_redirect_to) => {
    channel = startGameChannel(gameSessionId)

    channel.onmessage = (e) => {
        let data = JSON.parse(e.data)

        let message = data.message

        if(message.game_session_status === "RUNNING"){

            localStorage.setItem("is_host", false)
            localStorage.setItem("gameSessionId", gameSessionId)
            location.href = on_admit_redirect_to
        }else if(message.game_session_status === "WAITING_FOR_PLAYER") {
            location.href = on_reject_redirect_to
        }
    }


    channel.addEventListener('open', function (event) {
        const message = JSON.stringify({ action: "connect" })
        channel.send(message)
    })
}

const ConnectSession = (sessionId) => {

    channel = startGameChannel(sessionId)
    channel.onmessage = (e) => {
        let data = JSON.parse(e.data)

        let message = data.message

        if(message.game_session_status === "RUNNING"){

            localStorage.setItem("is_host", false)
            localStorage.setItem("gameSessionId", sessionId)
            location.href = "/web/game"
        }
    }


    channel.addEventListener('open', function (event) {
        const message = JSON.stringify({ action: "connect" })
        channel.send(message)
    })

}
// var gameSocket = startGameChannel();