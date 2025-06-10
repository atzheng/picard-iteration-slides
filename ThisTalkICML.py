from manim_templates import *
from manim import *
import funcy as f


class ThisTalkICML(BaseSlide):
    def construct(self):
        self.setup_slide(title="Speeding up Policy Evaluation in Supply Chain RL")

        text = (
            VGroup(
                ParTex(
                    r"{\bf The Problem:} RL is often bottlenecked by policy evaluation, particularly in long-horizon problems",
                    width=0.9,
                ),
                ParTex(
                    r"{\bf The Solution:} Parallelize policy evaluation with {\bf Picard Iteration} ",
                    width=0.9,
                ),
                LatexItems(
                    r"\item Provably speeds up evaluation in supply chain problems",
                    r"\item 500x speedup (vs. sequential evaluation) when implemented on GPU",
                    r"\item Experiments show significant speedups possible in other environments",
                    page_width=r"0.9\textwidth"
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        self.play_animations(
            [FadeIn(text[0]), FadeIn(text[1]), *map(FadeIn, text[2])]
        )
