from manim import *
from manim_templates import *
from manim import *
import funcy as f


class MainResultICML(BaseSlide):
    def construct(self):
        self.setup_slide(title="Main Result (Informal)")

        # Theorem
        theorem = ParTex(
            r"\textbf{Theorem} \\"
            r"For a ``general'' class of policies, Picard iteration converges "
            r"in at most $J + 1$ iterations on the fulfillment optimization problem.",
            width=0.7,
        )

        # Consequence
        consequence = ParTex(
            r"\textbf{Consequence:} \quad "
            r"With $N$ processes, Picard Iteration speeds up policy evaluation by a factor $N / J$.",
            width=0.7,
        )

        # Box around theorem and consequence
        box_content = VGroup(theorem).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        box = SurroundingRectangle(
            box_content, color=GRAY, fill_color=GRAY, fill_opacity=0.2, buff=0.3, stroke_width=1
        )
        theorem_block = VGroup(box_content, box)

        # # Proof intro
        # intro = Tex(
        #     r"We will prove a special case: infinite inventory, and greedy policy:",
        # )

        # # Policy definition
        # policy = MathTex(
        #     r"\pi(s_t, \omega_t) = \arg\min_{j \in [J]} c_j(\omega_t) \quad \text{s.t.} \quad C_j > 0",
        # )

        # Arrange all together
        content = (
            VGroup(theorem_block, consequence)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(self.title, DOWN, buff=0.5, aligned_edge=LEFT)
        )
        theorem_block.set_x(0)
        # policy.set_x(0)
        self.play_animations(f.lmap(FadeIn, content))
