import bitwiseEnum

mods = {
    0:  "nm",
    1: "nf",
    2: "ez",
    4: "td",
    8: "hd",
    16: "hr",
    32: "sd",
    64: "dt",
    128: "rx",
    256: "ht",
    512: "nc",
    1024: "fl"
}
print(bitwiseEnum.findCombo(mods, 1032, []))

print(bitwiseEnum.findCombo(mods, 1602, []))