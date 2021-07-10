import os
import socket
import sys

import aiohttp

_root = os.path.dirname(os.path.realpath(__file__))[:-4]
sys.path.append(_root)
from src.bot import ScoreBot


def main():
    # read the stashed scores.
    print("reading scores", end="... ")
    with open(".scores.csv", 'r') as file:
        lines = file.readlines()
    # score have following format: '<score>;<date>;<username>'.
    data = list(map(lambda s: tuple(s.strip().split(';')), lines))

    # do NOT continue if not a single game has been completed.
    if len(data) == 0:
        print("no score to send.")
        return

    # read the token to connect the bot.
    print("reading token", end="... ")
    with open(".token.txt", 'r') as token_file:
        token = token_file.readline()

    # run the bot.
    print("creating bot", end="... ")
    bot = ScoreBot(game="NeoSnake", payload=data)
    print("sending results...")
    bot.run(token)


if __name__ == '__main__':
    try:
        main()
    except socket.gaierror as sg:
        print(sg)
        print("sending results failed. try again later with:")
        print(f"python {_root}/src/score.py")
    except aiohttp.client_exceptions.ClientConnectorError as acc:
        print(acc)
        print("sending results failed. try again later with:")
        print(f"python {_root}/src/score.py")
