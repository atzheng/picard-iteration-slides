from manim_templates import *
from manim import *
import funcy as f


class UniformDemand(BaseSlide):
    def construct(self):
        self.setup_slide(title="Speeding Up a Single Policy Evaluation")
        text = Tex("Demand distributed uniformly over products").next_to(
            self.title, DOWN, aligned_edge=LEFT, buff=0.3
        )
        uniform = (
            ImageMobject("uniform.png").next_to(text, DOWN, buff=0.5).set_x(0)
        )

        TW = Dot((3.9, -1.5, 0), color=RED_E)
        TW_label = Tex("Time Warp (5x)").next_to(TW, RIGHT, buff=0.1).set_color(RED_E)

        self.play_animations(
            [
                FadeIn(text),
                FadeIn(uniform),
                FadeIn(TW, TW_label),
            ]
        )
