from manimlib.imports import *
from projects.keyboard_layout.consts import *
import random
import os

ASSESTS_PATH = os.getcwd() + "/projects/keyboard_layout/assets/"
ALPHABET = "qwertyuiopasdfghjklzxcvbnm"

def get_lower_rect(obj, color="#41BC27"):
    p1 = obj.get_corner(DL) + .008 * RIGHT
    p2 = obj.get_corner(DR) - .008 * RIGHT
    p3 = p1 + .06 * UP
    p4 = p2 + .06 * UP
    return Polygon(p1, p2, p4, p3, fill_color=color, fill_opacity=1, stroke_width=0)

class PointObject(VMobject):
    """Creates a pointing line with an inflection.
    Parameters
    ----------
    point: The point which the line points to
    direction_x: x direction of pointing (RIGHT or LEFT)
    direction_y: y direction of pointing (UP or DOWN)

    """
    CONFIG = {
        "line_kwargs": {
            "color": WHITE,
            "stroke_width": 5
        }
    }
    def __init__(self, point, direction_x=RIGHT, direction_y=UP, length=2, **kwargs):
        VMobject.__init__(self, **kwargs)
        start = point
        x_amount = length / 3
        y_amount = x_amount * 2
        inflection = y_amount * direction_y + x_amount * direction_x
        end = start + inflection
        self.oblic = Line(start, end, **self.line_kwargs)
        self.straight = Line(end, end + length  * direction_x, **self.line_kwargs)
        self.add(self.oblic, self.straight)


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
        self.key_text = Text(key, **self.key_text_args).scale(self.scale_key * width)
        self.key_text.move_to(self.boundaries)
        self.add(self.boundaries, self.key_text)
    def glow(self, color):
        touch = ApplyMethod(self.boundaries.set_fill, color, .8)
        lift = ApplyMethod(self.boundaries.set_fill, color, 0)
        return (touch, lift)
    def set_color(self, color):
        animation = ApplyMethod(self.boundaries.set_fill, color, .8)
        return animation

class KeyImg(Mobject):
    CONFIG = {
        "scale_factor": .3,
        "key_path": ASSESTS_PATH + "normal_keys/",
    }

    def __init__(self, key, x=0, y=0, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.key_img = ImageMobject(self.key_path + key + ".png").scale(self.scale_factor)
        self.key_letter = key
        self.key_img.set_xy(x,y)
        self.add(self.key_img)

class Keyboard(VMobject):
    """
    A Keyboard class that draws a keys on the screen with a give layout
    """
    CONFIG = {
        "start_x": -3.5,
        "start_y": -1,
        "spacing_y": .65,
        "width_key": .7,
        "height_key": .7,

    }

    def __init__(self, layout,**kwargs):
        VMobject.__init__(self, **kwargs)
        self.layout = layout
        self.keys = Group()
        self.keys_dict = {}
        self.alpha_keys = []
        self.func_keys = []
        self.add_keys(layout)

    def add_keys(self, layout):
        for r in range(len(layout)):
            row = layout[r]
            row_group = Group()
            for i in row:
                a = KeyImg(i)
                row_group.add(a)
                self.keys_dict[i] = a
                if i in ALPHABET:
                    self.alpha_keys.append(a)
                else:
                    self.func_keys.append(a)

            row_group.set_x(-4)
            row_group.arrange_submobjects(RIGHT, False, False, buff=.08)
            if r > 0:
                row_group.next_to(self.keys[r-1], DOWN, buff=.1, aligned_edge=LEFT)
            self.keys.add(row_group)
            self.add(row_group)

        # self.background = SurroundingRectangle(Group(*self.keys), 
                                               # fill_color=WHITE,
                                               # fill_opacity=1,
                                               # stroke_width=0)
        # self.add(self.background)
        self.add(self.keys)

    def write_sequence(self, sequence, scene):
        seq = sequence.upper()
        for i in seq:
            key = self.keys_dict[i.lower()]
            rect = get_lower_rect(key, color=RED) 
            animations = Succession(FadeIn(rect), FadeOut(rect))
            scene.play(animations, run_time=.5)
    def move_keys(self, keys, start_x, start_y, scene):
        limit=.1
        j = 0
        animations = VGroup()
        x = start_x
        for i in keys:
            k = self.keys_dict[i]
            position = np.array([x + j * limit, start_y, 0])
            animations.add(ApplyMethod(k.move_to, position))
            x += .65
            j += 1
        scene.play(*animations)

    def color_word(self, word, scene):
        animations = VGroup()
        for i in word.upper():
            key = self.keys_dict[i]
            animations.add(key.set_color(GREEN))
        scene.play(LaggedStart(*animations, lag_ratio=.3))

    def explode(self, scene):
        animations = VGroup()
        directions = [UP, DOWN, RIGHT, LEFT]
        self.keys.save_state()
        for i in self.keys_dict.keys():
            key = self.keys_dict[i]
            key.save_state()
            if i in ALPHABET:
                #Needed for rearrange_keys
                key.old_pos = key.get_center()
            x = np.random.randint(1, 5)
            y = np.random.randint(1, 3)
            v = x * random.choice(directions) + y * random.choice(directions)
            animations.add(ApplyMethod(key.shift, v))
        scene.play(*animations)

    def rearrange_keys(self, layout, scene):
        """
        In this animation we rearrange keys given a layout, we use previous 
        key positions to make it easier to implement
        """
        alpha_keys = []
        animations_alpha_keys = Group()
        animations_func_keys = Group()
        t = 0
        for i in layout:
            for j in i:
                if j in ALPHABET:
                    key = self.alpha_keys[t]
                    new_key = self.keys_dict[j]
                    animations_alpha_keys.add(ApplyMethod(new_key.move_to, key.old_pos))
                    t += 1
                else:
                    animations_func_keys.add(Restore(self.keys_dict[j]))

        scene.play(*animations_func_keys)
        scene.wait(1)
        scene.play(*animations_alpha_keys)
                

       

class FramedImage(ImageMobject):
    CONFIG = {
        "frame_kwargs": {
            "color": BLUE,
            "stroke_width": 3,
        },
        "title_kwargs": {
            "font": "Century Gothic Bold",
            "color": WHITE,
        }
    }

    def __init__(self, filename, title, **kwargs):
        ImageMobject.__init__(self, filename, **kwargs)
        self.scale(.5)
        width = self.get_width()
        height = self.get_height()
        frame = Rectangle(width=width, height=height, **self.frame_kwargs)
        title_text = Text(title, **self.title_kwargs).scale(.5)
        title_text.next_to(frame, UP, buff=.1)
        self.add(frame,  title_text)

class QwertyKB(Scene):
    def construct(self):
        self.prepare()
        self.add_screen()
        self.write_on_screen()

    def prepare(self):
        self.keys = VGroup()
        self.keys_dict = {}
        self.first = True
        x = -3.5
        y = -1
        y_spacing = 0.85
        self.add_keys(list("QWERTYUIOP"), start_x=x, start_y=y)
        self.add_keys(list("ASDFGHJKL"), start_x=x+.5, start_y=y-y_spacing)
        self.add_keys(list("ZXCVBNM"), start_x=x+1, start_y=y-2*y_spacing)
        self.add_keys(list(" "), start_x=x+4, start_y=y-3*y_spacing, width=5)
    
    def add_keys(self, keys, start_x=-6.5, start_y=1, width=.7, height=.7):
        limit=.1
        j = 0
        animations = VGroup()
        x = start_x
        for i in keys:
            a = Key(i, x = x + j * limit, y=start_y, width=width, height=height)
            animations.add(ShowCreation(a))
            self.keys.add(a)
            self.keys_dict[i] = a
            x += width
            j += 1
        self.play(LaggedStart(*animations))

    def add_screen(self):
        screen_width = 7
        screen_height = 3.5
        x_screen, y_screen = 0, 1.5
        self.screen_rect = Rectangle(width=screen_width, height=screen_height)
        self.screen_rect.set_fill(color=WHITE, opacity=1)
        self.screen_rect.set_stroke(color=GREY, width=3)
        self.screen_rect.set_xy(x_screen, y_screen)
        self.screen_header = Rectangle(width=1.3, height=.4)
        self.screen_header.set_fill(color=BLUE, opacity=.5)
        self.screen_header.next_to(self.screen_rect, UP+LEFT, buff=0.03)
        self.screen_header.shift(1.35*RIGHT)
        self.title = Text("File1.txt", color=BLACK, font="Apercu-Mono").scale(.4)
        self.title.move_to(self.screen_header)
        self.screen = VGroup(self.screen_rect, self.screen_header, self.title)

    def write_on_screen(self):
        self.play(FadeInFrom(self.screen, 2 * RIGHT))
        cursor = Text("|", color=BLACK, font="Apercu-Mono").scale(.4)
        cursor.next_to(self.title, DOWN, buff=.5)
        self.play(Write(cursor))
        text="Just"
        for i in text:
            key = self.keys_dict[i.upper()]
            t = Text(i, color=BLACK, font="Apercu-Mono").scale(.4)
            t.next_to(cursor, RIGHT, buff=.02)
            a = key.glow(RED)
            self.play(Write(t), cursor.shift,.1 * RIGHT,a[0], run_time=.3)
            self.play(a[1], run_time=.2)


        

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
            key = self.keys_dict[i.upper()]
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

class TypeWriter(ThreeDScene):

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
        self.add_sound(ASSESTS_PATH + "sounds/typewriter-key.wav")
        self.play(img.shift, .3 * DOWN,
                  self.cylinder.shift, .1 * LEFT,
                  Write(text),
                  arm.rotate, 180 * DEGREES, Z_AXIS, {"about_point":arm.point}, run_time=.1)
        self.play(Restore(img), Restore(arm),run_time=.1)
        self.paper.add(text)
        self.text_pos = text.get_center()

    def write_word(self, word):
        for i in word:
            self.click_key(i)
        self.paper.plot_depth=10
        self.play(
            self.paper.move_to, ORIGIN,
            self.paper.scale, 2
        )


class AxisScene(MovingCameraScene):
    
    def construct(self):
        axis = Line(20 * LEFT, 5 * RIGHT, stroke_width=4)
        ticks_coords = [0, -3.5, -6, -9]
        ticks_texts = ["Now", "1970","1930", "1868"]
        images = ["keyboard", "old_keyboard", "teletype", "typewriter"]
        images = [i + ".jpg" for i in images]
        titles = ["Current", "Electronic Keyboard", "Teletype", "Typewriter"]
        axis.add_tip()
        self.play(ShowCreation(axis))
        ticks = VGroup()
        texts = VGroup()
        figures = Group()
        for i in range(4):
            start = np.array([ticks_coords[i], 0, 0])
            tick = Line(start, start + .2 * UP, stroke_width=4)
            text = Text(ticks_texts[i], font="Century Gothic Bold", color=BLACK).scale(.6)
            img = FramedImage(ASSESTS_PATH + images[i], titles[i])
            text.next_to(tick, DOWN, buff=.2)
            img.next_to(tick, UP, buff=0.5)
            ticks.add(tick)
            texts.add(text)
            figures.add(img)
        
        for i in range(4):
            self.play(ShowCreation(ticks[i]), run_time=.3)
            self.play(Write(texts[i]), run_time=.4)
            self.play(FadeInFrom(figures[i], 3 * UP))

        self.wait()

        self.play(
            self.camera_frame.set_height, 5)
        self.play(
            self.camera_frame.shift, 9 * LEFT, run_time=2, rate_func=linear
        )
        


class PartOne(Scene):
    """
    In this part we will introduce the qwerty keyboard, and explain some parts
    """
    CONFIG = {
        "text_kwargs": {
            "font": "SF Pro Display Regular",
            "color": BLACK,
        }
 
    }

    def construct(self):
        self.prepare()
        self.introduction()
        self.questioning()

    def prepare(self):
        layout = QWERTY_LAYOUT
        self.keyboard = Keyboard(layout)

    def introduction(self):
        self.play(ShowCreation(self.keyboard))
        text = Text("The QWERTY Keyboard", **self.text_kwargs).scale(1.0)
        text.set_y(3.5)
        self.play(FadeInFrom(text, 2 * UP))
        self.play(self.keyboard.shift, 2.5 * LEFT)
        row_names = ["Upper row", "Home row", "Lower row"]
        row_texts = VGroup()
        arrows = VGroup()
        x = 2.5
        y_start = -1
        j = 0
        for i in row_names:
            point = self.keyboard.keys[j].get_edge_center(RIGHT)
            arrow = PointObject(point)
            row_text = Text(i, **self.text_kwargs).scale(.8)
            row_text.next_to(arrow.straight, UP, buff=.2)
            self.play(ShowCreation(arrow))
            self.play(FadeInFrom(row_text, 2 * RIGHT))
            row_texts.add(row_text)
            arrows.add(arrow)
            y_start -= self.keyboard.spacing_y
            j += 1

        self.wait()
        self.play(FadeOut(arrows), FadeOut(row_texts))
        self.play(self.keyboard.shift, 2.5 * RIGHT)
        self.keyboard.write_sequence("ALI", self)


    def questioning(self):
        text = Text("But why this particular order?", **self.text_kwargs).scale(.8)
        text.set_y(1)
        self.play(Write(text))
        new_text = Text("Why not like this?", **self.text_kwargs).scale(.8)
        new_text.set_y(1)
        self.play(Transform(text, new_text))
        self.keyboard.explode(self)
        self.keyboard.rearrange_keys(ALPHA_LAYOUT, self)
        self.wait()
        

class Test(Scene):
    def construct(self):
        e = KeyImg("e")

