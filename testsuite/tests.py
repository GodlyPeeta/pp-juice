from testsuite import asserts, framework
import cogs

# Section: pp.pp tests

@framework.test
async def tcmd_pp_plain():
    fakectx = framework.FakeCtx()
    await cogs.OSU.pp(None, fakectx, "https://osu.ppy.sh/b/1762727")
    embed = fakectx.sent
    asserts.true(framework.is_embed(embed))
    asserts.embed_match(embed, r"BPM:[^0-9]+170")
    asserts.embed_match(embed, r"Map Length:[^0-9]+00:30")
    asserts.embed_match(embed, r"Combo:[^0-9]+152")
    asserts.embed_match(embed, r"CS:[^0-9]+3\.7")
    asserts.embed_match(embed, r"OD:[^0-9]+8")
    asserts.embed_match(embed, r"AR:[^0-9]+8\.2")
    asserts.embed_match(embed, r"HP:[^0-9]+4\.4")
    asserts.embed_contains(embed, "100.0%")

@framework.test
async def tcmd_pp_with_mods():
    fakectx = framework.FakeCtx()
    await cogs.OSU.pp(None, fakectx, "https://osu.ppy.sh/b/1762727", "+dthrnf", "69%", "1m", "130x")
    embed = fakectx.sent
    asserts.true(framework.is_embed(embed))
    asserts.embed_match(embed, r"BPM:[^0-9]+255")
    asserts.embed_match(embed, r"Map Length:[^0-9]+00:20")
    asserts.embed_match(embed, r"Combo:[^0-9]+130")
    asserts.embed_match(embed, r"CS:[^0-9]+4\.81")
    asserts.embed_match(embed, r"OD:[^0-9]+11\.1")
    asserts.embed_match(embed, r"AR:[^0-9]+11\.0")
    asserts.embed_match(embed, r"HP:[^0-9]+6\.16")
    asserts.embed_contains(embed, "69.0%")

@framework.test
async def tcmd_pp_invalid_link():
    fakectx = framework.FakeCtx()
    await cogs.OSU.pp(None, fakectx, "https://osu.ppy.sh/b/invalid link :trol:", "+dthrnftd", "69%", "1m", "130x")
    msg = fakectx.sent
    asserts.type_equals(msg, str)

@framework.test
async def tcmd_pp_invalid_mods():
    fakectx = framework.FakeCtx()
    await cogs.OSU.pp(None, fakectx, "https://osu.ppy.sh/b/1762727", "+dthusian", "69%", "1m", "130x")
    msg = fakectx.sent
    asserts.type_equals(msg, str)

# Section: Beatmap Link Embed Tests

@framework.test
async def t_maplink_embed_normal():
    embed = cogs.OSU.beatmaplinkembed("https://osu.ppy.sh/beatmapsets/842412#osu/1762727")
    asserts.true(framework.is_embed(embed))
    asserts.embed_match(embed, r"BPM:[^0-9]+170")
    asserts.embed_match(embed, r"Map Length:[^0-9]+00:30")
    asserts.embed_match(embed, r"Combo:[^0-9]+152")
    asserts.embed_match(embed, r"CS:[^0-9]+3\.7")
    asserts.embed_match(embed, r"OD:[^0-9]+8")
    asserts.embed_match(embed, r"AR:[^0-9]+8\.2")
    asserts.embed_match(embed, r"HP:[^0-9]+4\.4")

@framework.test
async def t_maplink_embed_invalid_link():
    embed = cogs.OSU.beatmaplinkembed("https://osu.ppy.sh/beatmapsets/invalid link :trol:")
    asserts.true(embed == None)

@framework.test
async def t_maplink_embed_infer_diff():
    embed = cogs.OSU.beatmaplinkembed("https://osu.ppy.sh/beatmapsets/842412")
    asserts.true(framework.is_embed(embed))
    asserts.embed_match(embed, r"BPM:[^0-9]+170")
    asserts.embed_match(embed, r"Map Length:[^0-9]+00:30")
    asserts.embed_match(embed, r"Combo:[^0-9]+151")
    asserts.embed_match(embed, r"CS:[^0-9]+3.8")
    asserts.embed_match(embed, r"OD:[^0-9]+9")
    asserts.embed_match(embed, r"AR:[^0-9]+9")
    asserts.embed_match(embed, r"HP:[^0-9]+5\.2")