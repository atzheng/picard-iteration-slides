from manim_templates import *
from manim import *
import funcy as f
import itertools as it


class SequentialBuild(BaseSlide):
    def construct(self):
        self.setup_slide(title="Sequential Simulation ")

        T = 4

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
        ).arrange_in_grid(n_rows=4, n_cols=5, buff=1)

        rs, pis, acs, fs, oms = [
            [seq[5 * i + j] for i in range(T)] for j in range(5)
        ]

        for pi in pis:
            pi.add_background_rectangle(color=RED, buff=0.2)

        for fx in fs:
            fx.add_background_rectangle(color=GREEN, buff=0.2)

        arrows = VDict(
            it.chain.from_iterable([
                [
                    ((s, pi), Arrow(s.get_right(), pi.get_left(), buff=0.1))
                    for s, pi in zip(rs, pis)
                ],
                [
                    ((pi, ac), Arrow(pi.get_right(), ac.get_left(), buff=0.1))
                    for pi, ac in zip(pis, acs)
                ],
                [
                    ((ac, f), Arrow(ac.get_right(), f.get_left(), buff=0.1))
                    for ac, f in zip(acs, fs)
                ],
                [
                    ((f, om), Arrow(om.get_left(), f.get_right(), buff=0.1))
                    for f, om in zip(fs, oms)
                ],
                [
                    ((f, s_next), Arrow(f.get_bottom(), s_next.get_top(), buff=0.1))
                    for f, s_next in zip(fs[:-1], rs[1:])
                ]
            ])
        )

        rs.append(VGroup())
        arrows[(fs[-1], rs[-1])] = VGroup()

        anims = []
        for i in range(T):
            anims.append(FadeIn(rs[i], run_time=0.5))


        self.play_animations(
            [
                *map(
                    FadeIn,
                    it.chain.from_iterable([
                        [rs[i],
                         arrows[(rs[i], pis[i])],
                         pis[i],
                         arrows[(pis[i], acs[i])],
                         acs[i],
                         oms[i],
                         arrows[(acs[i], fs[i])],
                         arrows[(fs[i], oms[i])],
                         fs[i],
                         arrows[(fs[i], rs[i + 1])],
                         ]
                        for i in range(T)
                    ]),
                ),
                # FadeIn(arrows),
            ]
        )
