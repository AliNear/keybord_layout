from manimlib.imports import *
import random
import os

ASSESTS_PATH = os.getcwd() + "/projects/keyboard_layout/assets/"
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
        self.boundaries = RoundedRectangle(corner_radius=.08, width=width, height=height).set_xy(x, y)
        self.boundaries.set_stroke(width=3)
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


class QwertyKB(Scene):
    def construct(self):
        self.keys = VGroup()
        self.keys_dict = {}
        self.first = True
        self.add_keys(list("QWERTYUIOP"), start_x=-6.5, start_y=1)
        self.add_keys(list("ASDFGHJKL"), start_x=-6.0, start_y=-.1)
        self.add_keys(list("ZXCVBNM"), start_x=-5.0, start_y=-1.2)
        self.add_keys(list(" "), start_x=-1.5, start_y=-2.3, width=5, height=1)
        self.write_sequence("ALI")
        self.play(self.keys.scale, .5)
        # self.explode()
        # self.move_keys(list("AZERTYUIOP"), start_x=-6.5, start_y=1)
        # self.move_keys(list("QDSFGHJKLM"), start_x=-6.5, start_y=-.2)
        # self.move_keys(list("WXCVBN"), start_x=-4.5, start_y=-1.4)
        # self.move_keys(list(" "), start_x=-0.5, start_y=-2.6)

    
    def add_keys(self, keys, start_x=-6.5, start_y=1, width=1, height=1):
        limit=.1
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

class TypeWriterArm(VMobject):
    CONFIG = {
        "head_kwargs": {
            "fill_opacity": 1,
            "fill_color": BLACK,
            "width": .1,
            "height": 0.4,
        },
        "body_kwargs": {
            "fill_opacity": 1,
            "fill_color": BLACK,
            "width": .03,
            "height": 1.5,
        }
    }
    def __init__(self, first, second, **kwargs):
        VMobject.__init__(self, **kwargs)
        # self.head = Rectangle(**self.head_kwargs).set_xy(x, y)
        self.head = Line(first.get_center(), second.get_center(), stroke_width=2)
        self.body = Line(first.get_center(), second.get_center(), stroke_width=5).scale(.3)
        self.body.shift(.4 * self.body.get_unit_vector())
        # self.body = Rectangle(**self.body_kwargs)
        # self.head.next_to(self.body, UP, buff=0)
        self.point = self.head.points[0]
        self.add(self.head, self.body)


class Test(ThreeDScene):
    def construct(self):
        
        self.move_camera(phi=0, theta=-90 * DEGREES, distance=20)
        t = -3 * PI / 4
        center_x = 0
        center_y = 2
        r = 2
        
        arms = VGroup()
        for i in range(21):
            x = center_x + r * np.cos(t)
            x_2 = center_x + r * 2 * np.cos(t)
            y = center_y + r * np.sin(t)
            y_2 = center_y + r * 2 * np.sin(t)
            d = Dot(np.array([x, y, 0])).scale(.3)
            f = Dot(np.array([x_2, y_2, 0]))
            self.play(FadeIn(d))
            arm = TypeWriterArm(d, f)
            arms.add(arm)
            t += PI/40
        
        self.play(ShowCreation(arms))
        for arm in arms:
            arm.save_state()
            self.play(arm.rotate, 180 * DEGREES, Z_AXIS, {"about_point":arm.point}, run_time=.5)
            self.play(Restore(arm), run_time=.5)


class TestTypeWriter(ThreeDScene):
    CONFIG = {
        "text_kwargs": {
            "font": "RM Typerighter old Regular",
            "color": BLACK,
        }
    }
    
    def construct(self):
        self.prepare()
        self.add_sticks()
        self.write_word("ALI")

        
    def prepare(self):
        self.move_camera(phi=0, theta=-90 * DEGREES, distance=20)
        self.chasis = ImageMobject(ASSESTS_PATH + "frame_4.png").scale(1.9)
        self.cylinder = ImageMobject(ASSESTS_PATH + "cylinder.png").scale(0.3)
        self.cursor = ImageMobject(ASSESTS_PATH + "cursor.png").scale(0.3)
        self.paper = Rectangle(fill_color=WHITE, fill_opacity=1, width=4, height=3)

        self.chasis.set_xy(0.3, -1.4)
        self.cylinder.set_xy(0.3, 2.2)
        self.paper.set_xy(0.3, 3.4)
        self.cursor.move_to(self.cylinder)
        self.add(self.chasis, self.cylinder,self.paper, self.cursor)
        self.text_pos = self.cursor.get_center()
        self.cylinder.add(self.paper)
        self.keys = Group()
        self.keys_dict = {}
        self.arms_key = 'qwertyuiopasdfghjklzxcvbnm'
        self.add_keys(list("QWERTYUIOP"), start_x=-2.5, start_y=-1)
        self.add_keys([*list("ASDFGHJKL"), "fig"], start_x=-2.4, start_y=-1.4)
        self.add_keys([*list("ZXCVBNM"), "semicolon", "colon", "cap"], start_x=-2.3, start_y=-1.8)
 

    def add_keys(self, keys, start_x=-6.5, start_y=1):
        x = start_x
        for i in keys:
            i = i.lower()
            a = ImageMobject(ASSESTS_PATH + "keys/" + i + ".png").scale(.15)
            a.set_xy(x, start_y)
            self.add(a)
            self.keys.add(a)
            self.keys_dict[i] = a
            x += .6

    def add_sticks(self):
        t = -3.2 * PI / 4
        s = 2 * -t
        center_x = self.chasis.get_center()[0]
        center_y = 2
        r = 1.0
        
        self.arms = VGroup()
        for i in range(27):
            x = center_x + r * np.cos(t)
            x_2 = center_x + r * 2 * np.cos(t)
            y = center_y + r * np.sin(t)
            y_2 = center_y + r * 2 * np.sin(t)
            d = Dot(np.array([x, y, 0])).scale(.3)
            f = Dot(np.array([x_2, y_2, 0]))
            # self.play(FadeIn(d))
            arm = TypeWriterArm(d, f)
            self.arms.add(arm)
            t += s/70
        
        self.play(ShowCreation(self.arms))
        # for arm in arms:
            # arm.save_state()
            # self.play(arm.rotate, 180 * DEGREES, Z_AXIS, {"about_point":arm.point}, run_time=.5)
            # self.play(Restore(arm), run_time=.5)


    def click_key(self, key):
        img = self.keys_dict[key.lower()]
        arm = self.arms[self.arms_key.find(key.lower())]
        img.save_state()
        arm.save_state()
        text = Text(key, **self.text_kwargs).scale(.4).move_to(self.text_pos)
        self.play(arm.set_color, RED, run_time=.3)

        self.play(img.shift, .3 * DOWN,
                  self.cylinder.shift, .1 * LEFT,
                  Write(text),
                  arm.rotate, 180 * DEGREES, Z_AXIS, {"about_point":arm.point}, run_time=.5)
        self.play(Restore(img), Restore(arm),run_time=.5)
        self.paper.add(text)
        self.text_pos = text.get_center()

    def write_word(self, word):
        for i in word:
            self.click_key(i)


