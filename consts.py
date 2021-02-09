
QWERTY_LAYOUT = [

["tab", *list("qwertyuiop"), "lbrace", "rbrace", "or"],
["caps", *list("asdfghjkl"), "colon", "quote", "enter"],
["lshift", *list("zxcvbnm"),  "less", "great", "exl", "rshift"],
["ctrl", "fn", "alt", "windows", "space", "alt_2", "context", "blank_2", "ctrl_big"]
]

ALPHA_LAYOUT = [

["tab", *list("abcdefghij"), "lbrace", "rbrace", "or"],
["caps", *list("klmnopqrs"), "colon", "quote", "enter"],
["lshift", *list("tuvwxyz"),  "less", "great", "exl", "rshift"],
["ctrl", "fn", "alt", "windows", "space", "alt_2", "context", "blank_2", "ctrl_big"]
]

DVORAK_LAYOUT = [

    ["tab", "less", "great", "exl", *list("pyfgcrl"), "lbrace", "rbrace", "or"],
    ["caps", *list("aoeuidhtns"), "quote", "enter"],
    ["lshift", "colon", *list("qjkxbmwvz"),  "rshift"],
    ["ctrl", "fn", "alt", "windows", "space", "alt_2", "context", "blank_2", "ctrl_big"]
]

QWERTY_LAYOUT_CHANGING = [

[*list("qwertyuiop"), "lbrace", "rbrace", "or"],
[*list("asdfghjkl"), "colon", "quote"],
[*list("zxcvbnm"),  "less", "great", "exl"],
]

DVORAK_LAYOUT_CHANGING = [

    [ "less", "great", "exl", *list("pyfgcrl"), "lbrace", "rbrace", "or"],
    [*list("aoeuidhtns"), "quote"],
    ["colon", *list("qjkxbmwvz")],
]

QWERTY_DISTANCES=[
70.4,
408.3,
3520.1,
4556.5,
0.0,
0.0,
4070.9,
1378.1,
1402.9,
561.9,
15969.2,
]

DVORAK_DISTANCES=[
68.2,
30.2,
33.4,
2547.2,
0.0,
0.0,
2862.6,
1151.6,
1791.9,
1021.9,
9506.9,
]

QWERTY_FINGERS = [
    399,
    444,
    1142,
    1169,
    958,
    0,
    967,
    391,
    652,
    150,
]

DVORAK_FINGERS = [
    400,
    380,
    723,
    804,
    958,
    0,
    866,
    702,
    816,
    623,
]

QWERTY_ROW_USAGE = [44, 27, 14, 15]
DVORAK_ROW_USAGE = [21, 56, 8, 15]
