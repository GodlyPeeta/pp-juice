import discord

TEST_LIST = []

def test(group):
    def _(fn):
        TEST_LIST.append((fn, group))
        return fn
    return _

class FakeAuthor:
    def __init__(self):
        self.id = 727
        self.name = "Unit Tester"

class FakeCtx:
    def __init__(self):
        self.sent = None
        self.author = FakeAuthor()

    async def send(self, embed):
        self.sent = embed