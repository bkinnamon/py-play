#!/usr/bin/env python

import asyncio
import json
import logging
import websockets
from tictactoe import TicTacToe

logging.basicConfig()

USERS = set()
GAME = TicTacToe()


async def register(websocket):
    """Registers a player."""
    USERS.add(websocket)
    if enough_players():
        await new_game()


async def unregister(websocket):
    """Resets the game if a player leaves."""
    USERS.remove(websocket)
    GAME.new_game()
    await update_players()


async def update_players():
    """Sends updates to the players."""
    if USERS:
        message = json.dumps({"type": "update", **GAME.get_state()})
        await asyncio.wait([user.send(message) for user in USERS])


def enough_players():
    """Checks to see if enough players are connected."""
    return True


async def new_game():
    """Creates a new game."""
    if enough_players():
        GAME.new_game()
        await update_players()


async def make_move(index):
    """Makes a move for the current player."""
    if enough_players():
        GAME.make_move(index)
        await update_players()


async def play_ttt(websocket, path):
    """Allows a socket to play tic-tac-toe."""
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "make_move":
                await make_move(data["index"])
            else:
                logging.error("Unexpected event: %s", data["action"])
    finally:
        await unregister(websocket)


start_server = websockets.serve(play_ttt, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
