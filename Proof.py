from manim_templates import *
from manim import *
import funcy as f
import random
from functools import partial


class Proof(BaseSlide):
    def construct(self):
        self.setup_slide(title="Convergence Proof for Greedy Policy")

        # Create N squares with random colors
        N = 10
        base_colors = [WHITE, BLUE_E, GREEN_E, YELLOW_E]
        exhaust_indices = [4, 7]
        random.seed(101)
        colors = []
        for i in range(N):
            if i <= exhaust_indices[0]:
                colors.append(random.choice(base_colors))
            elif i <= exhaust_indices[1]:
                colors.append(random.choice(base_colors[:-1]))
            else:
                colors.append(base_colors[0])
        colors[exhaust_indices[0]] = base_colors[-1]
        colors[exhaust_indices[1]] = base_colors[-2]

        squares = VGroup(
            *[
                Square(
                    side_length=0.4,
                    stroke_color=BLACK,
                    stroke_width=1,
                    fill_color=col,
                    fill_opacity=0.5,
                )
                for col in colors
            ]
        )
        squares.arrange(RIGHT, buff=0.1)
        squares.add(
            MathTex(r"a_t^{\rm seq}")
            .scale(0.7)
            .next_to(squares, LEFT, buff=0.2)
        )
        squares.next_to(self.title, DOWN, buff=1).set_x(0)

        iter0 = squares.copy().shift(DOWN)
        iter0[-1].become(MathTex(r"a_t^{(0)}").scale(0.7).move_to(iter0[-1]))
        for idx in range(N):
            iter0[idx].set_fill(WHITE)
            if iter0[idx].get_fill_color() != squares[idx].get_fill_color():
                iter0[idx].set_stroke(RED, width=4, opacity=1)

        iter1 = squares.copy().shift(2 * DOWN)
        iter1[-1].become(MathTex(r"a_t^{(1)}").scale(0.7).move_to(iter1[-1]))
        for idx in range(exhaust_indices[0] + 2, N):
            iter1[idx].set_fill(
                random.choice([base_colors[0], *base_colors[-2:]]), opacity=0.5
            )
            if iter1[idx].get_fill_color() != squares[idx].get_fill_color():
                iter1[idx].set_stroke(RED, width=4, opacity=1)
        iter1[exhaust_indices[0] + 2].set_fill(base_colors[-1], opacity=0.5)

        iter2 = squares.copy().shift(3 * DOWN)
        iter2[-1].become(MathTex(r"a_t^{(2)}").scale(0.7).move_to(iter2[-1]))
        for idx in range(exhaust_indices[1] + 1, N):
            iter2[idx].set_fill(
                random.choice([base_colors[0], base_colors[-2]]), opacity=0.5
            )
            if iter2[idx].get_fill_color() != squares[idx].get_fill_color():
                iter2[idx].set_stroke(RED, width=4, opacity=1)
        iter2[exhaust_indices[0] + 1].set_fill(base_colors[-2], opacity=0.5)

        iter3 = squares.copy().shift(4 * DOWN)
        iter3[-1].become(MathTex(r"a_t^{(3)}").scale(0.7).move_to(iter3[-1]))

        iters = VGroup(squares, iter0, iter1, iter2, iter3).to_edge(LEFT)
        # # Randomly select 4 indices to color red
        # for idx in red_indices:
        #     squares[idx].set_fill(RED, opacity=1)
        #     squares[idx].set_stroke(RED)

        # Add labels and arrows for red squares
        labels = VGroup()
        exhaust_names = ["Yellow", "Green"]
        for i, idx in enumerate(exhaust_indices):
            label = Text(
                f"{exhaust_names[i]}\nExhausted", font_size=16, color=BLACK
            )
            label.next_to(squares[idx], UP, buff=0.2)
            arrow = Arrow(
                label.get_bottom(),
                squares[idx].get_top(),
                color=BLACK,
                buff=0.05,
                max_tip_length_to_length_ratio=0.15,
                stroke_width=1,
            )
            labels.add(VGroup(label, arrow))

        squares.add_background_rectangle(color=GREEN, opacity=0.1, buff=0.2)

        Texx = partial(ParTex, width=0.6, font_size=32)
        text = (
            VGroup(
                Texx(r"By Lemma: If no nodes exhausted, there are no mistakes"),
                Texx(r"Also: no processor will choose a node known to be exhausted in the cache"),
                Texx(r"Therefore: if next iter has a mistake, it chose an {\bf exhausted node} which is {\bf not yet known to be exhausted} in the cache."),
                # ParTex(
                #     r"At iter $k$: suppose cache is correct up to time $t_k$, i.e.,",
                #     width=0.9,
                # ),
                # MathTex(r"a_t^{(k)} = a_t^{\rm seq} \quad \forall t \leq t_k"),
                # ParTex(
                #     r"By Lemma: first incorrect action $a_{t_k+1}^{(k)}$ chose a node with exhausted capacity",
                #     width=0.9,
                # ),
                # ParTex(
                #     r"However, since cache is correct up to $t_k$: all processors now know that this node is exhausted",
                #     width=0.9,
                # ),
                Texx(
                    r"At most $J$ nodes can be exhausted, so at most $J$ mistakes can occur",
                ),
                # Texx(
                #     r"\textbf{Summary}: Processors only chose incorrect actions when a node's capacity runs out; and capacity can only run out $J$ times."
                # ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)
            .to_edge(RIGHT)
        )

        self.play_animations(
            [
                Create(squares),
                Create(labels),
                Create(iter0),
                Create(iter1),
                FadeIn(text[0]),
                Indicate(iter1[:exhaust_indices[0]]),
                FadeIn(text[1]),
                Indicate(iter1[exhaust_indices[0]]),
                FadeIn(text[2]),
                Create(iter2),
                FadeIn(text[3]),
                Create(iter3),
                # FadeIn(text[4]),
            ]
        )
