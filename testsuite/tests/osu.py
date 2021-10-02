from discord.embeds import Embed
from testsuite import asserts, framework
import cogs

# Section: Beatmap Link Embed Tests

@framework.test(group="osu")
async def maplink_embed_normal():
    embed = cogs.OSU.beatmaplinkembed("https://osu.ppy.sh/beatmapsets/842412#osu/1762727")
    asserts.type_equals(embed, Embed)
    asserts.embed_match(embed, r"BPM:[^0-9]+170")
    asserts.embed_match(embed, r"Map Length:[^0-9]+00:30")
    asserts.embed_match(embed, r"Combo:[^0-9]+152")
    asserts.embed_match(embed, r"CS:[^0-9]+3\.7")
    asserts.embed_match(embed, r"OD:[^0-9]+8")
    asserts.embed_match(embed, r"AR:[^0-9]+8\.2")
    asserts.embed_match(embed, r"HP:[^0-9]+4\.4")

@framework.test(group="osu")
async def maplink_embed_invalid_link():
    embed = cogs.OSU.beatmaplinkembed("https://osu.ppy.sh/beatmapsets/invalid link :trol:")
    asserts.true(embed == None)

@framework.test(group="osu")
async def maplink_embed_infer_diff():
    embed = cogs.OSU.beatmaplinkembed("https://osu.ppy.sh/beatmapsets/842412")
    asserts.type_equals(embed, Embed)
    asserts.embed_match(embed, r"BPM:[^0-9]+170")
    asserts.embed_match(embed, r"Map Length:[^0-9]+00:30")
    asserts.embed_match(embed, r"Combo:[^0-9]+151")
    asserts.embed_match(embed, r"CS:[^0-9]+3.8")
    asserts.embed_match(embed, r"OD:[^0-9]+9")
    asserts.embed_match(embed, r"AR:[^0-9]+9")
    asserts.embed_match(embed, r"HP:[^0-9]+5\.2")

# Section: Map Feed Embed Tests

@framework.test(group="osu")
async def mapfeed_embed_test():
    embed = cogs.OSU.mapfeedembed("https://osu.ppy.sh/beatmapsets/1357624", "ranked")
    asserts.type_equals(embed, Embed)
    asserts.embed_contains(embed, "Ranked")
    asserts.embed_contains(embed, "sabi")
    asserts.embed_contains(embed, "true DJ MAG top ranker's song Zenpen (katagiri Remix)")
    asserts.embed_contains(embed, "Nathan")

# Section: pp.osuset Tests

@framework.test(group="osu")
async def cmd_osuset_normal():
    fakectx = framework.FakeCtx()
    await cogs.OSU.osuset(None, fakectx, "mrekk")
    asserts.type_equals(fakectx.sent, str)
    await cogs.OSU.osuset(None, fakectx)
    asserts.type_equals(fakectx.sent, str)

async def cmd_osuset_nonexistent_user():
    fakectx = framework.FakeCtx()
    await cogs.OSU.osuset(None, fakectx, "@invalid") # User guaranteed to not exist because invalid char
    asserts.type_equals(fakectx.sent, str)

# Section: pp.osu Tests 

@framework.test(group="osu")
async def cmd_osu_normal():
    fakectx = framework.FakeCtx()
    await cogs.OSU.osu(None, fakectx, "pongger")
    embed = fakectx.sent
    asserts.type_equals(embed, Embed)
    asserts.embed_contains(embed, "pongger")
    asserts.embed_match(embed, r"Ranked Score:[^0-9]+115,257,297")
    asserts.embed_match(embed, r"Hit Accuracy:[^0-9]+88.75%")
    asserts.embed_match(embed, r"Play Count:[^0-9]+1,129")

@framework.test(group="osu")
async def cmd_osu_nonexistent_user():
    fakectx = framework.FakeCtx()
    await cogs.OSU.osu(None, fakectx, "@invalid")
    embed = fakectx.sent
    asserts.type_equals(embed, str)

# Section: pp.pp Tests

@framework.test(group="osu")
async def cmd_pp_plain():
    fakectx = framework.FakeCtx()
    await cogs.OSU.pp(None, fakectx, "https://osu.ppy.sh/b/1762727")
    embed = fakectx.sent
    asserts.type_equals(embed, Embed)
    asserts.embed_match(embed, r"BPM:[^0-9]+170")
    asserts.embed_match(embed, r"Map Length:[^0-9]+00:30")
    asserts.embed_match(embed, r"Combo:[^0-9]+152")
    asserts.embed_match(embed, r"CS:[^0-9]+3\.7")
    asserts.embed_match(embed, r"OD:[^0-9]+8")
    asserts.embed_match(embed, r"AR:[^0-9]+8\.2")
    asserts.embed_match(embed, r"HP:[^0-9]+4\.4")
    asserts.embed_contains(embed, "100.0%")

@framework.test(group="osu")
async def cmd_pp_with_opts():
    fakectx = framework.FakeCtx()
    await cogs.OSU.pp(None, fakectx, "https://osu.ppy.sh/b/1762727", "+dthrnf", "69%", "1m", "130x")
    embed = fakectx.sent
    asserts.type_equals(embed, Embed)
    asserts.embed_match(embed, r"BPM:[^0-9]+255")
    asserts.embed_match(embed, r"Map Length:[^0-9]+00:20")
    asserts.embed_match(embed, r"Combo:[^0-9]+130")
    asserts.embed_match(embed, r"CS:[^0-9]+4\.81")
    asserts.embed_match(embed, r"OD:[^0-9]+11\.1")
    asserts.embed_match(embed, r"AR:[^0-9]+11\.0")
    asserts.embed_match(embed, r"HP:[^0-9]+6\.16")
    asserts.embed_contains(embed, "69.0%")

@framework.test(group="osu")
async def cmd_pp_invalid_link():
    fakectx = framework.FakeCtx()
    await cogs.OSU.pp(None, fakectx, "https://osu.ppy.sh/b/invalid link :trol:", "+dthrnftd", "69%", "1m", "130x")
    msg = fakectx.sent
    asserts.type_equals(msg, str)

@framework.test(group="osu")
async def cmd_pp_invalid_mods():
    fakectx = framework.FakeCtx()
    await cogs.OSU.pp(None, fakectx, "https://osu.ppy.sh/b/1762727", "+dthusian", "69%", "1m", "130x")
    msg = fakectx.sent
    asserts.type_equals(msg, str)

#TODO pp.top unit tests

# Note: osutrack related commands are too rare to justify testing

#TODO pp.strains unit tests

#TODO pp.netpp unit tests

# Note: mapfeed, beatmaplink commands are too rare to justify testing

#TODO pp.scores unit tests

#TODO pp.lb unit tests

#TODO pp.rs unit tests

#TODO pp.mr unit tests
