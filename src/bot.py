import discord


class ScoreBot(discord.Client):
    """ A Bot to send scores to the Discord server of SCSC."""

    def __init__(self, game, payload, flush=False):
        """
            Creates a bot that can that a score payload and send it to the Discord server of SCSC.

            Args
            ----
            game : str
                the name of the game and thus the score board.
            payload : [(int, str, str), ...]
                the payload to send to the server, namely [(score, date, username), ...].
            flush : bool, optional
                tells whether to flush the channel or not.
        """
        super(ScoreBot, self).__init__()
        # the game name and thus the score board name.
        self.game = game
        self.head = f"**{self.game}**:"

        # the payload and the flush flag.
        self.payload = payload
        self.flush = flush

        # the channel id the bot has access to.
        self.channel_id = 862644543207637042

    async def on_ready(self):
        """
            Runs when the bot connects to the server. Its only purpose is to read the channel, create or modify the game
            score board and send it to the channel.

            Args
            ----

            Returns
            -------
        """
        # some logging message.
        log_msg = f"Logged in as {self.user.name} ({self.user.id})"
        print(log_msg)
        print('-' * len(log_msg))

        # send the score board to the server.
        await self.send_score_board()

        # close the bot, its job is done.
        await self.close()

    async def build_score_board(self, payload, sep):
        # payload = list(zip(*payload))
        payload.sort()
        payload = payload[::-1]

        cols = (4, 5, 19, max(list(map(len, list(zip(*payload))[1]))))

        lines = [f"\t`{'rank':^{cols[0]}}{sep}{'score':^{cols[1]}}{sep}{'date':^{cols[2]}}{sep}{'name':^{cols[3]}}`"]
        lines += ["\t`" + "-+-".join(['-' * col for col in cols]) + '`']
        lines += [f"\t`{i + 1:>{cols[0]}d}{sep}{score:>{cols[1]}}{sep}{date:>{cols[2]}}{sep}{name:>{cols[3]}}`" for
                  i, (score, date, name) in enumerate(payload)]

        score_board = '\n'.join([self.head] + lines[:10])
        return score_board

    async def send_score_board(self):
        hist = await self.get_channel(self.channel_id).history(limit=None).flatten()

        for i, msg in enumerate(hist):
            print(f"{msg.content}")
            if self.flush:
                await msg.delete()

        if self.flush:
            hist = await self.get_channel(self.channel_id).history(limit=None).flatten()

        score_boards = [msg for msg in hist if msg.content.startswith(self.head)]

        sep = ' | '
        if len(hist) == 0 or len(score_boards) == 0:
            print(f"creating score board for {self.game}")
            payload = self.payload

        else:
            score_board = score_boards[0]
            for msg in score_boards:
                await msg.delete()

            print("appending to", self.game)
            previous_score_board = score_board.content.split('\n')
            lines = list(map(lambda x: x.replace('`', '').split(sep)[1:], previous_score_board[3:]))
            lines = list(map(lambda line: map(lambda el: el.replace('`', '').strip(), line), lines)) + self.payload

            scores, dates, names = tuple(zip(*lines))
            scores = list(map(int, scores))
            payload = list(zip(scores, dates, names))

        score_board = await self.build_score_board(payload=payload, sep=sep)
        await self.get_channel(self.channel_id).send(score_board)


if __name__ == '__main__':
    with open(".token.txt", 'r') as token_file:
        token = token_file.readline()
    data = [(8, "10/07/2021 15:18:15", "toto"), (92, "10/07/2021 15:17:51", "antoine.stevan"),
            (1, "10/07/2021 15:17:54", "antoine")]
    bot = ScoreBot(game="NeoSnake", payload=data, flush=True)
    print("sending results...")
    bot.run(token)
