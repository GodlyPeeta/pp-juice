import re

def true(b):
    if not b: raise AssertionError("condition was false")

def equals(a, b):
    if a != b: raise AssertionError(f"{a} and {b} were not equal")

def not_equals(a, b):
    if a == b: raise AssertionError(f"recieved equal values of {a}")

def type_equals(a, t):
    if type(a) is t: return
    raise AssertionError(f"{a} was not type {t}, instead was type {type(a)}")

def embed_contains(embed, st):
    if embed.title and embed.title.count(st): return
    if embed.author and str(embed.author).count(st): return
    if embed.description and embed.description.count(st): return
    if embed.footer and embed.footer.text.count(st): return
    for field in embed.fields:
        if field.name.count(st): return
        if field.value.count(st): return
    raise AssertionError(f"embed did not contain '{st}'")

def embed_match(embed, regex):
    p = re.compile(regex, 0)
    if p.search(embed.title): return
    if p.search(str(embed.author)): return
    if p.search(embed.description): return
    if p.search(embed.footer.text): return
    for field in embed.fields:
        if p.search(field.name): return
        if p.search(field.value): return
    raise AssertionError(f"embed did not match /{regex}/g")