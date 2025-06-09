from manim_templates import *
from manim import *
import funcy as f


class HeavyTailedDemand(BaseSlide):
    def construct(self):
        self.setup_slide(title="Policy Evaluation with Heavy-Tailed Demand")

        distrs = (
            ImageMobject("demand-distributions.png").scale(0.6).to_edge(LEFT)
        )
        distrs.add(
            Tex(r"Demand(i) $\propto i^\beta$").next_to(distrs, UP, buff=0.3)
        )

        ann = ParTex(
            r"""
        Uniform: $\beta = 0$ \\
        Typical: $\beta \approx -0.7$
        """
        ).next_to(distrs, DOWN, buff=0.5)

        prod = ImageMobject("product-split.png").scale(0.6).to_edge(RIGHT)
        prod.add(
            Tex(r"Speedup vs. $\beta$")
            .next_to(prod, UP, buff=0.3)
            .set_y(distrs[-1].get_y())
        )

        pop = (
            Tex(r"Processors allocated \\ {\bf by product}", font_size=28)
            .set_color(RED_D)
            .move_to((2, 0, 1))
            .set_z_index(1)
        )
        pot = (
            Tex(r"Processors allocated \\ {\bf randomly}", font_size=28)
            .set_color(BLUE_D)
            .move_to((5, 2, 1))
            .set_z_index(1)
        )

        prod_unif = (
            ImageMobject("product-and-uniform-split.png")
            .scale(0.6)
            .move_to(prod[0])
            .shift(0.1 * DOWN)
        )

        self.play_animations(
            [
                FadeIn(distrs),
                FadeIn(ann),
                FadeIn(prod),
                FadeIn(pop),
                AnimationGroup(
                    FadeIn(prod_unif),
                    FadeIn(pot),
                ),
            ]
        )
