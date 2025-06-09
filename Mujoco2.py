from manim_templates import *
from manim import *
import funcy as f


class Mujoco2(BaseSlide):
    def construct(self):
        self.setup_slide(title="Beyond the Theory: General Dynamical Systems")
        text = Tex(
            r"{\bf Results}: Within 15 iters, RMSE of state vectors is < 0.1 \% (T=200)"
        ).next_to(self.title, DOWN, aligned_edge=LEFT, buff=0.3)

        mujoco = (
            ImageMobject("mujoco-results.png")
            .scale(0.8)
            .next_to(text, DOWN, buff=0.3)
            .set_x(0)
        )

        self.play_animations(
            [
                FadeIn(text),
                FadeIn(mujoco),
            ]
        )
