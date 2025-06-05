from manim_templates import *
from manim import *
import funcy as f

class Title(BaseSlide):
    def construct(self):
        self.setup_slide()
        self.wait(0.1)
        title = Tex(r"""
        Speeding Up Policy Simulation in Supply Chain RL
        """, font_size=55, color=BLACK)
        author = Tex(r"""
        Vivek Farias, Aryan Khojandi (MIT) \\
        Joren Gijsbrechts (ESADE)  \\
        Tianyi Peng (Columbia) \\
        Andy Zheng (UBC)
        """, font_size=35, color=BLACK).next_to(title, 2 * DOWN )
        self.play_animations(
            [FadeIn(title), FadeIn(author),]
        )
