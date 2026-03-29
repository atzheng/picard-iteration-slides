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

        # text[0]: "Input: a (sparse) conflict graph"
        self.play_animations([FadeIn(text[0])])

        # text[1]: "Each processor runs independently; upon completing a step, notify neighbors"
        # Yellow dots show which timestep each processor is currently on
        # Processor 4 (index 3) is on last timestep; others at varying positions
        dot_positions = [
            1,
            2,
            0,
            per_group - 1,
        ]  # timestep index within each group
        progress_dots = [
            Dot(
                groups[gi][dot_positions[gi]].get_center(),
                radius=0.06,
                color=YELLOW,
            ).set_z_index(2)
            for gi in range(N_GROUPS)
        ]

        # Find all conflict edges incident to Processor 1 (index 0)
        p1_edges = VGroup(
            *[
                cl
                for cl in conflict_lines
                if np.allclose(cl.get_start(), CORNERS[0], atol=0.1)
                or np.allclose(cl.get_end(), CORNERS[0], atol=0.1)
            ]
        )

        self.play_animations(
            [
                FadeIn(text[1]),
                AnimationGroup(
                    *[FadeIn(d) for d in progress_dots], lag_ratio=0.1
                ),
            ]
        )

        # Processor 1 completes a step: advance its yellow dot to the next cell
        p1_dot = progress_dots[0]
        p1_next_box = groups[0][dot_positions[0] + 1]
        self.play_animations([p1_dot.animate.move_to(p1_next_box.get_center())])

        # Conflict: Indicate edges incident to Processor 1
        self.play_animations([Indicate(p1_edges, color=RED, scale_factor=1.0)])

        # text[2]: "Neighbors check consistency; if not, roll back"
        # Processor 4 (index 3) rolls back: shift its yellow dot back one cell
        p4_dot = progress_dots[3]
        p4_prev_box = groups[3][dot_positions[3] - 1]

        self.play_animations(
            [
                FadeIn(text[2]),
                p4_dot.animate.move_to(p4_prev_box.get_center()),
            ]
        )

        # text[3]: blank line / "Problems: ..."
        # text[4]: "Problems: fully-connected conflict graph..."
        # Draw ALL edges to show fully-connected graph
        full_lines = VGroup(
            *[
                Line(
                    CORNERS[i],
                    CORNERS[j],
                    color=RED,
                    stroke_width=2,
                    stroke_opacity=0.6,
                )
                for i in range(N_GROUPS)
                for j in range(i + 1, N_GROUPS)
                if not any(
                    np.allclose(cl.get_start(), CORNERS[i], atol=0.1)
                    and np.allclose(cl.get_end(), CORNERS[j], atol=0.1)
                    or np.allclose(cl.get_start(), CORNERS[j], atol=0.1)
                    and np.allclose(cl.get_end(), CORNERS[i], atol=0.1)
                    for cl in conflict_lines
                )
            ]
        ).set_z_index(-1)

        self.play_animations(
            [
                FadeIn(text[3]),
                AnimationGroup(*[Create(l) for l in full_lines], lag_ratio=0.1),
            ]
        )

        # text[4]: "Unsynchronized message passing, bad for GPUs"
        self.play_animations([FadeIn(text[4])])
