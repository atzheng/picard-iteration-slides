from manim_templates import *
from manim import *
import funcy as f


class Setup(BaseSlide):
    def construct(self):
        self.setup_slide(title="Setup")

        # Table content
        table_data = [
            [VGroup(), Tex(r"{\bf Notation}"), Tex(r"{\bf Example}")],
            [
                Tex(r"\textbf{State space}"),
                MathTex(r"\mathcal{S}"),
                Tex(r"Inventory / Capacity"),
            ],
            [
                Tex(r"\textbf{Action space}"),
                MathTex(r"\mathcal{A}"),
                Tex(r"Fulfillment decision"),
            ],
            [
                Tex(r"\textbf{Disturbance space}"),
                MathTex(r"\Omega"),
                Tex(r"Exogenous demand"),
            ],
            [
                Tex(r"\textbf{Dynamics}"),
                MathTex(
                    r"f : \mathcal{S} \times \mathcal{A} \times \Omega \mapsto \mathcal{S}"
                ),
                Tex(r"Inventory consumption"),
            ],
            [
                Tex(r"\textbf{Policy}"),
                MathTex(r"\pi : \mathcal{S} \times \Omega \mapsto \mathcal{A}"),
                Tex(r"Fulfillment policy"),
            ],
        ]

        # Create table as grid
        table = VGroup(*f.flatten(table_data))
        # for row in table_data:
        #     table.add(*row)

        table.arrange_in_grid(
            rows=6, cols=3, col_alignments=["l"] * 3, buff=(0.45, 0.3)
        ).next_to(self.title, DOWN).set_x(0)

        # Annotation: cheap/expensive
        cheap = Tex(r"{Cheap (e.g., linear)}").set_color(GREEN)
        cheap.next_to(table_data[4][1], UP, buff=0.1).shift(0.5 * RIGHT)

        expensive = Tex(r"{Expensive (e.g., neural network)}").set_color(RED)
        expensive.next_to(table_data[5][1], DOWN, buff=0.4)
        arrow = Arrow(
            start=expensive.get_top(),
            end=table_data[5][1].get_bottom(),
            buff=0.05,
            color=RED,
        )

        # Inputs and goal
        inputs = (
            Tex(
                r"\textbf{Inputs:} Policy $\pi$, initial state $s_0$, disturbance sequence $\omega_0, \omega_1, \ldots \omega_T$"
            )
            .next_to(table, DOWN, buff=1)
            .align_to(self.title, LEFT)
        )

        goal = (
            Tex(
                r"\textbf{Goal:} Compute action sequence $a_0, a_1, \ldots a_T$"
            )
            .next_to(inputs, DOWN, buff=0.3)
            .align_to(inputs, LEFT)
        )

        all = Group(table, cheap, expensive, arrow, inputs, goal)

        self.play_animations(
            [
                # FadeIn(table),
                FadeIn(all),
            ]
        )
