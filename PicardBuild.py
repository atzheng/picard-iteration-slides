from manim_templates import *
from manim import *
import funcy as f

from SequentialBuild import create_sequence

class PicardBuild(BaseSlide):
    def construct(self):
        self.setup_slide(title="Picard Iteration")

        T = 4
        # Create two sequences
        rs1, pis1, acs1, fs1, oms1, arrows1 = create_sequence(T)
        rs2, pis2, acs2, fs2, oms2, arrows2 = create_sequence(T)

        acache = [
            f.lmap(MathTex, [f"a_{i}^{{({j})}}" for i in range(T)])
            for j in range(2)
        ]

        # Create groups for each sequence
        seq1 = VGroup(*rs1, *pis1, *acs1, *fs1, *oms1, *arrows1.get_all_submobjects())
        seq2 = VGroup(*rs2, *pis2, *acs2, *fs2, *oms2, *arrows2.get_all_submobjects())

        # Arrange sequences side by side
        seq1.shift(LEFT * 3.5)
        seq2.shift(RIGHT * 3.5)

        # Create animations for both sequences
        anims = []
        for i in range(T):
            # First sequence
            state_group1 = [rs1[i]]
            if i > 0:
                state_group1.append(arrows1[(fs1[i - 1], rs1[i])])
            anims.append(AnimationGroup(*[FadeIn(obj) for obj in state_group1]))
            
            if i not in [1, 3]:  # Only animate policies for indices 0, 2
                anims.append(AnimationGroup(FadeIn(arrows1[(rs1[i], pis1[i])]), FadeIn(pis1[i])))
                anims.append(AnimationGroup(FadeIn(arrows1[(pis1[i], acs1[i])]), FadeIn(acs1[i])))
            else:
                anims.append(FadeIn(acs1[i]))

            anims.append(
                AnimationGroup(
                    FadeIn(arrows1[(acs1[i], fs1[i])]),
                    FadeIn(fs1[i]),
                    FadeIn(arrows1[(rs1[i], fs1[i])]),
                    FadeIn(arrows1[(fs1[i], oms1[i])]),
                    FadeIn(oms1[i]),
                )
            )

            # Second sequence
            state_group2 = [rs2[i]]
            if i > 0:
                state_group2.append(arrows2[(fs2[i - 1], rs2[i])])
            anims.append(AnimationGroup(*[FadeIn(obj) for obj in state_group2]))
            
            if i not in [0, 2]:  # Only animate policies for indices 1, 3
                anims.append(AnimationGroup(FadeIn(arrows2[(rs2[i], pis2[i])]), FadeIn(pis2[i])))
                anims.append(AnimationGroup(FadeIn(arrows2[(pis2[i], acs2[i])]), FadeIn(acs2[i])))
            else:
                anims.append(FadeIn(acs2[i]))

            anims.append(
                AnimationGroup(
                    FadeIn(arrows2[(acs2[i], fs2[i])]),
                    FadeIn(fs2[i]),
                    FadeIn(arrows2[(rs2[i], fs2[i])]),
                    FadeIn(arrows2[(fs2[i], oms2[i])]),
                    FadeIn(oms2[i]),
                )
            )

        self.play_animations(anims
        )
