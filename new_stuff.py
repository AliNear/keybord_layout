from manimlib.imports import *
import os

from random import shuffle

ASSESTS_PATH = os.getcwd() + "/projects/keyboard_layout/assets/"

class AnotherTest(Scene):
    
    def construct(self):
        s = self.get_sound_wave()
        self.play(ShowCreation(s))
        img = ImageMobject(ASSESTS_PATH + "vintage.jpg").scale(2)
        animation = self.image_reveal_animation(img)
        self.play(animation)
        
    def get_sound_wave(self):
        sound = VGroup(*[
            Line(DOWN, UP).set_height(
                (0.3 + 0.8 * random.random()) * abs(np.sin(x))
            )
            for x in np.linspace(0, 3 * PI, 100)
        ])
        sound.arrange(RIGHT, buff=0.05)
        return sound
        
    def image_reveal_animation(self, image, bit_height=0.1):
        box = SurroundingRectangle(image)
        box.set_fill(BLACK, 1)
        box.set_stroke(width=0)
        bits = self.get_image_bits(image, bit_height=bit_height)

        return AnimationGroup(
            Animation(image),
            ApplyMethod(
                box.stretch, 0, 1, {"about_edge": DOWN}, remover=True,
                rate_func=linear,
            ),
            LaggedStartMap(
                VFadeInThenOut, bits,
                run_time=1,
                lag_ratio=3 / len(bits)
            )
        )
        
    def get_bit_grid(self, n_rows, n_cols, bits=None, buff=MED_SMALL_BUFF, height=4):
        bit_pair = VGroup(Text("0").scale(.3), Text("1").scale(.3))
        bit_mobs = VGroup(*[
            bit_pair.copy()
            for x in range(n_rows * n_cols)
        ])
        bit_mobs.arrange_in_grid(n_rows, n_cols, buff=buff)
        bit_mobs.set_height(height)
        if bits is None:
            bits = np.random.randint(0, 2, len(bit_mobs))

        for bit_mob, bit in zip(bit_mobs, bits):
            bit_mob[1 - bit].set_opacity(0)

        bit_mobs.n_rows = n_rows
        bit_mobs.n_cols = n_cols
        return bit_mobs
       
    def get_image_bits(self, image, bit_height=0.15, buff=MED_SMALL_BUFF):
        bit = Text("0").scale(.3)
        small_buff = (buff / bit.get_height()) * bit_height
        bit.set_height(bit_height)
        bits = self.get_bit_grid(
            n_rows=int(image.get_height() / (bit.get_height() + small_buff)),
            n_cols=int(image.get_width() / (bit.get_width() + small_buff)),
            buff=buff
        )
        bits.replace(image)
        return bits

class Test(Scene):
    def construct(self):
        rect = Rectangle(fill_opacity=1, fill_color=GREEN)
        c = Circle(fill_opacity=1, fill_color=BLUE)
        self.play(ShowCreation(c))
        self.play(ShowCreation(rect))
        self.wait()

class CoolImageAnim(Scene):

    def construct(self):
        img = ImageMobject(ASSESTS_PATH + "vintage.jpg")
        width = img.get_width()
        height = img.get_height()
        parts = 64
        w4 = width/parts
        h4 = height/parts
        boxes = VGroup(*[
            Rectangle(
                width=w4,
                height=h4,
                fill_opacity=1,
                fill_color=BLACK,
                stroke_width=0
            )
            for i in range(parts * parts)
        ])
        boxes.arrange_in_grid(n_rows=parts,n_cols=parts, buff=0)
        self.add(img)
        self.add(boxes)
        boxes.move_to(img)
        bb = [i for i in boxes]
        shuffle(bb)
        animations = []
        for i in bb:
            animations.append(FadeOut(i))
        self.play(
            LaggedStart(*animations),
            run_time=3
        )
        self.wait()

class ThanosAnim(Scene):

    def construct(self):
        img = ImageMobject(ASSESTS_PATH + "normal_keys/a.png")
        width = img.get_width()
        height = img.get_height()
        parts = 24
        w4 = width/parts
        h4 = height/parts
        boxes = VGroup(*[
            Rectangle(
                width=w4,
                height=h4,
                fill_opacity=1,
                fill_color=BLACK,
                stroke_width=0
            )
            for i in range(parts * parts)
        ])
        boxes.arrange_in_grid(n_rows=parts,n_cols=parts, buff=0)
        self.add(img)
        #self.add(boxes)
        boxes.move_to(img)
        animations = []
        s = 0
        for i in range(parts):
            b = boxes[s:s+parts]
            b_odd = [b[j] for j in range(len(b)) if j%2 != 0]
            b_even = [b[j] for j in range(len(b)) if j%2 == 0]
            shuffle(b_odd)
            shuffle(b_even)
            an = LaggedStart(
                LaggedStart(*[FadeIn(j) for j in b_odd]),
                LaggedStart(*[FadeIn(j) for j in b_even]),
                run_time=.5
            )
            animations.append(
                an
            )
            s += parts
        self.play(
            LaggedStart(*animations, lag_ratio=1),
            run_time=1
        )
        self.wait()


def get_fading_boxes(img, color=BLACK, parts=16):
    width = img.get_width()
    height = img.get_height()
    w4 = width/parts
    h4 = height/parts
    boxes = VGroup(*[
        Rectangle(
            width=1.4 * w4,
            height=1.4 * h4,
            fill_opacity=1,
            fill_color=color,
            stroke_width=w4/4,
            color=BLACK
        )
        for i in range(parts * parts)
    ])
    boxes.arrange_in_grid(n_rows=parts,n_cols=parts, buff=-0.008)
        #self.add(boxes)
    boxes.move_to(img)
    animations_in = []
    animations_out = []
    s = 0
    for i in range(parts):
        b = boxes[s:s+parts]
        b_odd = [b[j] for j in range(len(b)) if j%2 != 0]
        b_even = [b[j] for j in range(len(b)) if j%2 == 0]
        shuffle(b_odd)
        shuffle(b_even)
        an_in = LaggedStart(
            LaggedStart(*[FadeIn(j) for j in b_odd]),
            LaggedStart(*[FadeIn(j) for j in b_even]),
            run_time=.5
        )
        animations_in.append(
            an_in
        )
        an_out = LaggedStart(
            LaggedStart(*[FadeOut(j) for j in b_odd]),
            LaggedStart(*[FadeOut(j) for j in b_even]),
            run_time=.5
        )
        animations_out.append(
            an_out
        )

        s += parts
    shuffle(animations_in)
    shuffle(animations_out)
    return LaggedStart(*animations_in, lag_ratio=.7), LaggedStart(*animations_out, lag_ratio=.7)

def get_fading_boxes_random(img, color=BLACK, parts=16):
    width = img.get_width()
    height = img.get_height()
    w4 = width/parts
    h4 = height/parts
    boxes = VGroup(*[
        Rectangle(
            width=1.4 * w4,
            height=1.4 * h4,
            fill_opacity=1,
            fill_color=color,
            stroke_width=w4/4,
            color=BLACK
        )
        for i in range(parts * parts)
    ])
    boxes.arrange_in_grid(n_rows=parts,n_cols=parts, buff=-0.008)
    boxes.move_to(img)
    boxes_list = list(boxes)
    shuffle(boxes_list)
    animations_in = []
    animations_out = []

    for i in boxes_list:
        an_in = FadeIn(i)
        animations_in.append(an_in)
        an_out = FadeOut(i)
        animations_out.append(an_out)

#    shuffle(animations_in)
#    shuffle(animations_out)
    return LaggedStart(*animations_in, lag_ratio=.3), LaggedStart(*animations_out, lag_ratio=.3)

