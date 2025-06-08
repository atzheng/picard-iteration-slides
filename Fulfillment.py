from manim_templates import *
from manim import *
import funcy as f


class Fulfillment(BaseSlide):
    def construct(self):
        self.setup_slide(title="A Structured Problem: Fulfillment Optimization")

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
        c1 = MathTex(r"c_1(\omega_t)").next_to(line1.get_center(), UP, buff=0.2)
        c2 = MathTex(r"c_2(\omega_t)").next_to(line2.get_center(), UP, buff=0.2)
        c3 = MathTex(r"c_3(\omega_t)").next_to(line3.get_center(), RIGHT, buff=0.2)

        # Create labels for shopper and warehouses
        shopper_label = Tex(
            r"Order $\omega_t$ \\ for product $i(\omega_t)$"
        ).scale(0.8).next_to(shopper, DOWN, buff=0.2)

        wh1_label = (
            MathTex(r"\text{Inventory }W_{1,t} \\ \text{Capacity }C_{1,t}")
            .scale(0.8)
            .next_to(wh1, RIGHT, buff=0.2)
        )
        wh2_label = (
            MathTex(r"\text{Inventory }W_{2,t} \\ \text{Capacity }C_{2,t}")
            .scale(0.8)
            .next_to(wh2, RIGHT, buff=0.2)
        )
        wh3_label = (
            MathTex(r"\text{Inventory }W_{3,t} \\ \text{Capacity }C_{3,t}")
            .scale(0.8)
            .next_to(wh3, RIGHT, buff=0.2)
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
        )
        graph.scale(0.9).next_to(self.title, DOWN, buff=1).to_edge(LEFT)

        text = (
            VGroup(
                ParTex(r"Products $i \in [I]$, Nodes $j \in [J]$"),
                ParTex(
                    r"\textbf{Policy:} Choose fulfillment node \\ $a_t \in [J] \cup \{0\}$ (0 for unfulfill)"
                ),
                ParTex(r"\textbf{For Picard iteration:} \\"),
                ParTex(
                    r"\textit{Parallelization:} Each process responsible for a set of products; allocate orders by product."
                ),
                ParTex(
                    r"\textit{Initial cache:} Just unfulfill, $a_t^{(0)} = 0$"
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .scale(0.8)
            .next_to(graph, RIGHT, buff=0.3)
            .to_edge(RIGHT)
        )

        # Animation sequence
        animations = [
            FadeIn(shopper),
            AnimationGroup(FadeIn(wh1), FadeIn(wh2), FadeIn(wh3), lag_ratio=0.2),
            AnimationGroup(Create(line1), Create(line2), Create(line3), lag_ratio=0.2),
            AnimationGroup(Write(c1), Write(c2), Write(c3), lag_ratio=0.2),
            AnimationGroup(
                Write(shopper_label),
                Write(wh1_label),
                Write(wh2_label),
                Write(wh3_label),
                lag_ratio=0.2,
            ),
            FadeIn(text),
        ]
        self.play_animations(animations)

        # self.play_animations([
        #     FadeIn(text),
        # ])
