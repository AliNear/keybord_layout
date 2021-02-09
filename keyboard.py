import os

from manimlib.imports import *
from projects.keyboard_layout.consts import *
from projects.keyboard_layout.new_stuff import get_fading_boxes_random
from projects.animations.pie_chart import PieChart
from projects.animations.useful_animations import TextWithHighlight
from random import choice

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


def get_surrounding_trans(mobject, opacity=.3):
    rect = RoundedRectangle(width=mobject.get_width() * 1.2, height=mobject.get_height() * 1.5,
                            color=WHITE, fill_color=WHITE,
                            stroke_width=0, fill_opacity=opacity, corner_radius=.1)

    # height = mobject.get_height()
    # rect.set_height(height * 1.2)
    rect.move_to(mobject)
    return rect


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
        self.straight = Line(end, end + length * direction_x, **self.line_kwargs)
        self.add(self.dot, self.oblic, self.straight)


class Key(VMobject):
    CONFIG = {
        "key_text_args": {
            "color": WHITE,
            "font": "DDT W00 Regular",
        },
        "scale_key": 1.2,
    }

    def __init__(self, key, x=0, y=0, width=1, height=1, **kwargs):
        VMobject.__init__(self, **kwargs)
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
            "color": WHITE,
            "fill_opacity": .6,
            "stroke_width": 1,
            "buff": SMALL_BUFF / 4,
        }
    }

    def __init__(self, key, x=0, y=0, **kwargs):
        Mobject.__init__(self, **kwargs)
        self.key_img = ImageMobject(self.key_path + key + ".png").scale(self.scale_factor)
        self.key_letter = key
        self.key_img.set_xy(x, y)
        self.add(self.key_img)

    def get_mask(self, color="#EE243D"):
        rect = SurroundingRectangle(self, fill_color=color, **self.mask_kwargs)
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
                row_group.next_to(self.keys[r - 1], DOWN, buff=self.buffer_line, aligned_edge=LEFT)
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
        limit = .1
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
        for i in range(len(points) - 1):
            obj.add(Dot(points[i], color=RED))
            obj.add(DashedLine(points[i], points[i + 1], color=BLACK))

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
                # Needed for rearrange_keys
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

    def rearrange_keys_no_anim(self, old_changing, new_changing, scene):
        """
        In this animation we rearrange keys given a layout, we use previous
        key positions to make it easier to implement
        """
        positions = []
        for i in old_changing:
            pos = []
            for j in i:
                key = self.keys_dict[j]
                pos.append(key.get_center())

            positions.append(pos)
        k = 0
        for i in new_changing:
            m = 0
            for j in i:
                key = self.keys_dict[j]
                key.move_to(positions[k][m])
                m+= 1
            k +=  1

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
                    new_key.move_to(key.old_pos)
                    t += 1
                else:
                    self.keys_dict[j].restore()


"""
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
        self.add(frame, title_text)


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
        },
        "text_white": {
            "font": "RM Typerighter old Regular",
            "color": WHITE,
        },
        "normal_text_kwargs": {
            "font": "Agency FB",
            "color": WHITE,
        },
        "letter_font": "DTT W00 Regular",

    }

    def construct(self):
        self.prepare()
        self.add_sticks()
        self.regroup_objects(add_to_scene=True)
        self.typeWriter_animation()
        self.wait()
        self.show_inventor()
        self.wait()
        self.write_word("Hi")
        self.wait()
        self.questioning()
        self.jamming()
        self.japan_guy()
        self.wait()
        self.after_morse()
        self.wait()
        self.morse_similarities()
        self.wait()
        self.morse_similarities_2()

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
        # self.add(self.chasis, self.cylinder,self.paper, self.cursor)
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
            # self.add(a)
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
            t += s / 70
        # self.play(ShowCreation(self.arms))
        # for arm in arms:
        # arm.save_state()
        # self.play(arm.rotate, 180 * DEGREES, Z_AXIS, {"about_point":arm.point}, run_time=.5)
        # self.play(Restore(arm), run_time=.5)

    def regroup_objects(self, add_to_scene=False):
        self.typewriter_obj = Group(
            self.cylinder,
            self.cursor,
            self.chasis,
            self.keys,
            self.arms
        )
        # This is used just to win some time (no animation needed to add the typerwriter)
        if add_to_scene:
            self.add(self.typewriter_obj)

    def typeWriter_animation(self):

        self.typewriter_obj.scale(.7)
        self.play(
            LaggedStart(
                FadeInFrom(self.cylinder, LEFT),
                GrowFromCenter(self.cursor),
                FadeInFrom(self.chasis, DOWN),
                ShowIncreasingSubsets(self.keys),
                ShowIncreasingSubsets(self.arms),
            )
        )

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
                  arm.rotate, 180 * DEGREES, Z_AXIS, {"about_point": arm.point}, run_time=.1)
        self.play(Restore(img), Restore(arm), run_time=.1)
        self.paper.add(text)
        self.text_pos = text.get_center()

    def write_word(self, word):
        for i in word:
            self.click_key(i)
        self.paper.save_state()
        self.paper.plot_depth = 10
        self.play(
            self.paper.move_to, ORIGIN,
            self.paper.scale, 2
        )
        self.play(Restore(self.paper))

    def get_highlight_key(self, letter):
        """
        Given a letter returns an ellips that highlight the key
        corresponding to the letter
        """
        key = self.keys_dict[letter]
        w, h = 109, 46
        ellips_width = w / h
        ellips_height = 1

        ellipse = Ellipse(
                    fill_color="#e63946",
                    fill_opacity=.5,
                    width=ellips_width,
                    height=ellips_height,
                    stroke_width=0,
                 ).scale(.15)

        ellipse.move_to(key.get_center() + .035 * UP)
        return ellipse

    def show_inventor(self):
        self.scholes = ImageMobject(ASSESTS_PATH + "christopher_scholes.png")
        self.scholes_name = Text("Christopher Scholes", **self.text_white).scale(1.5)
        self.scholes.scale(2)
        self.scholes.move_to(self.typewriter_obj)
        self.scholes.shift(.5 * LEFT)
        self.scholes_name.next_to(self.scholes, 1.5 * DOWN)
        self.typewriter_obj.save_state()
        self.play(
            self.typewriter_obj.scale, .6,
            self.typewriter_obj.shift, 4 * RIGHT,
            FadeInFrom(self.scholes, 3 * LEFT)
        )
        self.play(ShowIncreasingSubsets(self.scholes_name))
        self.wait(1)
        self.play(
            FadeOutAndShift(self.scholes, 3 * LEFT),
            FadeOutAndShift(self.scholes_name, 3 * LEFT),
            Restore(self.typewriter_obj)
        )
        # self.play(FadeIn(self.scholes))

    def questioning(self):
        question = Text("But why is it QWERTY?", **self.normal_text_kwargs)
        # self.play(ShowIncreasingSubsets(question), run_time=1.5)
        self.play(
            self.typewriter_obj.shift, FRAME_WIDTH * .75 * LEFT,
            FadeInFrom(question, FRAME_WIDTH * .75 * RIGHT),
            run_time=2
        )
        self.wait()
        self.play(
            self.typewriter_obj.shift, -FRAME_WIDTH * .75 * LEFT,
            FadeOutAndShift(question, FRAME_WIDTH * .75 * RIGHT),
            run_time=2
        )

    def jamming(self):
        self.click_key("Q")
        self.click_key("W")
        self.wait()
        arm_q = self.arms[self.arms_key.find("q")]
        arm_w = self.arms[self.arms_key.find("w")]
        self.play(
            arm_q.set_color, RED,
            arm_w.set_color, RED,
        )
        c = Circle(radius=.2).move_to(arm_q)
        self.play(ShowCreation(c))
        self.wait()
        self.play(
            FadeOut(c),
            arm_q.set_color, WHITE,
            arm_w.set_color, WHITE,
        )

        def point_two_keys(a, b):
            ellips_a = self.get_highlight_key(a)
            ellips_b = self.get_highlight_key(b)
            self.play(
                GrowFromCenter(ellips_a),
                GrowFromCenter(ellips_b),
            )
            return VGroup(ellips_a, ellips_b)

        ellips_group = point_two_keys("t", "h")
        example_one = Text("The", **self.normal_text_kwargs)
        dot_example = Dot(color=WHITE).set_xy(-5.5, 3)
        example_one.next_to(dot_example, RIGHT)
        example_one.submobjects[0].set_color(RED)
        example_one.submobjects[1].set_color(RED)
        self.play(
            GrowFromCenter(dot_example),
            Write(example_one)
        )
        self.wait()
        self.play(
            FadeOut(ellips_group),
        )
        # S and T
        ellips_group = point_two_keys("s", "t")
        example_two = Text("Host", **self.normal_text_kwargs)
        example_two.next_to(dot_example, RIGHT)
        example_two.submobjects[2].set_color(RED)
        example_two.submobjects[3].set_color(RED)
        self.play(ReplacementTransform(example_one, example_two))
        self.wait()
        self.play(
            FadeOut(ellips_group),
        )

        # H and E
        ellips_group = point_two_keys("h", "e")
        example_one = Text("The", **self.normal_text_kwargs)
        example_one.next_to(dot_example, RIGHT)
        example_one.submobjects[1].set_color(RED)
        example_one.submobjects[2].set_color(RED)

        self.play(ReplacementTransform(example_two, example_one))
        self.wait()
        self.play(
            FadeOut(ellips_group),
            FadeOut(example_one),
            FadeOut(example_two),
            FadeOut(dot_example)
        )

    def japan_guy(self):
        self.japs = ImageMobject(ASSESTS_PATH + "koichi_yasuoka.png").scale(1.5)
        self.japs_name = Text("Koichi Yasuoka", **self.normal_text_kwargs)
        self.japs_name.next_to(self.japs, DOWN)

        self.play(
            self.typewriter_obj.shift, 1.2 * FRAME_HEIGHT * DOWN,
            LaggedStart(
                FadeInFrom(self.japs, 1.2 * FRAME_HEIGHT * UP),
                ShowIncreasingSubsets(self.japs_name)
            ),
            run_time=2,
            rate_function=linear
        )
        # Add a telegraph operator image
        self.operator = ImageMobject(ASSESTS_PATH + "telegraph_op.jpg").scale(1.8)
        self.play(
            FadeOut(self.japs),
            FadeOut(self.japs_name),
            GrowFromCenter(self.operator)
        )

    def after_morse(self):
        """
        This will play after the new Morse Scene (new class)
        """
        self.clear()
        self.morse_us = ImageMobject(ASSESTS_PATH + "morse_us.png").scale(2)
        self.play(StretchFromSide(self.morse_us, LEFT))
        self.wait()
        self.play(FadeOutAndShift(self.morse_us, DOWN))

    def morse_similarities(self):
        y_div = FRAME_HEIGHT / 2
        self.v_divider = Line(y_div * UP, y_div * DOWN, color="#ced4da", stroke_width=2)
        self.z_letter = Text("Z", font=self.letter_font, color="#adb5bd").scale(2)
        self.se_letter = Text("SE", font=self.letter_font, color="#adb5bd").scale(2)
        self.z_letter.set_xy(-4, 2.5)
        self.se_letter.set_xy(4, 2.5)
        self.z_morse = VGroup(*[Dot(color=WHITE).scale(1.5) for i in range(4)])
        self.se_morse = VGroup(*[Dot(color=WHITE).scale(1.5) for i in range(4)])
        self.z_morse.arrange(RIGHT, True, False, buff=.4)
        self.se_morse.arrange(RIGHT, True, False, buff=.4)
        self.z_morse.next_to(self.z_letter, DOWN, buff=2)
        self.se_morse.next_to(self.se_letter, DOWN, buff=2)

        self.play(ShowCreation(self.v_divider))
        self.play(
            GrowFromCenter(self.z_letter),
            GrowFromCenter(self.se_letter),
        )
        for i in range(4):
            z = self.z_morse[i]
            se = self.se_morse[i]
            self.play(
                GrowFromPoint(z, z.get_edge_center(LEFT), run_time=.5),
                GrowFromPoint(se, se.get_edge_center(LEFT), run_time=.5),
            )

        self.objects_group = VGroup(self.v_divider, self.z_letter,
                                    self.se_letter, self.z_morse,
                                    self.se_morse)

        self.play(
            self.objects_group.shift, 8 * UP,
            self.typewriter_obj.move_to, ORIGIN
        )
        ellipsises = VGroup(
            *[
                self.get_highlight_key(i)
                for i in "zse"
            ]
        )
        self.play(
            *[
                GrowFromCenter(i)
                for i in ellipsises
            ]
        )
        self.wait()
        self.play(
            *[
                ShrinkToCenter(i)
                for i in ellipsises
            ]
        )

    def morse_similarities_2(self):
        self.play(
            self.objects_group.shift, 8 * DOWN,
            self.typewriter_obj.shift, 8.32 * DOWN
        )

        self.c_letter = Text("C", font=self.letter_font, color="#adb5bd").scale(2)
        self.c_letter.set_xy(-4, 2.5)
        # self.c_morse = self.z_morse[:-1]
        pos_z_morse = self.z_morse.get_center()
        pos_se_morse = self.se_morse.get_center()
        self.play(
            Transform(self.z_letter, self.c_letter),
            FadeOut(self.z_morse[-1]),
            self.z_morse[:-1].move_to, pos_z_morse,
        )

        self.play(
            FadeOut(self.se_letter[1]),
            self.se_letter[0].move_to, self.se_letter.get_center(),
            FadeOut(self.se_morse[-1]),
            self.se_morse[:-1].move_to, pos_se_morse,
        )
        self.objects_group = VGroup(self.v_divider, self.z_letter,
                                    self.se_letter[0], self.z_morse,
                                    self.se_morse[:-1])

        self.play(
            self.objects_group.shift, 8 * UP,
            self.typewriter_obj.move_to, ORIGIN
        )
        ellipsises = VGroup(
            *[
                self.get_highlight_key(i)
                for i in "ce"
            ]
        )
        self.play(
            *[
                GrowFromCenter(i)
                for i in ellipsises
            ]
        )
        self.wait()
        self.play(
            *[
                ShrinkToCenter(i)
                for i in ellipsises
            ]
        )

        # self.play()


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
        self.questioning()

    def prepare(self):
        layout = QWERTY_LAYOUT
        self.keyboard = Keyboard(layout, background=False)

    def introduction(self):
        self.play(FadeInFrom(self.keyboard, 2 * DOWN))
        text = Text("The QWERTY Keyboard", **self.text_kwargs).scale(1.0)
        text.set_y(3.5)
        self.play(FadeInFrom(text, 2 * UP))
        # Qwerty name origin
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
        rect = Rectangle(width=row.get_width() + .1, height=row.get_height() + .1,
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

        # Show why it's named Home row
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
            "color": WHITE,  # It has to be "Invisible" at first
        }
    }

    def construct(self):
        self.prepare()
        self.add_screen()
        self.type_words(2)
        self.show_typing_complexity(2)

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
        # Move the screen away and s
        self.play(FadeOut(self.screen), FadeOut(self.texts_editor), FadeOut(self.editor))
        self.play(self.keyboard.shift, UP)
        self.cons_title = Text("Cons", **self.title_kwargs).scale(.8)
        self.cons_pos = self.screen.get_corner(UR)
        self.cons_title.move_to(self.cons_pos).shift(2 * RIGHT + .4 * DOWN)
        self.play(GrowFromCenter(self.cons_title))

        self.cons_list = ["Complicated finger\n motion", "One hand typing", "Jumping over the home row"]
        self.cons_obj = VGroup(*[Text("• " + i, **self.text_kwargs).scale(.6) for i in self.cons_list])
        self.cons_obj.arrange_submobjects(DOWN, True, True, aligned_edge=LEFT)
        self.cons_obj.next_to(self.cons_title, DOWN, buff=.4, aligned_edge=LEFT)

        self.words_list = self.words_list[:num_words]
        first_iteration = True
        cons_index = 0
        for i in range(len(self.words_list) - 1, -1, -1):
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
            if first_iteration:
                self.play(ShowIncreasingSubsets(self.cons_obj[cons_index]))
                cons_index += 1
                first_iteration = False
            else:
                self.play(ShowIncreasingSubsets(self.cons_obj[cons_index]))
                cons_index += 1


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
        self.ticks_texts = ["Now", "1970", "1930", "1868"]
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
        self.next_line = Line(ORIGIN, 6 * LEFT)
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



class MorseCode(MovingCameraScene):
    CONFIG = {
        "normal_text_kwargs": {
            "font": "Cairo Bold",
            "color": WHITE
        }
    }

    def construct(self):
        self.camera_frame = self.camera.frame
        self.camera_frame.save_state()
        self.morse = Text("Morse code", **self.normal_text_kwargs).set_y(0.0)
        self.morse.scale(1.5)
        dots = [Dot(color=WHITE) for i in range(6)]
        dashes = [
            Line(ORIGIN, .5 * RIGHT, stroke_width=8, color=WHITE)
            for i in range(3)
        ]
        sos = VGroup(*dots[0:3], *dashes, *dots[3:])
        sos.set_y(-2)
        self.play(ShowIncreasingSubsets(self.morse))
        sos.arrange(RIGHT, False, True, buff=.3)
        self.play(self.camera_frame.shift, 2 * DOWN)

        for i in sos:
            self.play(GrowFromPoint(i, i.get_edge_center(LEFT), run_time=.5))
        first_s_brace = Brace(sos[0:3])
        o_brace = Brace(sos[3:6])
        second_s_brace = Brace(sos[6:])
        o_brace.set_y(first_s_brace.get_y())

        self.play(
            self.camera_frame.set_width, 6,
        )
        self.play(
            FadeIn(first_s_brace),
            FadeIn(o_brace),
            FadeIn(second_s_brace),
        )
        s_letter1 = Text("S", font="Candara Bold", color="#e63946").scale(2)
        o_letter = Text("O", font="Candara Bold", color="#e63946").scale(2)
        s_letter2 = s_letter1.copy()
        s_letter1.next_to(first_s_brace, DOWN)
        o_letter.next_to(o_brace, DOWN)
        s_letter2.next_to(second_s_brace, DOWN)
        for i in [s_letter1, o_letter, s_letter2]:
            self.play(StretchFromSide(i, LEFT, run_time=.5))
            # self.play(Write(i))

        letters = VGroup(s_letter1, s_letter2, o_letter)
        braces = VGroup(first_s_brace, o_brace, second_s_brace)
        # sos.shift(2*UP)
        # letters.shift(2*UP)
        # braces.shift(2*UP)
        # self.morse.shift(2*UP)
        self.play(
            self.camera_frame.shift, UP,
            self.camera_frame.set_width, FRAME_WIDTH,
            self.camera_frame.set_height, FRAME_HEIGHT,
        )
        # self.play(Restore(self.camera_frame))




class DvorakScene(MovingCameraScene):
    CONFIG = {
        "text_kwargs": {
            "font": "SF Pro Display Semibold",
            "color": WHITE,
        },
    }

    def construct(self):
        self.prepare()
        self.questionning()
        self.dvorak_comes()

    def prepare(self):
        self.keyboard = Keyboard(QWERTY_LAYOUT, key_scale=.2, background=False).shift(DOWN)
        self.dvorak_guy = ImageMobject(ASSESTS_PATH + "dvorak.png").scale(1.5)
        self.thanos = ImageMobject(ASSESTS_PATH + "thanos.png")
        self.dvorak_guy.set_xy(4, -2)
        self.thanos.set_xy(2.6, -2.5)
        self.add(self.keyboard)
    def questionning(self):
        question = Text("But why the QWERTY stayed?", **self.text_kwargs).set_y(1)
        question_2 = Text("We don't use morse with computers, right?", **self.text_kwargs).set_y(1)
        self.play(ShowIncreasingSubsets(question))
        self.play(
            LaggedStart(
                FadeOutAndShift(question, UP),
                ShowIncreasingSubsets(question_2)
            )
        )
        self.play(
            FadeOut(question_2),
        )
        self.play(
            self.keyboard.shift, 2 * UP
        )


    def dvorak_comes(self):
        self.play(
            FadeIn(self.dvorak_guy)
        )
        self.play(
            FadeInFromDown(self.thanos)
        )
        animations_in = []
        animations_out = []
        for i in QWERTY_LAYOUT_CHANGING:
            keys = [self.keyboard.keys_dict[j] for j in i]
            for j in keys:
                anim_in, anim_out = get_fading_boxes_random(j, color="#181818", parts=16)
                animations_in.append(anim_in)
                animations_out.append(anim_out)

        self.play(*animations_in, run_time=1)
        self.wait()

        for i in self.keyboard.keys_dict.keys():
            key = self.keyboard.keys_dict[i]

            key.save_state()
            if i in ALPHABET:
                key.old_pos = key.get_center()

        self.keyboard.rearrange_keys_no_anim(QWERTY_LAYOUT_CHANGING,
                                             DVORAK_LAYOUT_CHANGING, self)
        self.play(*animations_out, run_time=1)
        self.wait()

class DvorakPerks(Scene):
    """
    In this part we will type a list of words and show that qwerty
    layout isn't that great
    """
    CONFIG = {
        "text_kwargs": {
            "font": "DINOT-Regular",
            "color": WHITE,
        },
        "title_kwargs": {
            "font": "SF Pro Display Bold",
            "color": "#F7D95B",
        },
        "editor_text_kwargs": {
            "font": "SF Pro Display Regular",
            "color": WHITE,  # It has to be "Invisible" at first
        },
        "red": "#EE243D",
        "cons_bg_kwargs": {
            "fill_color": "#51CFF4",
            "fill_opacity": 1,
            "stroke_width": 0,
            "height": FRAME_HEIGHT,
            "width": FRAME_WIDTH / 2.5,
        }
    }

    def construct(self):
        self.prepare()
        self.vowels_consonants()
        self.rows_used()
        #self.diagraphs()

    def prepare(self):
        self.keyboard = Keyboard(DVORAK_LAYOUT,
                                 key_scale=.3, background=False)
        self.add(self.keyboard)

    def vowels_consonants(self):
        """
        Vowels on the left and consonants of the left
        """
        vowels_text = Text("Vowels", **self.text_kwargs).set_xy(-2.5, 1.5)
        consonants_text = Text("Consonants", **self.text_kwargs).set_xy(2.5, 1.5)
        divider = Line(2 * UP, UP, color=GREY, stroke_width=2)
        vowels = "aoeui"
        consonants = "rstnlc"
        masks, temp = self.keyboard.color_word(vowels)
        self.play(
            FadeIn(masks),
        )
        self.play(ShowIncreasingSubsets(vowels_text))

        self.wait(.5)
        #self.play(FadeOut(masks), FadeOut)
        masks_2, temp = self.keyboard.color_word(consonants)
        self.play(FadeIn(masks_2))
        self.play(ShowIncreasingSubsets(consonants_text),
                  ShowCreation(divider))
        self.wait(.5)
        #ShowCreationThenDestructionAround
        self.play(
            LaggedStart(
                FadeOut(masks),
                FadeOut(masks_2),
                FadeOutAndShift(vowels_text, UP),
                FadeOutAndShift(consonants_text, UP),
                Uncreate(divider),
            )
        )

    def rows_used(self):
        masks, temp = self.keyboard.color_word("aoeuidhtns")
        most_text = Text("Most used row", **self.text_kwargs).set_y(1.5)
        least_text = Text("Least used row", **self.text_kwargs).set_y(1.5)
        most = most_text.get_sub_string("Most")
        rest_most = most_text.get_sub_string(" used row")
        least = least_text.get_sub_string("Least")
        self.play(ShowIncreasingSubsets(masks))

        most.set_fill(self.red)
        least.set_fill(self.red)
        self.play(
            ShowIncreasingSubsets(most_text),
        )
        self.wait()
        masks_2, temp = self.keyboard.color_word("qjkxbmwvz")

        self.play(
            LaggedStart(
                FadeOut(masks),
                ShowIncreasingSubsets(masks_2),
                AnimationGroup(
                    FadeOutAndShift(most, UP),
                    FadeInFrom(least, DOWN),
                    ApplyMethod(rest_most.shift, .1 * RIGHT),
                ),
            )
        )
        self.wait()
        self.play(FadeOut(masks_2))

    def diagraphs(self):
        diagraphs = "sh", "ch", "th", "wh"
        for i in diagraphs:
            masks, temp = self.keyboard.color_word(i)
            self.play(FadeIn(masks))
            self.wait(.5)
            self.play(FadeOut(masks))




class DvorakStats(MovingCameraScene):
    CONFIG = {
        "text_kwargs": {
            "font": "DINOT-Regular",
            "color": WHITE,
        },
        "website_kwargs": {
            "font": "SF Pro Display Semibold",
            "color": RED,
        },
        "num_kwargs": {
            "font": "Agency FB",
            "color": GREY
        },
        "sum_kwargs": {
            "font": "Agency FB",
            "color": RED
        },
        "text_kwargs_grey": {
            "font": "DINOT-Regular",
            "color": GREY,
        },

    }

    def construct(self):
        self.prepare()
        #self.show_website()
        #self.show_stats_distance()
        self.row_usage()
        #self.finger_usage()

    def prepare(self):
        self.camera_frame = self.camera.frame
        self.website = ImageMobject(ASSESTS_PATH + "website.png").scale(3)
        self.website_rect = SurroundingRectangle(
            self.website,
            color=BLUE,
            stroke_width=3,
            buff=0.03
        )
        self.website_address = Text("http://patorjk.com/keyboard-layout-analyzer",
                                    **self.website_kwargs).scale(.4)
        self.website_address.next_to(
            self.website_rect,
            DOWN,
            aligned_edge=RIGHT,
            buff=.1
        )
        self.wb_adrees_line = Line(stroke_width=2)
        self.wb_adrees_line.match_width(self.website_address)
        self.wb_adrees_line.next_to(self.website_address, DOWN, buff=.1)

    def show_website(self):
        self.play(ShowCreation(self.website_rect))
        self.play(GrowFromCenter(self.website))
        self.play(
            LaggedStart(
                ShowIncreasingSubsets(self.website_address),
                ShowCreation(self.wb_adrees_line)
            )
        )
        self.wait(4)
        self.clear()

    def show_stats_distance(self):
        title = Text("Distance", **self.text_kwargs).scale(1.5)
        title.set_y(3.5)
        table = VGroup()
        rows = 2
        columns = 12
        data = 10
        table_start_x = -6
        table_start_y = 1
        fingers = ["Pinky", "Ring", "Middle", "Index", "Thumb"]
        left_fingers = ["Left\n" + i for i in fingers]
        right_fingers = ["Right\n" + i for i in fingers]

        l_fingers_obj = VGroup(
            *[Text(i, **self.text_kwargs).scale(.5) for i in left_fingers]
        )

        r_fingers_obj = VGroup(
            *[Text(i, **self.text_kwargs).scale(.5) for i in right_fingers]
        )

        row_qwerty_title = Text("QWERTY", **self.text_kwargs).scale(.6)
        row_dvorak_title = Text("DVORAK", **self.text_kwargs).scale(.6)
        row_qwerty_title.set_xy(table_start_x, table_start_y)
        row_dvorak_title.next_to(row_qwerty_title, DOWN, buff=.5)
        qwerty_stats = VGroup(*
                              [Text("{:.2f}".format(i), **self.num_kwargs).scale(.6)
                               for i in QWERTY_DISTANCES[:-1]]
                              )
        dvorak_stats = VGroup(*
                              [Text("{:.2f}".format(i), **self.num_kwargs).scale(.6)
                               for i in DVORAK_DISTANCES[:-1]]
                              )
        qwerty_stats.arrange_submobjects(RIGHT, False, False, buff=.5)
        qwerty_stats.next_to(row_qwerty_title, RIGHT)
        y_titles_fingers = dvorak_stats.get_y() + 1.8
        for i in range(len(dvorak_stats)):
            dvorak_stats[i].next_to(qwerty_stats[i], DOWN, buff=.5)
            if i < 5:
                l_fingers_obj[i].set_xy(qwerty_stats[i].get_x(), y_titles_fingers)
            else:
                r_fingers_obj[i-5].set_xy(qwerty_stats[i].get_x(), y_titles_fingers)
        row_dvorak_title.set_y(dvorak_stats.get_y())
        sum_qwerty = Text(str(QWERTY_DISTANCES[-1]), **self.sum_kwargs).scale(.6)
        sum_dvorak = Text(str(DVORAK_DISTANCES[-1]), **self.sum_kwargs).scale(.6)
        sum_title = Text("Total", **self.text_kwargs).scale(.6)
        sum_qwerty.next_to(dvorak_stats[-1], RIGHT)
        sum_dvorak.next_to(qwerty_stats[-1], RIGHT)
        sum_title.next_to(r_fingers_obj[-1], RIGHT, buff=.2)

        lines_start_x = row_qwerty_title.get_edge_center(LEFT)[0]
        lines_end_x = sum_qwerty.get_edge_center(RIGHT)[0]
        line_1_y = row_qwerty_title.get_y() + .3
        line_1_start = np.array([lines_start_x, line_1_y, 0])
        line_1_end = np.array([lines_end_x, line_1_y, 0])

        line_1 = Line(line_1_start,
                      line_1_end,
                      stroke_width=2,
                      color=GREY
                      )
        line_2 = line_1.copy()
        line_2.set_y(row_dvorak_title.get_y() + .3)


        self.play(ShowIncreasingSubsets(title))

        self.play(
            FadeIn(row_qwerty_title),
            FadeIn(row_dvorak_title),
            run_time=.5,
        )
        self.play(
            ShowCreation(line_1),
            ShowCreation(line_2),
            run_time=.5,
        )
        self.play(
            LaggedStart(
            FadeIn(qwerty_stats),
            FadeIn(dvorak_stats),
            FadeIn(l_fingers_obj),
            FadeIn(r_fingers_obj),
            FadeIn(sum_qwerty),
            FadeIn(sum_dvorak),
            FadeIn(sum_title),
            lag_ratio=.4
            )
        )
        rect_sum_qwerty = SurroundingRectangle(sum_qwerty, color=GREEN)
        rect_sum_dvorak = SurroundingRectangle(sum_dvorak, color=GREEN)
        self.play(ShowCreation(rect_sum_qwerty))
        self.play(Transform(rect_sum_qwerty, rect_sum_dvorak))
        self.wait(2)

        self.play(
            LaggedStart(
                FadeOut(qwerty_stats),
                FadeOut(dvorak_stats),
                FadeOut(l_fingers_obj),
                FadeOut(r_fingers_obj),
                FadeOut(sum_qwerty),
                FadeOut(sum_dvorak),
                FadeOut(sum_title),
                FadeOut(line_1),
                FadeOut(line_2),
                FadeOut(row_qwerty_title),
                FadeOut(row_dvorak_title),
                FadeOut(rect_sum_qwerty),
                FadeOut(rect_sum_dvorak),
                lag_ratio=.4
            )
        )

        self.play(FadeOutAndShift(title, UP))

    def row_usage(self):
        title = Text("Row Usage", **self.text_kwargs).scale(1.3)
        title.set_y(3.5)
        line = Line(color=GREY)
        line.match_width(title)
        line.next_to(title, DOWN, buff=.1)

        self.play(
            FadeInFrom(title, UP),
            ShowCreation(line)
        )

        qwerty_perc = [i/100 for i in QWERTY_ROW_USAGE]
        dvorak_perc = [i/100 for i in DVORAK_ROW_USAGE]
        colors = ["#d62828", "#f77f00", "#fcbf49", "#eae2b7"]
        chart_key = VGroup(
            *[Square(
            side_length=.4,
            fill_color=i,
            fill_opacity=1,
            stroke_width=1,
            )
            for i in colors])
        rows = ["Top Row", "Home Row", "Bottom Row", "Spacebar Row"]
        rows_obj = [Text(i, **self.text_kwargs).scale(.5) for i in rows]

        chart_key.arrange_submobjects(RIGHT, True, True, buff=1.6)
        chart_key.set_y(-3.2)
        chart_key.shift(0.0 * RIGHT)
        for i in enumerate(rows_obj):
            i[1].next_to(chart_key[i[0]], DOWN, buff=.1)


        x = 3
        qwerty_pie = PieChart(
            percentages=qwerty_perc,
            x=-x,
            colors=colors
        )

        dvorak_pie = PieChart(
            percentages=dvorak_perc,
            x=x,
            colors=colors
        )
        qwerty_title = Text("QWERTY", **self.text_kwargs).scale(.8)
        dvorak_title = Text("DVORAK", **self.text_kwargs).scale(.8)
        qwerty_title.set_xy(-x, 2.5)
        dvorak_title.set_xy(x, 2.5)

        self.add(qwerty_pie, dvorak_pie)
        animations = qwerty_pie.animate()
        animations_2 = dvorak_pie.animate()
        squares = iter(chart_key)
        legends = iter(rows_obj)
        self.play(ShowIncreasingSubsets(qwerty_title))
        self.play(ShowIncreasingSubsets(dvorak_title))
        for i in range(len(animations)):
            self.play(
                animations[i],
                animations_2[i],
                ShowCreation(next(squares)),
                FadeIn(next(legends)),
                run_time=1
            )
            self.wait(.1)
        self.play(dvorak_pie.slice_slide(1))
        self.play(qwerty_pie.slice_slide(0))

        self.wait()


    def finger_usage(self):
        title = Text("Finger Usage", **self.text_kwargs).scale(1.3)
        title.set_y(3.5)
        line = Line()
        line.match_width(title)
        line.next_to(title, DOWN, buff=.1)

        self.play(
            FadeInFrom(title, UP),
            ShowCreation(line)
        )

        self.bar_plot = BarChart(QWERTY_FINGERS, max_value=max(QWERTY_FINGERS) + 50,
                                bar_fill_opacity=1, height=4)
        self.bar_plot_2 = BarChart(DVORAK_FINGERS, max_value=max(QWERTY_FINGERS) + 50,
                                 bar_fill_opacity=1, height=4, bar_colors=BLUE)
        self.bar_plot_2.set_x(-.3)
        colors = ["#e63946", BLUE]
        plot_key = [Square(fill_color=i, fill_opacity=1).scale(.2)
                    for i in colors
                    ]
        plot_key = VGroup(*plot_key)
        plot_key.arrange(DOWN, False, False)
        plot_key.next_to(self.bar_plot, RIGHT)
        legends = [Text(i, **self.text_kwargs).scale(.6) for i in ("QWERTY", "DVORAK")]
        for i, legend in enumerate(legends):
            legend.next_to(plot_key[i], RIGHT)


        bars_group = [VGroup(i, j) for i,j in zip(self.bar_plot.bars, self.bar_plot_2.bars)]

        fingers = ["Pinky", "Ring", "Middle", "Index", "Thumb"]
        l_fingers = ["Left\n" + i for i in fingers]
        fingers.reverse()
        r_fingers = ["Right\n" + i for i in fingers]
        fingers_obj = [Text(i, **self.text_kwargs_grey).scale(.5) for i in l_fingers+r_fingers]

        for index, finger in enumerate(fingers_obj):
            finger.next_to(bars_group[index], DOWN)

        fingers_obj = VGroup(*fingers_obj)

        self.play(ShowCreation(self.bar_plot.x_axis))
        self.play(ShowIncreasingSubsets(fingers_obj))
        self.play(ShowCreation(self.bar_plot.y_axis))
        self.play(
            LaggedStart(
                *[
                    StretchFromSide(i, DOWN)
                    for i in self.bar_plot.bars
                ]
            ),
            ShowIncreasingSubsets(self.bar_plot.y_axis_labels),
            LaggedStart(
                GrowFromCenter(plot_key[0]),
                ShowIncreasingSubsets(legends[0])
            )
        )

        self.play(
            LaggedStart(
                *[
                    StretchFromSide(i, DOWN)
                    for i in self.bar_plot_2.bars
                ]
            ),
            LaggedStart(
                GrowFromCenter(plot_key[1]),
                ShowIncreasingSubsets(legends[1])
            )
        )

