from manimlib.imports import *
import random

class Key(VMobject):
    CONFIG = {
        "key_text_args": {
            "color": WHITE,
            "font": "DDT W00 Regular",
        },
        "scale_key": 1.2,
    }

    def __init__(self, key, x=0, y=0, width=1, height=1,**kwargs):
        VMobject.__init__(self,  **kwargs)
        self.key = key
        self.boundaries = Rectangle(width=width, height=height).set_xy(x, y)
        self.key_text = Text(key, **self.key_text_args).scale(self.scale_key)
        self.key_text.move_to(self.boundaries)
        self.add(self.boundaries, self.key_text)
    def glow(self, color):
        touch = ApplyMethod(self.boundaries.set_fill, color, .8)
        lift = ApplyMethod(self.boundaries.set_fill, color, 0)
        return (touch, lift)
    def set_color(self, color):
        animation = ApplyMethod(self.boundaries.set_fill, color, .8)
        return animation


class Test(Scene):
    def construct(self):
        self.keys = VGroup()
        self.keys_dict = {}
        self.first = True
        self.add_keys(list("QWERTYUIOP"), start_x=-6.5, start_y=1)
        self.add_keys(list("ASDFGHJKL"), start_x=-6.5, start_y=-.2)
        self.add_keys(list("ZXCVBNM"), start_x=-4.5, start_y=-1.4)
        self.add_keys(list(" "), start_x=-0.5, start_y=-2.6, width=5, height=1)
        # self.write_sequence("minouche is gay")
        self.explode()
        self.move_keys(list("AZERTYUIOP"), start_x=-6.5, start_y=1)
        self.move_keys(list("QDSFGHJKLM"), start_x=-6.5, start_y=-.2)
        self.move_keys(list("WXCVBN"), start_x=-4.5, start_y=-1.4)
        self.move_keys(list(" "), start_x=-0.5, start_y=-2.6)

    
    def add_keys(self, keys, start_x=-6.5, start_y=1, width=1, height=1):
        limit=.2
        j = 0
        animations = VGroup()
        x = start_x
        for i in keys:
            a = Key(i, x = x + j * limit, y=start_y, width=width, height=height)
            animations.add(ShowCreation(a))
            self.keys.add(a)
            self.keys_dict[i] = a
            x += 1
            j += 1
        if self.first:
            self.play(LaggedStart(*animations))
            self.first = False
        else:
            self.play(*animations)

    def move_keys(self, keys, start_x, start_y):
        limit=.2
        j = 0
        animations = VGroup()
        x = start_x
        for i in keys:
            k = self.keys_dict[i]
            position = np.array([x + j * limit, start_y, 0])
            animations.add(ApplyMethod(k.move_to, position))
            x += 1
            j += 1
        self.play(*animations)
 
    def write_sequence(self, sequence):
        seq = sequence.upper()
        t = Text("", font="DDT W00 Regular").set_xy(-4, 2).scale(.3)
        for i in seq:
            key = self.keys_dict[i]
            a = key.glow(RED)
            if i == " ":
                s = Text("_", font="DDT W00 Regular").set_fill(opacity=0)
                s.set_stroke(width=0)
            else:
                s = Text(str(i), font="DDT W00 Regular")
            s.next_to(t, RIGHT, buff=.2)
            b = Write(s)
            self.play(a[0], b, run_time=.3)
            self.play(a[1], run_time=.1)
            t = s

    def color_word(self, word):
        animations = VGroup()
        for i in word.upper():
            key = self.keys_dict[i]
            animations.add(key.set_color(GREEN))
        self.play(LaggedStart(*animations, lag_ratio=.3))

    def explode(self):
        animations = VGroup()
        directions = [UP, DOWN, RIGHT, LEFT]
        self.keys.save_state()
        for i in self.keys:
            x = np.random.randint(1, 5)
            y = np.random.randint(1, 3)
            r = np.random.rand()
            v = x * random.choice(directions) + y * random.choice(directions)
            animations.add(ApplyMethod(i.rotate, r))
            animations.add(ApplyMethod(i.shift, v))
        self.play(*animations)

