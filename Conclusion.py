from manim_templates import *
from manim import *
import funcy as f

class Conclusion(BaseSlide):
    def construct(self):
        self.setup_slide(title="Conclusion")

        text = (
            VGroup(
                ParTex("Picard iteration enables GPU-accelerated, parallel policy evaluation", width=0.9),
                Tex("Future directions:"),
                LatexItems(
                    r"\item Many other problem classes: inventory, ridesharing, continuous control",
                    r"\item Speed / accuracy tradeoffs in policy optimization",
                    r"\item Parallelizing the whole computation graph: over time and over policy iterations",
                    page_width=r"0.9\textwidth"
                ),
                Tex("Thank you!")
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)
        )



        self.play_animations(
            [
                FadeIn(text[0]),
                FadeIn(text[1]),
                *map(FadeIn, text[2]),
                FadeIn(text[3]),
            ]
        )
