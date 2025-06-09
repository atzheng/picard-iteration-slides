from manim_templates import *
from manim import *
import funcy as f

from SequentialBuild import create_sequence


class PicardBuild(BaseSlide):
    def construct(self):
        self.setup_slide(title="Parallelizing Simulation with Picard Iteration")

        T = 4
        # Create two sequences
        rs1, pis1, acs1, fs1, oms1, arrows1 = create_sequence(T)
        rs2, pis2, acs2, fs2, oms2, arrows2 = create_sequence(T)
        # Create groups for each sequence
        seq1 = VGroup(
            *rs1, *pis1, *acs1, *fs1, *oms1, *arrows1.get_all_submobjects()
        )
        seq2 = VGroup(
            *rs2, *pis2, *acs2, *fs2, *oms2, *arrows2.get_all_submobjects()
        )

        # Arrange sequences side by side
        # Create time labels
        time_labels = VGroup(
            *[
                MathTex(f"t={i}")
                .rotate(90 * DEGREES)
                .next_to(rs1[i], LEFT, buff=0.5)
                .set_color(BLUE_E if i % 2 == 0 else "#800000")
                for i in range(T)
            ]
        )

        seq1.shift(LEFT * 3.5 + 0.5 * DOWN)
        seq2.shift(RIGHT * 3.5 + 0.5 * DOWN)
        time_labels.shift(LEFT * 3.5 + 0.5 * DOWN)

        acache1 = VGroup(
            *[
                VGroup(
                    *[
                        MathTex(f"a_{i}^{{({j})}}").move_to(acs1[i])
                        for i in range(T)
                    ]
                )
                for j in range(3)
            ]
        )

        acache2 = VGroup(
            *[
                VGroup(
                    *[
                        MathTex(f"a_{i}^{{({j})}}").move_to(acs2[i])
                        for i in range(T)
                    ]
                )
                for j in range(3)
            ]
        )

        acache1[1].set_color(BLUE_E)
        acache2[1].set_color("#800000")
        # acache1[2].set_color(BLUE_E)
        # acache2[2].set_color("#800000")

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

        # Create headings
        heading1 = Tex("Processor 1", color=BLUE_E).next_to(seq1, UP, buff=0.5)
        heading2 = Tex("Processor 2", color="#800000").next_to(
            seq2, UP, buff=0.5
        )

        # Create background rectangles for rows
        # For sequence 1 (rows 0 and 2)
        bg1 = VGroup()
        for i in [0, 2]:
            rect = Rectangle(
                width=seq1.width,
                height=1.1,
                color=BLUE_E,
                fill_opacity=0.1,
                stroke_width=0,
            )
            rect.move_to(VGroup(rs1[i], oms1[i]))
            bg1.add(rect)

        # For sequence 2 (rows 1 and 3)
        bg2 = VGroup()
        for i in [1, 3]:
            rect = Rectangle(
                width=seq2.width,
                height=1.1,
                color="#800000",
                fill_opacity=0.1,
                stroke_width=0,
            )
            rect.move_to(VGroup(rs2[i], oms2[i]))
            bg2.add(rect)

        sync_cps = VGroup(
            acache2[1][1].copy(),
            acache2[1][3].copy(),
            acache1[1][0].copy(),
            acache1[1][2].copy(),
        )

        # Create a group of all elements except title
        all_elements = VGroup(
            seq1,
            seq2,
            heading1,
            heading2,
            bg1,
            bg2,
            acache1,
            acache2,
            acache1_bg,
            acache2_bg,
            sync_cps,
            time_labels,
        )
        all_elements.scale(0.7).next_to(self.title, DOWN, buff=0.3).to_edge(
            RIGHT
        )

        text = LatexItems(
            r"\item Assign each process a set of times",
            r"\item Start with an action cache $a_t^{(0)}$ (initial ``guess'')",
            r"\item Each process simulates as usual... but only update cache for assigned times",
            r"\item Synchronize caches, iterate",
            itemize="enumerate",
            page_width=r"0.4\textwidth",
        ).scale(0.65)

        text.next_to(all_elements, LEFT).to_edge(LEFT)

        anims = [
            # First text item and initial setup
            AnimationGroup(
                FadeIn(heading1),
                FadeIn(heading2),
            ),
            FadeIn(text[0]),
            AnimationGroup(
                FadeIn(time_labels),
                FadeIn(bg1),
                FadeIn(bg2),
            ),
            # Second text item and cache initialization
            FadeIn(text[1]),
            AnimationGroup(
                FadeIn(acache1[0], acache1_bg),
                FadeIn(acache2[0], acache2_bg),
            ),
            # Third text item before main simulation
            FadeIn(text[2]),
        ]

        for i in range(T):
            # First sequence
            state_group1 = [rs1[i]]
            if i > 0:
                state_group1.append(arrows1[(fs1[i - 1], rs1[i])])
            anims.append(AnimationGroup(*[Create(obj) for obj in state_group1]))

            if i not in [1, 3]:  # Only animate policies for indices 0, 2
                anims.append(
                    AnimationGroup(
                        Create(arrows1[(rs1[i], pis1[i])]), Create(pis1[i])
                    )
                )
                anims.append(
                    AnimationGroup(
                        Create(arrows1[(pis1[i], acs1[i])]),
                        ReplacementTransform(acache1[0][i], acache1[1][i]),
                        Indicate(acache1[1][i]),
                    )
                )

            anims.append(
                AnimationGroup(
                    Create(arrows1[(acs1[i], fs1[i])]),
                    Create(fs1[i]),
                    Create(arrows1[(rs1[i], fs1[i])]),
                    Create(arrows1[(fs1[i], oms1[i])]),
                    Create(oms1[i]),
                )
            )

            # Second sequence
            state_group2 = [rs2[i]]
            if i > 0:
                state_group2.append(arrows2[(fs2[i - 1], rs2[i])])
            anims.append(AnimationGroup(*[Create(obj) for obj in state_group2]))

            if i not in [0, 2]:  # Only animate policies for indices 1, 3
                anims.append(
                    AnimationGroup(
                        Create(arrows2[(rs2[i], pis2[i])]), Create(pis2[i])
                    )
                )
                anims.append(
                    AnimationGroup(
                        Create(arrows2[(pis2[i], acs2[i])]),
                        ReplacementTransform(acache2[0][i], acache2[1][i]),
                        Indicate(acache2[1][i]),
                    )
                )

            anims.append(
                AnimationGroup(
                    Create(arrows2[(acs2[i], fs2[i])]),
                    Create(fs2[i]),
                    Create(arrows2[(rs2[i], fs2[i])]),
                    Create(arrows2[(fs2[i], oms2[i])]),
                    Create(oms2[i]),
                )
            )

        anims.extend(
            [
                # Fourth text item before synchronization
                FadeIn(text[3]),
                AnimationGroup(
                    FadeOut(acache1[0][1]),
                    FadeOut(acache1[0][3]),
                    FadeOut(acache2[0][0]),
                    FadeOut(acache2[0][2]),
                ),
                AnimationGroup(
                    sync_cps[0].copy().animate.move_to(acache1[1][1]),
                    sync_cps[1].copy().animate.move_to(acache1[1][3]),
                    sync_cps[2].copy().animate.move_to(acache2[1][0]),
                    sync_cps[3].copy().animate.move_to(acache2[1][2]),
                ),
            ]
        )

        # anims.append(
        #     # AnimationGroup(
        #     #     acache1[1].animate.set_color(BLACK),
        #     #     acache2[1].animate.set_color(BLACK),
        #     #     seq1.animate.set_opacity(0.2),
        #     #     seq2.animate.set_opacity(0.2),
        #     # )
        # )

        obs = (
            VGroup(
                Tex(r"Converges in at most $T$ iterations (induction)"),
                Tex(
                    r"For structured problems, can be $\ll T$ -- focus of remaining talk"
                ),
                Tex(r"Independent $\pi$ executions can be batched on GPU"),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .next_to(text, DOWN, buff=0.8, aligned_edge=LEFT)
        )

        anims.extend(f.lmap(FadeIn, obs))
        anims.extend(
            [
                AnimationGroup(
                    Indicate(pis1[0]),
                    Indicate(pis2[1])
                ),
                AnimationGroup(
                    Indicate(pis1[2]),
                    Indicate(pis2[3])
                ),
            ]
        )

        self.play_animations(anims)
