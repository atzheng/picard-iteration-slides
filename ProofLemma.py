from copy import deepcopy
from manim_templates import *
from manim import *
import funcy as f


class ProofLemma(BaseSlide):
    def construct(self):
        self.setup_slide(title="Analyzing Picard Iteration's ``Mistakes''")

        text = (
            VGroup(
                Tex(
                    r"At iteration $k$, time $t$, a Processor's internal state capacity may be:"
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        state_0 = Group(
            Tex(r"\textcircled{1} Sequential $s_t$"),
            ImageMobject("shopper.png").scale(0.2),
            ImageMobject("warehouse.png").scale(0.2),
            ImageMobject("warehouse.png").scale(0.2),
            ImageMobject("warehouse.png").scale(0.2),
        ).arrange(RIGHT, buff=1.2)

        state_0.add(
            Line(
                state_0[1].get_left(),
                state_0[-1].get_right(),
                color=BLACK,
                stroke_width=2,
            ).next_to(state_0[1], DOWN, buff=0.1, aligned_edge=LEFT)
        )

        state_1 = state_0.copy()
        state_2 = state_0.copy()
        # state_2[0] = Tex(r"Processor $s_t$ \\ Underest. Cap.")
        #
        state_0[2].fade(0.8)
        state_2[2].fade(1 - 0.2)
        state_2[3].fade(1 - 0.2)

        states = (
            Group(state_0, state_1, state_2)
            .arrange(DOWN, buff=0.9)
            .scale(0.8)
            .next_to(text, DOWN, buff=0.5)
            .set_x(0)
        )

        # Add lemma box
        lemma_text = Tex(r"{\bf Lemma}: $a_t^{(k)}$ is either correct \textcircled{1}, or an exhausted node \textcircled{2}")
        lemma_box = SurroundingRectangle(
            lemma_text,
            buff=0.3,
            fill_color=GRAY_E,
            fill_opacity=0.1,
            stroke_width=1,
            stroke_color=GRAY_E
        )
        lemma = VGroup(lemma_box, lemma_text)
        lemma.next_to(states, DOWN, buff=1).set_x(0)

        s1_lab = (
            Tex(r"\textcircled{2} Overest. Capacity")
            .scale(0.8)
            .move_to(state_1[0])
        )
        state_1[0].become(s1_lab)

        s2_lab = (
            Tex(r"\textcircled{3} Underest. Capacity")
            .scale(0.8)
            .move_to(state_2[0])
        )
        state_2[0].become(s2_lab)

        a0 = Tex(r"$a_t^{\rm seq}$").next_to(state_0[3], DOWN).scale(0.8)
        a1 = Tex(r"$a_t^{(k)}$").next_to(state_1[2], DOWN).scale(0.8)
        a2 = Tex(r"$a_t^{(k)}$").next_to(state_2[4], DOWN).scale(0.8)

        self.play_animations(
            [
                *f.lmap(FadeIn, text),
                FadeIn(state_0),
                FadeIn(a0),
                FadeIn(state_1),
                FadeIn(a1),
                FadeIn(state_2),
                FadeIn(a2),
                FadeIn(lemma),
            ]
        )

        # Create and animate red X
        line1 = Line(
            state_2.get_left() + LEFT * 0.2,
            state_2.get_right() + RIGHT * 0.2,
            color=RED,
            stroke_width=6
        )
        line2 = Line(
            state_2.get_right() + LEFT * 0.2,
            state_2.get_left() + RIGHT * 0.2,
            color=RED,
            stroke_width=6
        )
        cross = VGroup(line1, line2)
        cross.move_to(state_2)
        
        self.play(Create(cross))
