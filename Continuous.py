#!/usr/bin/env python3

from manim_templates import *
from manim import *
import funcy as f

class Continuous(BaseSlide):
    def construct(self):
        self.setup_slide(title="Picard for Continuous Control")

        text = TexBox(
            r"""
            Inputs to Picard iteration:
            1. The initial action cache $a^{(0)}$
            2. Assignment of timesteps to processors
            
            Absent further structure, simply assign each timestep to a different processor.

            I.e., at iteration $k$:
            
            $$a_{t}^{(k)} &= \pi(s_{t}^{(k)}, \omega_{t}) \\ s_{t+1}^{(k)} &= f(s_{t}^{(k)}, a_{t}^{(k-1)}, \omega_{t})$$
            """,
            width=6.5,
        ).next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)

        text2 = TexBox(
            r"""
            {\bf Assumption} (smoothness): For all $s, s', \tilde{s}^{\prime} \in \mathcal{S}$ and $\omega \in \Omega$, it holds that:
            $$\| f(s', \pi(\tilde{s}^{\prime},\omega), \omega) - f(s, \pi(s, \omega), \omega) \| \leq \| s - s'\| + \kappa \|\tilde{s}^{\prime}  - s\|.$$

            {\bf Proposition}: Picard iteration converges at the rate
            $$\| s_{t}^{(k)} - s_{t}^{\mathrm{seq}}\| \leq (e \kappa t / k)^{k} s_{\mathrm{max}}$$

            where $s_{\rm max} = \max_{s, s' \in \mathcal{S}} \| s - s'\|.$
            """,
            width=6.5,
        ).next_to(text, RIGHT, aligned_edge=UP)

        prop = text2[2:]
        prop.add_background_rectangle(buff=0.2, color=GRAY)
        # prop[1].fade(0.5)

        self.play_animations(
            [
                *map(FadeIn, text),
                FadeIn(text2[:2]),
                FadeIn(prop),
            ]
        )
