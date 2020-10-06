from manimlib.imports import *
import os

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
