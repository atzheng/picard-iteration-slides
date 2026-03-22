#!/usr/bin/env python3

from manim_templates import *
from manim import *
import funcy as f

HIGHLIGHT = 0  # 0-indexed

ITEMS = [
    r"1. The challenge of policy simulation",
    r"2. Our method: Picard Iteration",
    r"3. Convergence of Picard Iteration",
    r"4. Numerical Results",
    r"5. Beyond Policy Simulation",
]


class Agenda1(BaseSlide):
    def construct(self):
        self.setup_slide(title="Agenda")

        tex_items = "\n            ".join(
            r"{\bf " + item + r"}" if i == HIGHLIGHT else item
            for i, item in enumerate(ITEMS)
        )
        text = TexBox(
            "\n            " + tex_items + "\n            ",
            width=12,
        ).next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)

        for i, item in enumerate(text):
            if i != HIGHLIGHT:
                item.set_opacity(0.15)

        self.play_animations([FadeIn(text)])
