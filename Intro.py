from manim_templates import *
from manim import *
import funcy as f


class Intro(BaseSlide):
    def construct(self):
        self.setup_slide(
            title="Policy Evaluation is RL's Computational Bottleneck"
        )

        items = LatexItems(
            r"\item Start with a candidate policy (e.g., neural network)",
            r"\item {\bf Policy Evaluation}: Simulate policy performance on historical data",
            r"\item Compute a gradient wrt policy parameters",
            r"\item Update policy, repeat",
            itemize="enumerate",
            page_width=r"0.6\textwidth",
        )

        text = (
            VGroup(
                ParTex(
                    r"Reinforcement learning is SotA for many operations problems: inventory, queueing control, ridesharing dispatch, etc",
                    width=0.9,
                ),
                Tex(r"The basic policy optimization approach:"),
                items,
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        anntime = ParTex(
            r"""
        Medium-sized retailer, 1 month of data: \\
        10M policy evaluations (orders), takes 3 hrs
        """,
            width=0.4,
            font_size=30
        ).next_to(items[1], RIGHT).to_edge(RIGHT)
        time_arrow = Arrow(anntime.get_left(), items[1].get_right())
        anntime.add(time_arrow)


        anniters = ParTex(
            r"""
            Need 100s-1000s of loops
            """,
            width=0.4,
            font_size=30
        ).next_to(items[3], RIGHT, buff=2)
        iterarrow = Arrow(anniters.get_left(), items[3].get_right())
        anniters.add(iterarrow)


        self.play_animations(
            [
                FadeIn(text[0]),
                FadeIn(text[1]),
                *map(FadeIn, text[2]),
                FadeIn(anntime),
                FadeIn(anniters),
            ]
        )
