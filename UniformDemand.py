from manim_templates import *
from manim import *
import funcy as f


class UniformDemand(BaseSlide):
    def construct(self):
        self.setup_slide(title="Speeding Up a Single Policy Evaluation")
        text = Tex("Demand distributed uniformly over products").next_to(
            self.title, DOWN, aligned_edge=LEFT, buff=0.3
        )
        uniform = ImageMobject("uniform.png").next_to(text, DOWN, buff=0.5).set_x(0)

        self.play_animations(
            [
                FadeIn(text),
                FadeIn(uniform),
            ]
        )
