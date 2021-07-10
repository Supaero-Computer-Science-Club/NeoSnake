import asyncio
import time

import discord
import numpy as np


class ScoreBot(discord.Client):
    def __init__(self, score_board, flush=False):
        super(ScoreBot, self).__init__()
        self.score_board = score_board
        self.score = None
        self.flush = flush

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        print(self.is_ready())

        await self.treat_score()

        await self.close()

    async def treat_score(self):
        channel = self.get_channel(862644543207637042)
        hist = await channel.history(limit=None).flatten()

        for i, msg in enumerate(hist):
            print(f"{msg.content}")
            if self.flush:
                await msg.delete()

        if self.flush:
            hist = await channel.history(limit=None).flatten()

        print(len(hist))
        if len(hist) == 0:
            print("creating", self.score_board)
            score_board = f"**{self.score_board}**:\n" \
                          f"\t1. {self.score}"
            await channel.send(score_board)

        else:
            for msg in hist:
                if msg.content.startswith(f"**{self.score_board}**"):
                    print("appending to", self.score_board)
                    score_board = msg.content.split('\n')
                    await msg.delete()
                    score_board += [f"\t{len(score_board)}. {self.score}"]
                    score_board, scores = score_board[0], score_board[1:]
                    scores = [int(score.strip().split(". ")[1]) for score in scores]
                    print(scores)
                    scores.sort()
                    scores = scores[::-1]
                    print(scores)
                    scores = ['\t' + ". ".join([str(rank + 1), str(score)]) for rank, score in
                              zip(range(len(scores)), scores)]
                    score_board = [score_board] + scores[:10]

                    await channel.send('\n'.join(score_board))

    def set_score(self, score):
        self.score = score


if __name__ == '__main__':
    bot = ScoreBot("NeoSnake", flush=False)
    with open(".token.txt", 'r') as token_file:
        token = token_file.readline()
    for score in np.random.randint(low=1, high=100, size=(20,)):
        print(f"{score = }")
        bot.set_score(score)
        # bot.run(token)
        # loop = asyncio.get_event_loop()
        # asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot.start(token))
        loop.close()
        time.sleep(1)
        # asyncio.set_event_loop(asyncio.new_event_loop())
    bot.close()
