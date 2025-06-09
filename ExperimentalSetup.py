from manim_templates import *
from manim import *
import funcy as f

class ExperimentalSetup(BaseSlide):
    def construct(self):
        self.setup_slide(title="Experimental Setup")

        text = (
            VGroup(
                Tex(r"{\bf Environment}: Moderately large-scale fulfillment network"),
                LatexItems(
                    r"\item 30 Nodes (near 30 most populous metros)",
                    r"\item Capacity, Inventory pro-rata to population",
                    r"\item Load factor of 1.25 (Hard)",
                    r"\item Up to 1M SKUs, varying demand distribution",
                    r"\item 3M orders, location pro-rata to population",
                    page_width=r"\textwidth",
                ),
                Tex(r"{\bf Policy}: simple two-layer MLP ($\sim$10K params)"),
                Tex(r"{\bf Implementation}: Implemented in JAX, run on single A100 GPU"),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            .next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        self.play_animations(
            [
                FadeIn(text[0]),
                *map(FadeIn, text[1]),
                *map(FadeIn, text[2:]),
            ]
        )
