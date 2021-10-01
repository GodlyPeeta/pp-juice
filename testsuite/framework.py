import discord

TEST_LIST = []

def test(fn):
    TEST_LIST.append(fn)
    return fn

class FakeCtx:
    def __init__(self):
        self.sent = None

    async def send(self, embed):
        self.sent = embed

def is_embed(embed):
    return type(embed) is discord.Embed