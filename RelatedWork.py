#!/usr/bin/env python3

from manim_templates import *
from manim import *
import funcy as f


class RelatedWork(BaseSlide):
    def construct(self):
        self.setup_slide(
            title="The Pattern: Cheap Drafts, Parallel Verifiers"
        )
        # self.title.scale(0.9).to_corner(UP + LEFT)
        text = TexBox(
            r"""
            For a sequence of expensive computations:
            1. Generate a draft using a cheap surrogate
            2. Verify each step of the draft in parallel 
            3. Identify first error, repeat
            """,
            width=4,
        ).next_to(self.title, DOWN, buff=0.3, aligned_edge=LEFT)

        text2 = TexBox(
            r"""

            {\bf Speeding up Policy Simulation in Supply Chain RL}, Farias et. al., ICML 2025
            $\bullet$ Expensive computations: policy executions
            $\bullet$ Draft policy: initial cache, parallel rollouts
            
            {\bf Break the sequential dependency of LLM inference using lookahead decoding.} Fu et. al., ICML 2024
            $\bullet$ Expensive computations: LLM inference
            $\bullet$ Draft policy: Cheaper LLM

            {\bf Speculative Actions: A Lossless Framework for Faster Agentic Systems.} Ye et. al., ICLR 2026.
            $\bullet$ Expensive computations: API/Tool calls
            $\bullet$ Draft policy: Cheaper LLM 
            """,
            width=9,
        ).next_to(text, RIGHT, aligned_edge=UP, buff=0.3)

        self.play_animations([*map(FadeIn, text), *map(FadeIn, text2)])
