#!/usr/bin/env python3

from manim_templates import *
from manim import *
import funcy as f
import pandas as pd

from ggmanim import GGManim


COM_COLOR = RED_E
MEM_COLOR = BLUE_D


def make_flow_box(label, sublabel=None, width=2.0, height=0.9, color=BLUE_E):
    rect = Rectangle(width=width, height=height, color=color, stroke_width=2)
    if sublabel:
        top = (
            Tex(label, font_size=24, color=color).move_to(rect).shift(UP * 0.16)
        )
        bot = (
            Tex(sublabel, font_size=18, color=GRAY)
            .move_to(rect)
            .shift(DOWN * 0.18)
        )
        return VGroup(rect, top, bot)
    lbl = Tex(label, font_size=24, color=color).move_to(rect)
    return VGroup(rect, lbl)


class GPU(BaseSlide):
    def construct(self):
        self.setup_slide(title="Aside: Parallelism on GPU")

        text = TexBox(
            r"""
            Parallelism here: policies on different `processors' are executed in batch
            Why are large batches fast to compute? (Hint: not b/c a GPU has many cores)
            E.g., multiply $d \times d$ weight matrix by size $d$ vectors, in batches of $B$:
            """,
            width=8,
        ).next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)

        # --- Flowchart: VRAM -> Registers -> Compute ---
        box_vram = make_flow_box("VRAM", r"", color=MEM_COLOR)
        box_compute = make_flow_box("Compute", r"", color=COM_COLOR)

        flow = VGroup(box_vram, box_compute).arrange(RIGHT, buff=1.8)
        flow.next_to(text, DOWN, buff=0.4, aligned_edge=LEFT)

        def flow_arrow(a, b):
            return Arrow(
                a[0].get_right(),
                b[0].get_left(),
                buff=0.08,
                stroke_width=2,
                tip_length=0.18,
                color=BLACK,
            )

        arr_vr = flow_arrow(box_vram, box_compute).set_color(MEM_COLOR)
        arr_rc = (
            arr_vr.copy()
            .next_to(box_compute, RIGHT, buff=0.0)
            .set_color(COM_COLOR)
        )

        bw_lbl = Tex(
            r"Bandwidth (GB/s)", font_size=20, color=MEM_COLOR
        ).next_to(arr_vr, UP, buff=0.06)
        bw_lbl_2 = Tex(
            r"$2^{39}$ FP16/s", font_size=18, color=MEM_COLOR
        ).next_to(arr_vr, DOWN, buff=0.02)
        fl_lbl = Tex(r"FLOPS/s", font_size=20, color=COM_COLOR).next_to(
            arr_rc, UP, buff=0.06
        )
        fl_lbl_2 = Tex(
            r"$2^{48}$ FP16 FLOPS/s", font_size=18, color=COM_COLOR
        ).next_to(arr_rc, DOWN, buff=0.02)

        flowchart = VGroup(flow, arr_vr, arr_rc, bw_lbl, fl_lbl)

        text2 = TexBox(
            r"""
            VRAM: Every batch moves $d \times d$ weights + $d \times B$ batch
            Larger batches amortize the $d \times d$ weight movement
            Linear gains in throughput until you hit compute bottleneck
            """,
            width=8,
        ).next_to(flow, DOWN, buff=0.3, aligned_edge=LEFT)
        data = pd.read_csv("matvec_throughput_results.csv")
        data.columns = ["Batch Size", "Throughput"]
        data["Log(Batch Size)"] = np.log2(data["Batch Size"])
        data["Log(MatVecs / s)"] = np.log2(data["Throughput"])

        plot = (
            (
                GGManim(
                    data, aes={"x": "Log(Batch Size)", "y": "Log(MatVecs / s)"}
                )
                .geom_function(
                    function=lambda x: np.log2(
                        2**39 / (2 ** (24 - x) + 2**12)
                    ),
                    color=MEM_COLOR,
                    # label="Mem. Bandwidth",
                )
                .geom_hline(yintercept=23, color=COM_COLOR, label="Compute Bound")
                .ylim((16, 30))
                .geom_line(label="Empirical", color=GREEN_D)
                .geom_hline(yintercept=27, color=MEM_COLOR, label="Memory Bound")
                .build(
                    x_length=4,
                    y_length=4,
                    axis_config={
                        "include_ticks": False,
                        "include_numbers": False,
                    },
                )
            )
            .next_to(text, RIGHT, buff=0.5)
            .set_y(0)
        )

        plot["layers"][0][1].next_to(
            plot["layers"][0][0], UP, aligned_edge=RIGHT, buff=0.1
        )
        plot["layers"][2][1].next_to(
            plot["layers"][2][0].get_right(), DOWN, aligned_edge=RIGHT, buff=0.1
        ).set_color(GREEN_D)

        self.play_animations(
            [
                *map(FadeIn, text),
                FadeIn(plot["axes"]),
                Create(box_vram),
                Create(arr_vr),
                Create(box_compute),
                Create(arr_rc),
                FadeIn(bw_lbl),
                FadeIn(fl_lbl),
                FadeIn(bw_lbl_2),
                Create(plot["layers"][3]),
                FadeIn(fl_lbl_2),
                Create(plot["layers"][1]),
                *map(FadeIn, text2[:-1]),
                Create(plot["layers"][0]),
                FadeIn(text2[-1]),
                Create(plot["layers"][2]),
            ]
        )
