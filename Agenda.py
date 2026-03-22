#!/usr/bin/env python3

from manim_templates import *
from manim import *
import funcy as f


class Agenda(BaseSlide):
    def construct(self):
        self.setup_slide(title="Agenda")

        text = TexBox(
            r"""
            1. The challenge of policy simulation
            2. Our method: Picard Iteration
            3. Convergence of Picard Iteration
            4. Numerical Results
            5. Beyond Policy Simulation
            """,
            width=12,
        ).next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)

        self.play_animations([*map(FadeIn, text)])
