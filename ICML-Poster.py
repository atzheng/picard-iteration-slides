from manim_templates import *
from manim_templates import ParTex
from manim import *
from manim import (
    VGroup,
    VDict,
    MathTex,
    Tex,
    ImageMobject,
    config,
    Arrow,
    RED,
    GREEN,
    BLACK,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    WHITE,
    CurvedArrow,
    SurroundingRectangle,
    Rectangle,
    NumberPlane,
    DEGREES,
    TexTemplate,
    Line,
    Dot,
    Group,
)
import funcy as f
import itertools as it


# config.pixel_width = 1080
# config.pixel_height = r
config.frame_width = 16
config.frame_height = 12


def make_arrow(start, end, **kwargs):
    default_kwargs = {
        "buff": 0.1,
        "stroke_width": 1,
        "max_tip_length_to_length_ratio": 0.15,
    }
    return Arrow(start, end, **{**default_kwargs, **kwargs})


def create_sequence(T):
    seq = VGroup(
        *it.chain.from_iterable(
            [
                f.lmap(
                    MathTex,
                    [rf"s_{i}", rf"\pi", rf"a_{i}", r"f", rf"\omega_{i}"],
                )
                for i in range(T)
            ]
        )
    ).arrange_in_grid(n_rows=T, n_cols=5, buff=1)

    rs, pis, acs, fs, oms = [
        [seq[5 * i + j] for i in range(T)] for j in range(5)
    ]

    for pi in pis:
        pi.add_background_rectangle(color=RED, buff=0.2)

    for fx in fs:
        fx.add_background_rectangle(color=GREEN, buff=0.2, opacity=0.3)

    arrows = VDict(
        it.chain.from_iterable(
            [
                [
                    ((s, pi), make_arrow(s.get_right(), pi.get_left()))
                    for s, pi in zip(rs, pis)
                ],
                [
                    ((pi, ac), make_arrow(pi.get_right(), ac.get_left()))
                    for pi, ac in zip(pis, acs)
                ],
                [
                    ((ac, f), make_arrow(ac.get_right(), f.get_left()))
                    for ac, f in zip(acs, fs)
                ],
                [
                    ((f, om), make_arrow(om.get_left(), f.get_right()))
                    for f, om in zip(fs, oms)
                ],
                [
                    (
                        (f, s_next),
                        make_arrow(
                            f.get_bottom(),
                            s_next.get_top(),
                            max_tip_length_to_length_ratio=0.05,
                        ),
                    )
                    for f, s_next in zip(fs[:-1], rs[1:])
                ],
                [
                    (
                        (s, f),
                        CurvedArrow(
                            s.get_bottom(),
                            f.get_left(),
                            angle=1,
                            color=BLACK,
                            fill_color=WHITE,
                            stroke_width=1,
                            tip_length=0.15,
                        ),
                    )
                    for s, f in zip(rs, fs)
                ],
            ]
        )
    )

    rs.append(VGroup())
    arrows[(fs[-1], rs[-1])] = VGroup()

    return rs, pis, acs, fs, oms, arrows


class ICML_Poster(Scene):
    def construct(self):
        mytemplate = TexTemplate(
            tex_compiler="xelatex",
            output_format=".xdv",
            preamble=r"""
\usepackage[english]{babel}
\usepackage{xcolor}
\newcommand\red[1]{\color{red}#1}
\newcommand\blue[1]{\color{blue}#1}
\newcommand\green[1]{\color{green}#1}
% \newcommand[red][\color{red}]
% \newcommand[blue][\color{blue}]
% \newcommand[green][\color{green}]
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{amssymb}
\usepackage{varwidth}
\usepackage{fontspec}
\usepackage{ragged2e}
            """,
        )
        fg_color = BLACK
        Line.set_default(color=fg_color)
        Dot.set_default(color=fg_color)
        Arrow.set_default(color=fg_color, stroke_width=2, tip_length=0.2)
        MathTex.set_default(color=fg_color, font_size=40)
        Tex.set_default(color=fg_color, font_size=19, tex_template=mytemplate)
        tex = f.partial(ParTex, width=7.5 / 8)

        c = NumberPlane().add_coordinates().fade(0.9)
        c.get_x_axis().numbers.set_color(BLACK)
        c.get_y_axis().numbers.set_color(BLACK)
        # self.add(c)

        title = (
            Tex(
                r"{\bf Speeding Up Policy Simulation in Supply Chain RL}",
                font_size=50,
            )
            .to_edge(UP)
            .to_edge(LEFT)
        )
        authors = ParTex(
            "Vivek Farias (MIT), Joren Gijsbrechts (ESADE), Aryan Khojandi (MIT), Tianyi Peng (Columbia), Andy Zheng (UBC)",
            width=2,
        ).next_to(title, DOWN, buff=0.1, aligned_edge=LEFT)

        qr = ImageMobject("qr.png").scale(0.18).to_corner(UP + RIGHT, buff=0.1)

        tldr = (
            tex(
                r"""
            {\bf TL;DR}: How to speed up policy simulation when horizons are long? \\ {\bf Parallelize over time}!
                \setlength{\leftmargini}{1em}
            \begin{itemize}
            \setlength\itemsep{0.0em}
            \item {\bf Picard iteration}: an iterative, parallel (GPU-friendly) simulation algo
            \item Converges in a few ($\ll T$) iterations for certain problem classes
            \item Up to {\bf 441x} speedups over sequential
            \item Beyond the theory, {\bf applicable to any MDP}
            \end{itemize}
            """,
            )
            .add_background_rectangle(
                color=GREEN,
                buff=0.2,
                opacity=0.5,
                corner_radius=0.2,
                stroke_color=BLACK,
                stroke_width=1,
                stroke_opacity=1,
            )
            .next_to(authors, DOWN, buff=0.1, aligned_edge=LEFT)
        )

        # Algo
        # -------------------------------------------------------------------------

        # T = 4
        # rs, pis, acs, fs, oms, arrows = create_sequence(T)
        # time_labels = VGroup(
        #     *[
        #         MathTex(f"t={i}")
        #         .rotate(90 * DEGREES)
        #         .next_to(rs[i], LEFT, buff=0.5)
        #         .set_opacity(0.4)
        #         for i in range(T)
        #     ]
        # )
        # seq_group = VGroup(rs, pis, acs, fs, oms, time_labels)

        expensive = tex(
            r"Assume $f$ is cheap and $\pi$ is expensive, so want to parallelize $\pi$ calls"
        )

        T = 4
        # Create sequences
        rs1, pis1, acs1, fs1, oms1, arrows1 = create_sequence(T)
        rs2, pis2, acs2, fs2, oms2, arrows2 = create_sequence(T)

        pis1[1].set_opacity(0.0)
        arrows1[(rs1[1], pis1[1])].set_opacity(0.0)
        arrows1[(pis1[1], acs1[1])].set_opacity(0.0)

        pis1[3].set_opacity(0.0)
        arrows1[(rs1[3], pis1[3])].set_opacity(0.0)
        arrows1[(pis1[3], acs1[3])].set_opacity(0.0)


        pis2[0].set_opacity(0.0)
        arrows2[(rs2[0], pis2[0])].set_opacity(0.0)
        arrows2[(pis2[0], acs2[0])].set_opacity(0.0)

        pis2[2].set_opacity(0.0)
        arrows2[(rs2[2], pis2[2])].set_opacity(0.0)
        arrows2[(pis2[2], acs2[2])].set_opacity(0.0)

        for x in acs1:
            x.set_opacity(0.0)
        for x in acs2:
            x.set_opacity(0.0)

        seq1 = VGroup(
            *rs1, *pis1, *acs1, *fs1, *oms1, *arrows1.get_all_submobjects()
        ).shift(LEFT * 3.5 + 0.5 * DOWN)
        seq2 = VGroup(
            *rs2, *pis2, *acs2, *fs2, *oms2, *arrows2.get_all_submobjects()
        ).shift(RIGHT * 3.5 + 0.5 * DOWN)

        time_labels = VGroup(
            *[
                MathTex(f"t={i}")
                .rotate(90 * DEGREES)
                .next_to(rs1[i], LEFT, buff=0.5)
                .set_color(BLUE_E if i % 2 == 0 else "#800000")
                for i in range(T)
            ]
        )

        # Cache overlays
        acache1 = VGroup(
            *[
                VGroup(
                    *[
                        MathTex(f"a_{i}^{{(k-1)}}").move_to(acs1[i])
                        for i in [1, 3]
                    ]
                ),
                VGroup(
                    *[
                        MathTex(f"a_{i}^{{(k)}}").move_to(acs1[i]).set_color(BLUE_E)
                        for i in [0, 2]
                    ]
                )
            ]
        )
        acache2 = VGroup(
            *[
                VGroup(
                    *[
                        MathTex(f"a_{i}^{{(k-1)}}").move_to(acs2[i])
                        for i in [0, 2]
                    ]
                ),
                VGroup(
                    *[
                        MathTex(f"a_{i}^{{(k)}}").move_to(acs2[i]).set_color(
                            "#800000"
                        )
                        for i in [1, 3]
                    ]
                )
            ]
        )

        # acache1[0].set_color(BLUE_E)

        acache1_bg = SurroundingRectangle(
            acache1,
            fill_color=BLACK,
            fill_opacity=0.1,
            stroke_width=0,
            buff=0.2,
        )
        acache2_bg = SurroundingRectangle(
            acache2,
            fill_color=BLACK,
            fill_opacity=0.1,
            stroke_width=0,
            buff=0.2,
        )

        # Row highlights
        bg1 = VGroup(
            *[
                Rectangle(
                    width=seq1.width,
                    height=1.1,
                    color=BLUE_E,
                    fill_opacity=0.1,
                    stroke_width=0,
                ).move_to(VGroup(rs1[i], oms1[i]))
                for i in [0, 2]
            ]
        )
        bg2 = VGroup(
            *[
                Rectangle(
                    width=seq2.width,
                    height=1.1,
                    color="#800000",
                    fill_opacity=0.1,
                    stroke_width=0,
                ).move_to(VGroup(rs2[i], oms2[i]))
                for i in [1, 3]
            ]
        )

        headings = VGroup(
            MathTex(r"\text{Processor 1}", color=BLUE_E).next_to(
                seq1, UP, buff=0.5
            ),
            MathTex(r"\text{Processor 2}", color="#800000").next_to(
                seq2, UP, buff=0.5
            ),
        )

        # # Synchronized cache highlights
        # sync_cps = VGroup(
        #     MathTex("a_1^{(k+1)}").move_to(acs2[1]),
        #     MathTex("a_3^{(k+1)}").move_to(acs2[3]),
        #     MathTex("a_0^{(k+1)}").move_to(acs1[0]),
        #     MathTex("a_2^{(k+1)}").move_to(acs1[2]),
        # )

        final_group = VGroup(
            seq1,
            seq2,
            time_labels,
            acache1,
            acache2,
            acache1_bg,
            acache2_bg,
            bg1,
            bg2,
            # sync_cps,
            *headings,  # , text,
        ).scale(0.4)
        caption = ParTex(
            r"""
            {\bf Example}: A single iteration. Proc. 1 assigned $t \in \{0, 2\}$; Proc. 2 assigned $t \in \{1, 3\}$. Each Proc. only executes $\pi$, updates cache to $a_t^{(k)}$ for assigned $t$. Independent $\pi$ calls executed in batch.
            """,
            font_size=13,
            width=1.3
        ).next_to(final_group, DOWN)
        final_group.add(caption)


        

        goal = tex(
            r"{\bf Goal}: using a parallel algorithm, generate the correct (state, action) {\bf trajectory} $(s_0, a_0) \ldots (s_T, a_T)$, corresponding to sequentially evaluating the {\it policy} $a_t = \pi(s_t, \omega_t)$ and {\it dynamics} $s_{t+1} = f(s_t, a_t, \omega_t)$ ($\{\omega_t\}_{t \in [T]}$ is noise)",
        )
        algo = (
            VGroup(
                Tex(r"{\bf The Algorithm: Picard Iteration }", font_size=30),
                goal,
                expensive,
                tex(
                    r"{\bf Setup}: {\bf assign} each processor a set of times; {\bf initialize a cache} of actions $a_t^{(0)}$ (superscript indicates iteration \#)"
                ),
                tex(
                    r"1. At {\bf Iteration} $k \geq 1$: Each process simulates independently... but only computes action $a_t^{(k)}$ for assigned times (o.w., use cached action $a_t^{(k-1)}$)"
                ),
                final_group,
                tex(
                    r"2. {\bf Synchronize} newly computed actions $a_t^{(k)}$ across processors"
                ),
                tex(
                    r"3. Stop if fixed point $a_t^{(k)} = a_t^{(k-1)}$ for all $t$; o.w. increment $k$, iterate"
                ),
                tex(
                    r"{\bf How fast is it}? With horizon $T$, $N$ processors, requiring $K$ iterations, Picard takes time $KT/N$ (vs. $T$ for sequential)"
                ),
                tex(
                    "In worst case, $K = T$; but will prove $K \ll T$ for specific problems"
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .next_to(tldr, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        final_group.set_x(goal.get_x())

        # subalgo = VGroup(*algo[3:8])
        # subalgo.add_background_rectangle(
        #         opacity=0.,
        #         stroke_color=BLACK,
        #         stroke_opacity=1,
        #         stroke_width=1,
        #         buff=0.1,
        #         corner_radius=0.1,
        # )

        # Theory
        # -------------------------------------------------------------------------
        thtex = f.partial(ParTex, width=9.5 / 8)
        thm = thtex(
            r"{\bf Theorem:} For a policy satisfying Assumption 1, Picard Iteration converges in $K \leq J + 1$ iterations.",
            width=6 / 8,
        ).add_background_rectangle(
            color=BLUE,
            buff=0.2,
            opacity=0.2,
            corner_radius=0.2,
            stroke_color=BLACK,
            stroke_width=1,
            stroke_opacity=1,
        )
        # Create and position images
        shopper = ImageMobject("shopper.png").scale(0.2)
        wh1 = ImageMobject("warehouse.png").scale(0.2)
        wh2 = ImageMobject("warehouse.png").scale(0.2)
        wh3 = ImageMobject("warehouse.png").scale(0.2)

        # Position elements
        shopper.move_to(LEFT * 3)
        wh1.move_to(UP * 2)
        wh2.move_to(RIGHT * 0.5)
        wh3.move_to(LEFT + DOWN)

        # Create lines
        line1 = Line(shopper.get_right(), wh1.get_left(), stroke_width=1)
        line2 = Line(shopper.get_right(), wh2.get_left(), stroke_width=1)
        line3 = Line(shopper.get_right(), wh3.get_left(), stroke_width=1)

        # Create cost labels
        c1 = (
            MathTex(r"c_1(\omega_t)")
            .scale(0.5)
            .next_to(line1.get_center(), UP, buff=0.2)
        )
        c2 = (
            MathTex(r"c_2(\omega_t)")
            .scale(0.5)
            .next_to(line2.get_center(), UP, buff=0.2)
        )
        c3 = (
            MathTex(r"c_3(\omega_t)")
            .scale(0.5)
            .next_to(line3.get_center(), RIGHT, buff=0.2)
        )

        # Create labels for shopper and warehouses
        shopper_label = (
            Tex(r"Order $\omega_t$ \\ for product $i(\omega_t)$")
            .scale(0.8)
            .next_to(shopper, DOWN, buff=0.2)
        )

        wh1_label = (
            MathTex(
                r"\text{Inventory }W_{\cdot, 1,t} \\ \text{Capacity }C_{1,t}"
            )
            .scale(0.5)
            .next_to(wh1, DOWN, buff=0.2)
        )
        wh2_label = (
            MathTex(
                r"\text{Inventory }W_{\cdot, 2,t} \\ \text{Capacity }C_{2,t}"
            )
            .scale(0.5)
            .next_to(wh2, DOWN, buff=0.2)
        )
        wh3_label = (
            MathTex(
                r"\text{Inventory }W_{\cdot, 3,t} \\ \text{Capacity }C_{3,t}"
            )
            .scale(0.5)
            .next_to(wh3, DOWN, buff=0.2)
        )

        # Group all elements
        graph = Group(
            shopper,
            wh1,
            wh2,
            wh3,
            line1,
            line2,
            line3,
            c1,
            c2,
            c3,
            shopper_label,
            wh1_label,
            wh2_label,
            wh3_label,
        ).scale(0.5)

        fulfill_text = ParTex(
            r"""
            Network with products $i \in [I]$ and warehouses $j \in [J]$
            \setlength{\leftmargini}{1em}
            \begin{itemize}
            \setlength\itemsep{0.0em}
            \item At time $t$, customer $\omega_t$ orders product $i(\omega_t)$
            \item {\bf State}: inventory $W_{i,j,t}$ and shipping capacity $C_{j,t}$
            \item {\bf Action}: which warehouse $a_t \in [J]$ to ship from (or unfulfill)
            \item {\bf Reward}: shipping cost $c_{a_t}(\omega_t)$
            \end{itemize}
            {\bf Picard iteration}: each processor {\bf assigned} to a product, processes all orders for that product. {\bf Initial cache}: simply unfulfill
                    """,
            width=6.5 / 8,
        ).next_to(graph, LEFT, aligned_edge=UP)

        theory = (
            Group(
                Tex(r"{\bf Example: Fulfillment Optimization}", font_size=30),
                Group(fulfill_text, graph),
                thm,
                Tex(
                    r"$\implies$ $N/J$ times faster than sequential; for large retailers $J \approx 100$"
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            .next_to(tldr, RIGHT, buff=0.18, aligned_edge=UP)
            .shift(DOWN * 0.1)
        )

        # Experiments
        # -------------------------------------------------------------------------
        expt_figs = Group(
            Tex(
                r"""
\begin{table}
    \centering
    % Reduce font size (optional)
    \small
    % Reduce horizontal space (optional)
    \setlength{\tabcolsep}{5pt}
    \begin{tabular}{lcc}
        \toprule
        \multicolumn{1}{l}{\textbf{Problem Scale}} & \multicolumn{1}{c}{\textbf{Runtime}} & \multicolumn{1}{c}{\textbf{Runtime}} \\
        \multicolumn{1}{l}{\textbf{\#Orders/ \#Products}} & \multicolumn{1}{c}{\textbf{Sequential}} & \multicolumn{1}{c}{\textbf{Picard}} \\
        \midrule
        3k / 1k     & 1m32s   & 59s \\
        30k / 10k  & 6m55s   & 1m01s \\
        300k / 100k & 1h04m   &  1m04s\\
        3M / 1M     & 10h02m  & 1m39s \\
        30M / 10M   & 4 days & 4m57s \\
        \bottomrule
    \end{tabular}
\end{table}
% \vspace{-2em}
            """
            ).scale(0.8),
            ParTex(
                r"{\bf Speed vs. Problem size}, for policy {\it optimization} with 1k policy gradient steps. Relative gains increase with problem size.",
                font_size=13,
                width=0.8,
            ),
            ImageMobject("uniform.png").scale(0.21),
            ParTex(
                r"{\bf Speed vs. Parallelism}:  PI is {\bf up to 441x faster} than sequential, speed linear in batch size. 3M orders, 1M products.",
                font_size=13,
                width=0.8,
            ),
        ).arrange_in_grid(
            n_rows=2,
            n_cols=2,
            # buff=0.5,
            flow_order="dr",
            row_alignments=["c", "u"],
        )
        expt_figs[1].shift(0.2 * UP)
        expt_figs[3].shift(0.2 * UP)

        expt_exp = ParTex(
            r"""
        {\bf Numerical results}: Implemented in JAX, on one A100 GPU. Policy is MLP with $\sim$10k params. On GPU, parallelism implemented by batching policy calls for multiple timesteps.
        """,
            width=1.15,
        )

        expts = (
            Group(
                expt_exp,
                expt_figs,
            )
            .arrange(DOWN, buff=0.3)
            .next_to(theory, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        ass = ParTex(
            r"""
            {\bf Assumption 1}: Policy is invariant to ``irrelevant'' state perturbations:
            \setlength{\leftmargini}{1em}
            \begin{itemize}
            \setlength\itemsep{0.0em}
            \item {\it Product locality}: Action $a_t$ depends only on inventory for $i(\omega_t)$
            \item {\it Node locality}: Changing state at node $j$ either doesn't affect action, or else switches action to node $j$
            \item {\it Monotonicity}: Increasing inventory at node $a_t$ will not change fulfillment away from that node
            \item {\it Capacity Dependence}: Action depends on capacity only via the {\it set} of nodes with exhausted capacity
            \end{itemize}

            {\it Intuition: limits dependence on on other processors' state. Includes greedy and bid-price policies.}
            """,
            font_size=7,
            width=0.9,
        ).next_to(thm, RIGHT, buff=0.4)

        ass.add_background_rectangle(
            opacity=0,
            stroke_color=BLACK,
            stroke_opacity=1,
            stroke_width=1,
            buff=0.1,
            corner_radius=0.1,
        )

        ass.add(
            Line(ass.get_left(), thm.get_right(), color=BLACK, stroke_width=1)
        )

        # Mujoco
        # -------------------------------------------------------------------------
        muimg = ImageMobject("mujoco-results.png").scale(0.22)
        mucap = ParTex(
            r"{\bf Iterations to convergence} for a single policy evaluation, in several envs. $T=200$. Converges to $\leq $0.1\% RMSE in $\leq 15$ iterations for all envs.",
            font_size=13,
            width = 0.95
        ).next_to(muimg, DOWN).shift(0.1 *UP)
        muimg.add(mucap)
        muexpl = text = (
            VGroup(
                ParTex(
                    r"Picard applies to generic MDPs: {\bf assign} each timestep to a different processor, {\bf initialize cache} with actions from previous policy iterate.",
                ),
                ParTex(
                    r"Continuous control env for robotics. Measure convergence in $L_2$ distance of state trajectory."
                ),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ).next_to(muimg, LEFT, aligned_edge=UP, buff=0.3)
        muimg.shift(0.2 * UP)
        muimg.add(muexpl)

        mujoco = (
            Group(
                Tex(r"{\bf Beyond supply chain: Mujoco}", font_size=30), muimg
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(expts, DOWN, buff=0.3, aligned_edge=LEFT)
        )
        muimg.shift(0.2 * UP)

        graph.shift(0.2 * UP)

        for x in [
            title,
            authors,
            tldr,
            goal,
            algo,
            theory,
            expts,
            ass,
            qr,
            mujoco,
            # subalgo
        ]:
            self.add(x)
