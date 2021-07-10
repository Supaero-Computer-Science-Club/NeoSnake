import discord


class ScoreBot(discord.Client):
    """ A Bot to send scores to the Discord server of SCSC."""

    def __init__(self, game, payload, needs_flush=False):
        """
            Creates a bot that can that a score payload and send it to the Discord server of SCSC.

            Args
            ----
            game : str
                the name of the game and thus the scoreboard.
            payload : [(int, str, str), ...]
                the payload to send to the server, namely [(score, date, username), ...].
            needs_flush : bool, optional
                tells whether to flush the channel or not.
        """
        super(ScoreBot, self).__init__()
        # the game name and thus the scoreboard name.
        self.game = game
        self.head = f"**{self.game}**:"

        # the payload and the flush flag.
        self.payload = payload
        self.needs_flush = needs_flush

        # the channel id the bot has access to.
        self.channel_id = 862644543207637042

        # internal variables.
        self.sep = " | "
        self.lines = 10
        self.cols = (4, 5, 19)

    async def on_ready(self):
        """
            Runs when the bot connects to the server. Its only purpose is to read the channel, create or modify the game
            scoreboard and send it to the channel.

            Args
            ----

            Returns
            -------
        """
        # some logging message.
        log_msg = f"Logged in as {self.user.name} ({self.user.id})"
        print(log_msg)
        print('-' * len(log_msg))

        # send the scoreboard to the server.
        await self.send_scoreboard()

        # close the bot, its job is done.
        await self.close()

    async def _flush(self):
        """
            Flushes all the history of the channel.
            Args
            ----

            Returns
            -------
            history : list
                the list of all previous message still present in the channel after the flush.
        """
        # retrieve history and flush it if needed.
        history = await self.get_channel(self.channel_id).history(limit=None).flatten()
        print("previous channel history.")
        for i, msg in enumerate(history):
            print(f"{msg.content}")
            if self.needs_flush:
                await msg.delete()

        # update the history if a flush happened.
        if self.needs_flush:
            history = await self.get_channel(self.channel_id).history(limit=None).flatten()

        return history

    def _extract_payload(self, scoreboard):
        """ 
            Extracts all the scores from an existing scoreboard and adds the current payload.
            
            Args
            ----
            scoreboard : str
                the scoreboard. It is simply a multi-lines string where each row, except the head of the scoreboard,
                contains information about the score performed.

            Returns
            -------
            payload : [(int, str, str), ...]
                the list of all the previous recorded scores, namely [(score, date, username), ...].
        """
        previous_scoreboard = scoreboard.split('\n')  # split the lines.

        # skip the first 3 lines + remove the '`', split with the separator and remove the first column.
        lines = list(map(lambda x: x.replace('`', '').split(self.sep)[1:], previous_scoreboard[3:]))
        # strip everything in the sub lists and append the current payload.
        lines = list(map(lambda line: map(lambda el: el.strip(), line), lines)) + self.payload

        scores, dates, names = tuple(zip(*lines))  # extract the information.
        scores = list(map(float, scores))  # convert the scores to numbers.
        payload = list(zip(scores, dates, names))  # recombine the information.

        return payload

    async def _build_scoreboard(self, payload):
        """ 
            Builds a valid scoreboard from a payload.

            Args
            ----
            payload : [(int, str, str), ...]
                the list of all the previous recorded scores, namely [(score, date, username), ...].

            Returns
            -------
            scoreboard : str
                the scoreboard. It is simply a multi-lines string where each row, except the head of the scoreboard,
                contains information about the score performed.
        """
        # sort the payload from biggest to smallest score, i.e. with the score which is ine first place.
        print(payload)
        payload.sort()
        payload = payload[::-1]

        # the width of the columns, the last one adapts to the usernames, which are unknown a priori.
        cols = self.cols + (max(list(map(len, list(zip(*payload))[1]))),)

        # the first line with the names of the columns.
        lines = [self.sep.join([f"\t`{'rank':^{cols[0]}}", f"{'score':^{cols[1]}}",
                                f"{'date':^{cols[2]}}", f"{'name':^{cols[3]}}`"])]
        lines += ["\t`" + "-+-".join(['-' * col for col in cols]) + '`']  # a separation line.
        # the rest of the lines, with the scores and more info.
        lines += [self.sep.join([f"\t`{i + 1:>{cols[0]}d}", f"{score:>{cols[1]}}", f"{date:>{cols[2]}}",
                                 f"{name:>{cols[3]}}`"]) for i, (score, date, name) in enumerate(payload)]

        scoreboard = '\n'.join([self.head] + lines[:self.lines + 2])  # simply join the head and enough lines with '\n'.
        return scoreboard

    async def send_scoreboard(self):
        """
            The main method of the bot. Reads the history of the channels, extracts scores from previous valid
            scoreboards, creates or modifies the scoreboard with new scores and send it back to the server.

            Args
            ----

            Returns
            -------
        """
        # read the history.
        history = await self._flush()

        # isolate scoreboards of the game.
        scoreboards = [msg for msg in history if msg.content.startswith(self.head)]

        # use the whole current payload to create a scoreboard from scratch.
        if len(history) == 0 or len(scoreboards) == 0:
            print(f"creating scoreboard for {self.game}")
            payload = self.payload

        # simply extracts the previous scores and add the current ones. also deletes all invalid scoreboards.
        else:
            payload = self._extract_payload(scoreboards[0].content)
            for msg in scoreboards:
                await msg.delete()

            print("appending to", self.game)

        # build and send the scoreboard.
        scoreboard = await self._build_scoreboard(payload=payload)
        await self.get_channel(self.channel_id).send(scoreboard)


if __name__ == '__main__':
    with open(".token.txt", 'r') as token_file:
        token = token_file.readline()
    data = [(8, "10/07/2021 15:18:15", "toto"), (92, "10/07/2021 15:17:51", "antoine.stevan"),
            (1, "10/07/2021 15:17:54", "antoine")]
    bot = ScoreBot(game="NeoSnake", payload=data, needs_flush=True)
    print("sending results...")
    bot.run(token)
