#!/usr/bin/env python3

from manim_templates import *
from manim import *
import funcy as f

T = 20
N_GROUPS = 4
GROUP_COLORS = [BLUE_E, RED_E, GREEN_E, ORANGE]

# Corner positions for the square (UL, UR, DL, DR)
# Square width 6.5, centered at x=-1.5 (left side of slide)
_cx, _hw, _hh = -1.5, 1.625, 1.3
CORNERS = [
    UP * _hh + RIGHT * (_cx - _hw) + 2 * LEFT,
    UP * _hh + RIGHT * (_cx + _hw) + 2 * LEFT,
    DOWN * _hh + RIGHT * (_cx - _hw) + 2 * LEFT,
    DOWN * _hh + RIGHT * (_cx + _hw) + 2 * LEFT,
]


def make_timestep_boxes(n=T, box_w=0.38, box_h=0.38, gap=0.08):
    boxes = VGroup(
        *[
            Square(
                side_length=box_w,
                color=GRAY,
                fill_color=WHITE,
                fill_opacity=1,
                stroke_width=1.5,
            )
            for _ in range(n)
        ]
    ).arrange(RIGHT, buff=gap)
    return boxes


class TimeWarp(BaseSlide):
    def construct(self):
        self.setup_slide(title="The Incumbent: Time Warp")

        # --- Step 1: Row of 20 boxes ---
        boxes = make_timestep_boxes()
        boxes.next_to(self.title, DOWN, buff=0.9).to_edge(LEFT, buff=0.5)
        t0_lbl = Tex(r"$t=0$", font_size=22, color=GRAY).next_to(
            boxes[0], UP, buff=0.1
        )
        tT_lbl = Tex(r"$t=T$", font_size=22, color=GRAY).next_to(
            boxes[-1], UP, buff=0.1
        )
        self.play_animations(
            [AnimationGroup(FadeIn(boxes), FadeIn(t0_lbl), FadeIn(tT_lbl))]
        )

        # --- Step 2: Color boxes by group (random allocation) ---
        import random

        per_group = T // N_GROUPS  # 5 each
        shuffled = list(range(T))
        random.seed(42)
        random.shuffle(shuffled)
        groups = [
            VGroup(
                *[boxes[shuffled[g * per_group + i]] for i in range(per_group)]
            )
            for g in range(N_GROUPS)
        ]
        self.play_animations(
            [
                AnimationGroup(
                    *[
                        grp.animate.set_color(GROUP_COLORS[gi]).set_fill(
                            GROUP_COLORS[gi], opacity=1.0
                        )
                        for gi, grp in enumerate(groups)
                    ]
                )
            ]
        )

        # --- Step 3: Move each group to a corner, condensing into a horizontal row ---
        box_w = 0.32
        gap = 0.05
        row_half_width = (per_group - 1) * (box_w + gap) / 2
        proc_labels = [
            Tex(
                f"Processor {gi + 1}", font_size=24, color=GROUP_COLORS[gi]
            ).move_to(CORNERS[gi] + UP * 0.45)
            for gi in range(N_GROUPS)
        ]

        self.play_animations(
            [
                AnimationGroup(
                    FadeOut(t0_lbl),
                    FadeOut(tT_lbl),
                    *[
                        AnimationGroup(
                            *[
                                grp[i]
                                .animate.move_to(
                                    CORNERS[gi]
                                    + RIGHT
                                    * (i * (box_w + gap) - row_half_width)
                                )
                                .scale(box_w / 0.38)
                                for i in range(per_group)
                            ]
                        )
                        for gi, grp in enumerate(groups)
                    ],
                    *[FadeIn(lbl) for lbl in proc_labels],
                    lag_ratio=0.2,
                ),
            ]
        )

        # --- Step 4: Lines between groups (conflict graph = fully connected) ---
        np.random.seed(42)
        conflict_lines = VGroup(
            *[
                Line(
                    CORNERS[i],
                    CORNERS[
                        np.random.choice([j for j in range(N_GROUPS) if j != i])
                    ],
                    color=BLACK,
                    stroke_width=2,
                )
                for i in range(N_GROUPS)
                # for j in range(i + 1, N_GROUPS)
            ]
        )
        conflict_lines.set_z_index(-1)
        self.play_animations([Create(conflict_lines)])

        graph = VGroup(
            *[box for grp in groups for box in grp],
            *proc_labels,
            conflict_lines,
        )

        # --- Text (right of the square) ---
        text = (
            TexBox(
                r"""
                Input: a (sparse) conflict graph
                Each processor runs independently; upon completing a step, notify neighbors
                Neighbors check whether their state is consistent with new info; if not, roll back and notify their neighbors

                Problems: In general MDPs, conflict graph is fully-connected; reduces to sequential execution
                Unsynchronized message passing, bad for GPUs
                """,
                width=6.5,
            )
            .next_to(graph, RIGHT, buff=0.4)
            .set_y(0)
        )

        self.play_animations([*map(FadeIn, text)])
