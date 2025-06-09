from manim_templates import *
from manim import *
import funcy as f

class PolicyOpt(BaseSlide):
    def construct(self):
        self.setup_slide(title="Policy Optimization")
        title = Tex(r"Policy opt. with 1,000 policy gradient steps, varying problem size:")
        title.next_to(self.title, DOWN, aligned_edge=LEFT, buff=0.5)

        # Table header and data
        table = MathTable(
            [
                [r"\textbf{Problem Scale}", r"\textbf{Runtime}", r"\textbf{Runtime}"],
                [r"\# \text{orders} / \# \text{products}", r"\text{(Sequential)}", r"\text{(Picard)}"],
                [r"3{,}000 / 1{,}000", r"1\text{m}32\text{s}", r"59\text{s}"],
                [r"30{,}000 / 10{,}000", r"6\text{m}55\text{s}", r"1\text{m}01\text{s}"],
                [r"300{,}000 / 100{,}000", r"1\text{h}04\text{m}", r"1\text{m}04\text{s}"],
                [r"3{,}000{,}000 / 1{,}000{,}000", r"10\text{h}02\text{m}", r"1\text{m}39\text{s}"],
                [r"30{,}000{,}000 / 10{,}000{,}000", r"4 \text{days (est.)}", r"4\text{m}57\text{s}"],
            ],
            include_outer_lines=True,
            h_buff=1.6,
            v_buff=0.3
        ).next_to(title, DOWN, buff=0.5).set_x(0)


        self.play_animations(
            [
                FadeIn(title),
                *map(FadeIn, table.get_rows())
            ]
        )
