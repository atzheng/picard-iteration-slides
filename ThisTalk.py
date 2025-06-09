from manim_templates import *
from manim import *
import funcy as f


class ThisTalk(BaseSlide):
    def construct(self):
        self.setup_slide(title="Solving the Bottleneck")

        text = (
            VGroup(
                ParTex(
                    r"{\bf The Problem:} How to speed up repeated evaluations of an expensive policy?",
                    width=0.9,
                ),
                Tex(r"This Talk:"),
                LatexItems(
                    r"\item Picard Iteration: an algorithm for parallelizing policy evaluation",
                    r"\item Provably speeds up evaluation in non-trivial problems",
                    r"\item 500x speedup when implemented on GPU",
                    page_width=r"0.9\textwidth"
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        self.play_animations(
            [FadeIn(text[0]), FadeIn(text[1]), *map(FadeIn, text[2])]
        )
