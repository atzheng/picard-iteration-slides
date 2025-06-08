from manim_templates import *
from manim import *
import funcy as f
import itertools as it


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


class SequentialBuild(BaseSlide):
    def construct(self):
        self.setup_slide(title="Sequential Simulation ")

        T = 4
        rs, pis, acs, fs, oms, arrows = create_sequence(T)

        anims = []
        for i in range(T):
            # State node and its incoming arrow (except first state)
            state_group = [rs[i]]
            if i > 0:
                state_group.append(arrows[(fs[i - 1], rs[i])])
            anims.append(AnimationGroup(*[FadeIn(obj) for obj in state_group]))

            # Policy node and its incoming arrow
            anims.append(
                AnimationGroup(FadeIn(arrows[(rs[i], pis[i])]), FadeIn(pis[i]))
            )

            # Action node and its incoming arrow
            anims.append(
                AnimationGroup(FadeIn(arrows[(pis[i], acs[i])]), FadeIn(acs[i]))
            )

            # Transition function, outcome, and their arrows
            anims.append(
                AnimationGroup(
                    FadeIn(arrows[(acs[i], fs[i])]),
                    FadeIn(fs[i]),
                    FadeIn(
                        arrows[(rs[i], fs[i])]
                    ),  # Add arc from state to transition
                    FadeIn(arrows[(fs[i], oms[i])]),
                    FadeIn(oms[i]),
                )
            )

        self.play_animations(anims)
