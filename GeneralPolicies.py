from manim_templates import *
from manim import *
import funcy as f


class GeneralPolicies(BaseSlide):
    def construct(self):
        self.setup_slide(title="Requirements for More General FO Policies")

        text = LatexItems(
            r"\item {\bf Independence of Irrelevant Inventory}: Decisions for a given product only depend on inventory for that product ",
            r"\item {\bf Locality}: Changing state at some node will either not change the decision, or else switch fulfillment to that node",
            r"\item {\bf Monotonicity}: Increasing inventory at a node will not change fulfillment away from that node",
            r"\item {\bf Capacity Dependence}: Decisions depend on capacity only via the {\it set} of nodes with exhausted capacity.",
            page_width=r"\textwidth",
            font_size=36,
        ).next_to(self.title, DOWN, aligned_edge=LEFT, buff=0.3)

        thm = (
            ParTex(
                r"""
        {\bf Theorem}: For any policy satisfying these properties,
        Picard Iteration converges in at most $J + 1$ iterations.
        """,
                width=0.7,
            )
            .add_background_rectangle(color=GRAY, buff=0.4, opacity=0.3)
            .to_edge(DOWN)
        )

        self.play_animations(
            [
                *map(FadeIn, text),
                FadeIn(thm),
            ]
        )
