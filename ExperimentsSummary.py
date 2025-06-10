from manim_templates import *
from manim import *
import funcy as f

class ExperimentsSummary(BaseSlide):
    def construct(self):
        self.setup_slide(title="Summary of Numerical Results")
        its = LatexItems(
            r"\item Implemented in JAX, experiments on one A100",
            r"\item For fulfillment optimization: speeds up single policy evaluation 500x",
            r"\item In policy optimization loop, cuts days to minutes",
            r"\item Converges in a small number of iterations on MuJoCo",
            page_width=r"0.9\textwidth"
        )

        self.play_animations(
            [
                *map(FadeIn, its)
            ]
        )
