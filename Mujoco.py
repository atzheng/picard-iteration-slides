from manim_templates import *
from manim import *
import funcy as f

class Mujoco(BaseSlide):
    def construct(self):
        self.setup_slide(title="Beyond the Theory: General Dynamical Systems")

        text = LatexItems(
            r"\item {\bf Environment}: Mujoco, a simple robotic locomotion benchmark",
            r"\item {\bf Parallelization}: Each process responsible for one timestep",
            r"\item {\bf Initialization}: Initialize trajectory from previous policy iterate"
        ).to_edge(LEFT)

        mujoco = ImageMobject("mujoco.png").scale(0.6).to_edge(RIGHT)

        self.play_animations(
            [
                FadeIn(mujoco),
                *map(FadeIn, text)
            ]
        )
