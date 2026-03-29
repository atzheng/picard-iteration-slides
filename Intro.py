from manim_templates import *
from manim import *
import funcy as f


class Intro(BaseSlide):
    def construct(self):
        self.setup_slide(
            title="Policy Simulation is RL's Computational Bottleneck"
        )

        text = TexBox(
            r"""
            Reinforcement learning is SotA for many operations problems: inventory, queueing control, ridesharing dispatch, etc
            The basic policy optimization approach:
            1. Start with a candidate policy (e.g., neural network)
            2. {\bf Simulate policy} on historical data
            3. Compute a gradient of performance wrt policy parameters
            4. Update policy, repeat
            """,
            width=10,
        ).next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)

        deep = (
            ImageMobject("deep-inventory.png")
            .scale_to_fit_height(3)
            .to_corner(DOWN + RIGHT)
        )
        # text[0]: RL intro, text[1]: "basic approach:", text[2-5]: items 1-4
        anntime = (
            TexBox(
                r"""
        Medium-sized retailer, 1 month of data: \\
        10M policy evaluations (orders), takes 3 hrs
        """,
                width=3,
                height=2,
            )
            .next_to(text[3], RIGHT)
            .to_edge(RIGHT)
        )
        time_arrow = Arrow(anntime.get_left(), text[3].get_right())
        anntime.add(time_arrow)

        anniters = TexBox(
            r"""
            Need 100s-1000s of loops
            """,
            font_size=30,
        ).next_to(text[5], RIGHT, buff=2)
        iterarrow = Arrow(anniters.get_left(), text[5].get_right())
        anniters.add(iterarrow)

        self.play_animations(
            [
                FadeIn(text[0]),
                FadeIn(deep),
                FadeIn(text[1]),
                *map(FadeIn, text[2:]),
                FadeIn(anntime),
                FadeIn(anniters),
            ]
        )
