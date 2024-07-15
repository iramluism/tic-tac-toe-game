# API Endpoints

## Index 
1. [Error Codes](#error-codes)
2. [Create Player](#post-apiv1player)
3. [Authenticate Player](#post-apiv1playerauth)
4. [Start a Game](#post-apiv1gamesstart)
5.  [List open session of other players](#get-apiv1games)
6. [Game Session Channel](#websocket-wsgamegame_session_id)
7.  [List History Game](#get-apiv1gameshistory)


## Error Codes
| Message| Code | Description |
|-------|-------|-------|
| PLAYER_ALREADY_EXISTS | 100409 | Create a player that already exists |
| PLAYER_UNAUTHORIZED | 100401 | Player not authorized |
| INVALID_USER_SESSION | 100403 | Invalid user session  |
| INVALID_GAME_SESSION | 101403 | Invalid Game Session |
| INVALID_ACTION | 100400 | Invalid Action |
| ACTION_NOT_ALLOWED| 102403 | Action not allowed |
| POSITION_ALREADY_MARKED| 104409 | Position already marked on the board |
| PLAYER_ALREADY_CONNECTED| 101409 | Player already connected to the game |
| POSITION_OUT_OF_BOARD| 101400 | position out of the board |
| INVALID_ITEM| 102400 | Invalid Item to mark on the board |



## `POST` /api/v1/player
**Description**:  Create a player

**Body**: Json with the username and password of user
```json
{
    "name": "player1",
    "password": "1234"
}
```

**Response**: JSON array containing the user session
```json
{
    "user_session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoicGxheWVyMSIsImV4cCI6MTcyMTM3NTQzNn0.X2EyZ93fl2Q7rUUvvkMARo_cF0PP7p-FQAfH-r6cuUk"
}
```

# `POST` /api/v1/player/auth

**Description**: Authenticate Player

**Body**: Json with the username and password of user
```json
{
    "name": "player1",
    "password": "1234"
}
```

**Response**: JSON array containing the user session
```json
{
    "user_session": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoicGxheWVyMSIsImV4cCI6MTcyMTM3NTQzNn0.X2EyZ93fl2Q7rUUvvkMARo_cF0PP7p-FQAfH-r6cuUk"
}
```

# `POST` /api/v1/games/start
**Description**: Start a game session

**Body**: None

**Headers**: The user session of user
```http
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoicGxheWVyMSIsImV4cCI6MTcyMTM3NTQzNn0.X2EyZ93fl2Q7rUUvvkMARo_cF0PP7p-FQAfH-r6cuUk
```

**Response**: JSON array containing the game session
```json
{
    "game_session_id": "cb3dde74-c131-4d9e-a6b2-1b15bc07d251"
}
```

## `GET` /api/v1/games
**Description**:  List all open sessions of other players

**Body**: None

**Headers**: The user session of user
```http
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoicGxheWVyMSIsImV4cCI6MTcyMTM3NTQzNn0.X2EyZ93fl2Q7rUUvvkMARo_cF0PP7p-FQAfH-r6cuUk
```

**Response**: JSON array containing the user session
```json
{
    "game_sessions": [
        {
            "id": "bbb33ae7-2bce-4abf-bd80-3e1e613585a7",
            "host": "iram"
        }
    ]
}
```

# `Websocket` /ws/game/<game_session_id>/
**Description**: Connect to the game session channel. To authenticate the user you can send the user session on the Authorization Header or in the query string. 

**Body**: None

**Query**: The user session of user 
```url
user_session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoicGxheWVyMSIsImV4cCI6MTcyMTM3NTQzNn0.X2EyZ93fl2Q7rUUvvkMARo_cF0PP7p-FQAfH-r6cuUk
```

**Headers**: The user session of user
```http
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoicGxheWVyMSIsImV4cCI6MTcyMTM3NTQzNn0.X2EyZ93fl2Q7rUUvvkMARo_cF0PP7p-FQAfH-r6cuUk
```

**Messages**: 
Connect to an open session. 
```json
{"action": "connect"}
```
Request for an resume of the game. 
```json
{"action": "resume"}
```
Admit connection request of other players.
```json
{"action": "admit_player", "player_name": "edpuig"}
```
Mark the item, Cross/Nought. 
```json
{
    "action": "mark",
    "item": "X",
    "position": [0,1]
}

// positions
// | (0,0) | (0,1) | (0,2) |
// | (1,0) | (1,1) | (1,2) |
// | (2,0) | (2,1) | (2,2) |
```

**Responses**

All server responses have this format. 
Game Session status:
1. **WAITING_FOR_PLAYER**: Waiting for players to start the game 
2. **WAITING_FOR_HOST_APPROVAL**: A request was sent to the host and the app is waiting for the approval. 
3. **RUNNING**: The app is running
4. **CLOSED**: The all never started and the game close, every time a user want to start a new game session the app close the remaind open sessions. 
5. **OVER**: The game is over. 

```json
{
    "message": {
        "game_session_status": "RUNNING", // WAITING_FOR_PLAYER, WAITING_FOR_HOST_APPROVAL, RUNNING, CLOSED, OVER
        "change_status_reason": null,
        "board": [
            [
                "X",
                null,
                null
            ],
            [
                null,
                "O",
                null
            ],
            [
                null,
                "X",
                null
            ]
        ],
        "player": "iram", // the current player 
        "next_turn": "iram", // next player 
        "is_over": false // game session is over
    }
}
```
# PUT /api/v1/game/{game_id}/
Description: Update details of a specific game.
Parameters: game_id - ID of the game.
Request Body: JSON object with updated game details.
Response: JSON object with updated game details.
DELETE /api/v1/game/{game_id}/
Description: Delete a specific game.
Parameters: game_id - ID of the game.
Response: HTTP 204 No Content on successful deletion.
POST /api/v1/game/{game_id}/move/
Description: Make a move in the game board.
Parameters: game_id - ID of the game.
Request Body: JSON object with move details (player and position).
Response: JSON object with updated game details after the move.


## `GET` /api/v1/games/history
**Description**:  List all open sessions of other players

**Body**: None

**Headers**: The user session of user
```http
Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoicGxheWVyMSIsImV4cCI6MTcyMTM3NTQzNn0.X2EyZ93fl2Q7rUUvvkMARo_cF0PP7p-FQAfH-r6cuUk
```

**Response**: JSON array containing the user session
```json
{
    "game_sessions": [
        {
            "id": "88887dec-65f6-44c0-8eb3-90b47663eea7",
            "host": "iram",
            "winner": "iram",
            "players": [
                "iram",
                "july"
            ],
            "board": [
                [
                    "X",
                    "O",
                    null
                ],
                [
                    "O",
                    "X",
                    null
                ],
                [
                    null,
                    null,
                    "X"
                ]
            ]
        }
    ]
}
```