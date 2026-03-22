#!/usr/bin/env python3

from manim_templates import *
from manim import *
import funcy as f

from Agenda1 import ITEMS

HIGHLIGHT = 1  # 0-indexed


class Agenda2(BaseSlide):
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
