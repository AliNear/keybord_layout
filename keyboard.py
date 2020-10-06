from manimlib.imports import *
from projects.keyboard_layout.consts import *
import random
import os

ASSESTS_PATH = os.getcwd() + "/projects/keyboard_layout/assets/"
ALPHABET = "qwertyuiopasdfghjklzxcvbnm"

def get_cross(obj, color=BLACK):
    cross = Line(ORIGIN, RIGHT, color=color).scale(obj.get_width() + .2)
    cross.move_to(obj)
    return cross

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
        self.dot = Dot(start, **self.line_kwargs).scale(.6)
        self.oblic = Line(start, end + .018 * direction_x, **self.line_kwargs)
        self.straight = Line(end, end + length  * direction_x, **self.line_kwargs)
        self.add(self.dot, self.oblic, self.straight)


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
        "mask_kwargs": {
            "fill_color": "#A5D48B",
            "fill_opacity": .6,
            "stroke_width": 1,
            "buff": SMALL_BUFF/4,
        }
    }

    def __init__(self, key, x=0, y=0, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.key_img = ImageMobject(self.key_path + key + ".png").scale(self.scale_factor)
        self.key_letter = key
        self.key_img.set_xy(x,y)
        self.add(self.key_img)
    def get_mask(self):
        rect = SurroundingRectangle(self, **self.mask_kwargs)
        return rect

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

    def __init__(self, layout, key_scale=.3, background=True, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.layout = layout
        self.key_scale = key_scale
        self.add_bakcground = background
        self.buffer = int(key_scale == .3) * .08 + int(key_scale != .3) * .05
        self.buffer_line = int(key_scale == .3) * .1 + int(key_scale != .3) * .08
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
                a = KeyImg(i, scale_factor=self.key_scale)
                row_group.add(a)
                self.keys_dict[i] = a
                if i in ALPHABET:
                    self.alpha_keys.append(a)
                else:
                    self.func_keys.append(a)

            row_group.set_x(-4)
            row_group.arrange_submobjects(RIGHT, True, True, buff=self.buffer)
            if r > 0:
                row_group.next_to(self.keys[r-1], DOWN, buff=self.buffer_line, aligned_edge=LEFT)
            self.keys.add(row_group)
            self.add(row_group)

        if self.add_bakcground:
            self.background = SurroundingRectangle(Group(*self.keys), 
                                               fill_color=WHITE,
                                               fill_opacity=1,
                                               stroke_width=2,
                                               stroke_color="#CFD2DA"
                                               )
            self.background.scale(.97)
            self.add(self.background)
        self.add(self.keys)

    def get_keys(self, keys):
        keys_obj = Group(*[self.keys_dict[i] for i in keys])
        return keys_obj


    def write_sequence(self, sequence, scene=None):
        seq = sequence.upper()
        for i in seq:
            key = self.keys_dict[i.lower()]
            rect = get_lower_rect(key, color=RED) 
            animation = (FadeIn(rect), FadeOut(rect))
            # animation.run_time = .5
            if scene is None:
                yield animation
            else:
                scene.play(animation, run_time=.5)
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

    def color_word(self, word):
        masks = Group()
        points = []
        for i in word.lower():
            key = self.keys_dict[i]
            masks.add(key.get_mask())
            points.append(key.get_center())
        obj = VGroup()
        for i in range(len(points)-1):
            obj.add(Dot(points[i], color=RED))
            obj.add(DashedLine(points[i], points[i+1], color=BLACK))

        obj.add(Dot(points[-1]))
 
 
        return masks, obj

    def explode(self, scene):
        animations = VGroup()
        directions = [UL, UP, UR, RIGHT, DR, DOWN, DL, LEFT]
        self.keys.save_state()
        dir_index = 0
        for i in self.keys_dict.keys():
            key = self.keys_dict[i]
            key.save_state()
            if i in ALPHABET:
                #Needed for rearrange_keys
                key.old_pos = key.get_center()
            x = np.random.randint(1, 4)
            w = x * directions[dir_index % 8]
            s = .3
            v = key.get_x() * s * RIGHT + key.get_y() * s * UP
            animations.add(ApplyMethod(key.shift, v))
            dir_index += 1
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

        scene.play(LaggedStart(*animations_alpha_keys))
        scene.wait(1)
        scene.play(*animations_func_keys)
                

       

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



class PartOne(Scene):
    """
    In this part we will introduce the qwerty keyboard, and explain some parts
    """
    CONFIG = {
        "text_kwargs": {
            "font": "SF Pro Display Bold",
            "color": WHITE,
        },
        "line_text_kwargs": {
            "font": "SF Pro Display Bold",
            "color": "#F7D95B",
        },
        "surround_rect_kwargs": {
            "color": "#A5D48B",
            "stroke_width": 7,
        },

    }

    def construct(self):
        self.prepare()
        self.introduction()
        # self.questioning()

    def prepare(self):
        layout = QWERTY_LAYOUT
        self.keyboard = Keyboard(layout, background=False)

    def introduction(self):
        self.play(FadeInFrom(self.keyboard, 2 * DOWN))
        text = Text("The QWERTY Keyboard", **self.text_kwargs).scale(1.0)
        text.set_y(3.5)
        self.play(FadeInFrom(text, 2 * UP))
        #Qwerty name origin
        qwerty = self.keyboard.get_keys("qwerty")
        qwerty.save_state()
        self.play(qwerty.scale, 2)
        self.wait(.5)
        self.play(Restore(qwerty))
        self.wait(.5)

        self.play(self.keyboard.shift, 2.2 * LEFT)
        row_names = ["Upper row", "Home row", "Lower row"]
        row_texts = VGroup()
        arrows = VGroup()
        row = self.keyboard.get_keys(QWERTY_LAYOUT[0])
        rect = Rectangle(width=row.get_width()+.1, height=row.get_height()+.1,
                         **self.surround_rect_kwargs)
        j = 0
        for i in row_names:
            row = self.keyboard.get_keys(QWERTY_LAYOUT.pop(0))
            point = self.keyboard.keys[j].get_edge_center(RIGHT)
            arrow = PointObject(point)
            row_text = Text(i, **self.line_text_kwargs).scale(.8)
            row_text.next_to(arrow.straight, UP, buff=.2)
            self.play(rect.move_to, row)
            self.play(ShowCreation(arrow))
            self.play(FadeInFrom(row_text, 2 * RIGHT))
            row_texts.add(row_text)
            arrows.add(arrow)
            j += 1
        self.play(FadeOut(rect))
        self.wait()
        self.play(FadeOut(arrows), FadeOut(row_texts))
        self.play(self.keyboard.shift, 2.2 * RIGHT)

        #Show why it's named Home row
        hands = ImageMobject(ASSESTS_PATH + "hands.png")
        hands.scale(3)
        hands.set_xy(-1, -2.5)
        self.play(FadeInFrom(hands, 2 * DOWN))
        self.wait(.3)
        self.play(FadeOut(hands))




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
        

class PartFour(Scene):
    """
    In this part we will type a list of words and show that qwerty 
    layout isn't that great
    """
    CONFIG = {
        "text_kwargs": {
            "font": "SF Pro Display Semibold",
            "color": WHITE,
        },
        "title_kwargs": {
            "font": "SF Pro Display Bold",
            "color": "#F7D95B",
        },
        "editor_text_kwargs": {
            "font": "SF Pro Display Regular",
            "color": WHITE,  #It has to be "Invisible" at first
        }
    }

    def construct(self):
        self.prepare()
        self.add_screen()
        self.type_words(1)
        self.show_typing_complexity(1)

    def prepare(self):
        self.keyboard = Keyboard(QWERTY_LAYOUT, key_scale=.2, background=False).shift(DOWN)
        self.screen = ImageMobject(ASSESTS_PATH + "computer.png").scale(2)
        self.screen.set_y(1.8)
        self.editor = ImageMobject(ASSESTS_PATH + "editor.png")
        self.editor.move_to(self.screen)
        self.editor.shift((.5 * UP))

    def add_screen(self):
        # self.play(FadeInFrom(self.keyboard, 2 * DOWN), run_time=.6)
        self.add(self.keyboard)
        self.play(FadeInFrom(self.screen, 2 * UP))
        self.play(GrowFromCenter(self.editor), run_time=.5)
        self.screen.add(self.editor)
        self.wait()

    def type_words(self, num_words=5):
        words_title = Text("Words", **self.title_kwargs).scale(.8)
        words_pos = self.screen.get_corner(UL)
        words_title.move_to(words_pos).shift(3 * LEFT + .4 * DOWN)
        self.play(GrowFromCenter(words_title))
        
        self.words_list = ["read", "morning", "the", "hello", "anyone"]
        self.words_list = self.words_list[:num_words]
        self.texts_obj = VGroup(*[Text("• " + i, **self.text_kwargs).scale(.6) for i in self.words_list])
        self.texts_obj.arrange_submobjects(DOWN, True, True, aligned_edge=LEFT)
        self.texts_obj.next_to(words_title, DOWN, buff=.4, aligned_edge=LEFT)
        animations = LaggedStart(*[FadeIn(i) for i in self.texts_obj], lag_ratio=.5)
        self.play(animations)
        
        pos = self.editor.get_corner(UL) + .2 * DR
        self.texts_editor = VGroup(*[Text(i, **self.editor_text_kwargs).scale(.3) for i in self.words_list])
        self.texts_editor.arrange_submobjects(DOWN, True, True, aligned_edge=LEFT, buff=.1)
        self.texts_editor.next_to(pos, DOWN, buff=.05, aligned_edge=LEFT)
        self.add(self.texts_editor)
        k = 0
        self.current_rect = SurroundingRectangle(self.texts_obj[k][2:], stroke_color=RED)
        self.play(ShowCreation(self.current_rect))

        for i in self.words_list:
            animations = self.keyboard.write_sequence(i)
            word = iter(self.texts_editor[k])
            for j in animations:
                self.play(j[0],
                          next(word).set_color, BLACK,
                          run_time=.1
                          )
                self.play(j[1], run_time=.1) 

            self.wait()
            k += 1

            if k < len(self.words_list):
                self.play(
                    self.current_rect.move_to, self.texts_obj[k][2:],
                    self.current_rect.set_width, self.texts_obj[k][2:].get_width() + .2, True
                )


    def show_typing_complexity(self, num_words):
        """
        Here we start showing cons of qwerty, starting by the key movements
        Cons we'll mention:
        - Awkward finger motion
        - Jumping over home row
        - Left hand
        """
        #Move the screen away
        self.play(FadeOut(self.screen), FadeOut(self.texts_editor))
        self.cons_title = Text("Cons", **self.title_kwargs).scale(.8)
        self.cons_pos = self.screen.get_corner(UR)
        self.cons_title.move_to(self.cons_pos).shift(3 * RIGHT + .4 * DOWN)
        self.play(GrowFromCenter(self.cons_title))

        self.cons_list = ["Complicated\n finger motion", "One hand typing", "Jumping over the home row"]
        self.cons_obj = VGroup(*[Text("• " + i, **self.text_kwargs).scale(.6) for i in self.cons_list])
        self.cons_obj.arrange_submobjects(DOWN, True, True, aligned_edge=LEFT)
        self.cons_obj.next_to(self.cons_title, DOWN, buff=.4, aligned_edge=LEFT)

        self.words_list = self.words_list[:num_words]
        firt_iteration = True
        for i in range(len(self.words_list)-1, -1, -1):
            k = i - 1
            masks, dot_line = self.keyboard.color_word(self.words_list[i])
            animations = [GrowFromCenter(i) for i in masks]
            self.play(LaggedStart(*animations))
            self.wait(.3)
            self.play(ShowCreation(dot_line), run_time=1.5)
            self.wait(.3)
            self.play(FadeOut(masks), FadeOut(dot_line))
            if k > -1:
                self.play(
                    self.current_rect.move_to, self.texts_obj[k][2:],
                    self.current_rect.set_width, self.texts_obj[k][2:].get_width() + .2, True
                )
            if firt_iteration:
                self.play(FadeInFrom(self.cons_obj[0], 2 * UP))




class PartTwo(MovingCameraScene):
    CONFIG = {
        "text_kwargs": {
            "font": "SF Pro Display Bold",
            "color": WHITE,
        },
        "line_text_kwargs": {
            "font": "SF Pro Display Bold",
            "color": "#F7D95B",
        },
 

    }

    def construct(self):
        self.ticks_texts = ["Now", "1970","1930", "1868"]
        images = ["keyboard", "old_keyboard", "teletype_1", "typewriter"]
        self.images = [i + ".png" for i in images]
        self.titles = ["Current", "Electronic Keyboard", "Teletype", "Typewriter"]
        self.scales = [.8, 1.0, 1.0, 1]
 
        img = ImageMobject(ASSESTS_PATH + "keyboard.png").scale(.8)
        tick = Line(ORIGIN, ORIGIN + .2 * UP, stroke_width=5)
        text = Text("Current", **self.line_text_kwargs).scale(.8)
        tick_text = Text("Now", **self.text_kwargs).scale(.7)
        text.next_to(img, UP, buff=.1)
        
        self.line = Line(RIGHT, ORIGIN)
        self.line.match_width(img)
        self.line.next_to(img, DOWN, aligned_edge=RIGHT)
        tick.next_to(self.line, DOWN, buff=.02)
        tick_text.next_to(tick, DOWN, buff=.02)
        animations = LaggedStart(
            FadeIn(img, 4 * DOWN),
            ShowCreation(self.line),
            ShowCreation(tick),
            GrowFromCenter(text),
            FadeIn(tick_text, 2 * DOWN)

        )
        self.play(animations, run_time=1.2)
        self.next_line = Line(ORIGIN,  6 * LEFT)
        self.next_line.next_to(self.line, LEFT, buff=0)
        self.camera_frame.save_state()
        self.play(
            self.camera_frame.set_width, 4,
            self.camera_frame.set_height, 5,
            self.camera_frame.shift, 7 * LEFT,
            ShowCreation(self.next_line)
        )
        self.i = 2
        for i in range(1, 4):
            self.add_milestone(i)
            if i < 3:
                self.play(
                    self.camera_frame.shift, 8 * LEFT,
                    ShowCreation(self.next_line)
                )


    def add_milestone(self, index):
        current = self.next_line.get_edge_center(LEFT)
        tick = Line(ORIGIN, ORIGIN + .2 * UP, stroke_width=5)
        tick_text = Text(self.ticks_texts[index], **self.text_kwargs).scale(.7)
        text = Text(self.titles[index], **self.line_text_kwargs).scale(.7)
        img = ImageMobject(ASSESTS_PATH + self.images[index]).scale(self.scales[index])
        img.next_to(current, UP, buff=.2)
        text.next_to(img, UP, buff=.1)
        tick.next_to(img, DOWN, buff=.19)
        tick_text.next_to(tick, DOWN, buff=.02)

        new_next_line = Line(ORIGIN, 8 * LEFT)
        new_next_line.next_to(self.next_line, LEFT, buff=0)

        animations = LaggedStart(
            FadeIn(img, 4 * DOWN),
            ShowCreation(tick),
            GrowFromCenter(text),
            FadeIn(tick_text, 2 * DOWN)

        )
        self.play(animations, run_time=1.2)
        self.next_line = new_next_line

class Test(Scene):
    def construct(self):
        obj = Circle()


