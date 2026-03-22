#!/usr/bin/env python3

from manim_templates import *
from manim import *
import funcy as f
import numpy as np
from scipy.special import binom
from ggmanim import GGManim

PROC_COLORS = [BLUE_E, RED_E, GREEN_E, ORANGE]
ROWS = 6
COLS = 6
BOX = 0.36
GAP = 0.05


def make_grid(color_fn):
    grid = VGroup()
    for r in range(ROWS):
        for c in range(COLS):
            box = Square(
                side_length=BOX,
                fill_color=color_fn(r, c),
                fill_opacity=0.85,
                stroke_color=WHITE,
                stroke_width=1,
            ).move_to(RIGHT * c * (BOX + GAP) + DOWN * r * (BOX + GAP))
            grid.add(box)
    return grid


def labeled_grid(color_fn, title):
    grid = make_grid(color_fn)
    grid_title = Tex(title, font_size=26, color=BLACK).next_to(
        grid, UP, buff=0.2
    )
    time_lbl = Tex(r"Time $\rightarrow$", font_size=20, color=GRAY).next_to(
        grid, DOWN, buff=0.18
    )
    grad_lbl = (
        Tex(r"$\leftarrow$ Gradient steps", font_size=20, color=GRAY)
        .rotate(90 * DEGREES)
        .next_to(grid, LEFT, buff=0.18)
    )
    return VGroup(grid_title, grid, time_lbl, grad_lbl), grid


class ComputationGraph(BaseSlide):
    def construct(self):
        self.setup_slide(title="Beyond Policy Simulation")

        # --- Three color functions ---
        # Grid 1: same color per column (partitioned by time step)
        col_colors = [PROC_COLORS[c % len(PROC_COLORS)] for c in range(COLS)]

        def by_column(r, c):
            return col_colors[c]

        # Grid 2: same color per row (partitioned by gradient step)
        row_colors = [PROC_COLORS[r % len(PROC_COLORS)] for r in range(ROWS)]

        def by_row(r, c):
            return row_colors[r]

        # Grid 3: each cell independently colored (fully parallel)
        np.random.seed(7)
        cell_colors = np.random.choice(len(PROC_COLORS), size=(ROWS, COLS))

        def by_cell(r, c):
            return PROC_COLORS[cell_colors[r, c]]

        # --- Build grids ---
        grp1, grid1 = labeled_grid(by_column, "Parallel over time")
        grp2, grid2 = labeled_grid(by_row, "Parallel over gradients")
        grp3, grid3 = labeled_grid(by_cell, "Fully parallel")

        row = VGroup(grp1, grp2, grp3).arrange(RIGHT, buff=0.7)
        row.scale(0.8).next_to(self.title, DOWN, buff=0.5).set_x(0)

        text = (
            TexBox(
                r"""
            Gradient Descent: $\theta_{i+1} = \theta_i - \eta \nabla J(\theta_i)$
            Speculative GD: $\theta_{i+1}^{(k)} = \theta_{i}^{(k)} - \eta \nabla J(\theta^{(k-1)}_{i})$
            {\bf Proposition}: For an $L$-smooth function, after $k$ iterations, the $i^{\rm th}$ Spec. GD iterate converges at rate $\| \theta_i - \theta_i^{(k)}\| \leq (\eta L i / k)^k$ 
            For quadratic loss, $k^{\rm th}$ iterate is the $k^{\rm th}$ degree Taylor of approx of $\theta_i$ (in $i$).
            """,
                width=6.5,
                height=4,
            )
            .next_to(row, DOWN, buff=0.3)
            .to_edge(LEFT)
        )

        def xt(t, k):
            x1 = 0.5
            eta = 0.2
            return 2 + x1 * sum(
                [
                    binom(t, j) * (-2 * eta) ** j
                    for j in range(min(k + 1, k + 1))
                ]
            )

        plot = (
            GGManim()
            .ylim((0, 4))
            .xlim((0, 10))
            .xlab("GD iterate $i$")
            .ylab(r"$\theta_i$")
            .geom_function(function=lambda t: xt(t, 1), color=RED, label="k=1")
            .geom_function(function=lambda t: xt(t, 2), color=RED, label="k=2")
            .geom_function(function=lambda t: xt(t, 3), color=RED, label="k=3")
            .geom_function(function=lambda t: xt(t, 4), color=RED, label="k=4")
            .geom_function(
                function=lambda t: xt(t, 10), color=BLACK, label="Seq"
            )
            .build(
                x_length=6.5,
                y_length=4,
            )
            .scale_to_fit_height(3.6)
            .to_corner(DOWN + RIGHT, buff=0.5)
        )

        # --- Animations ---
        self.play_animations(
            [
                FadeIn(grp1),
                FadeIn(grp2),
                *map(FadeIn, text[:-1]),
                FadeIn(grp3),
                FadeIn(plot["axes"]),
                *map(Create, plot["layers"]),
                FadeIn(text[-1]),
            ]
        )
