# -*- encoding: utf-8 -*-

from manim import *
import manim_japanese


class _T:
    def __init__(self, scene, title):
        self.scene = scene
        self.title = Title(title)

    def __enter__(self):
        self.scene.add(self.title)
        return self
    
    def __exit__(self, *args):
        self.scene.remove(self.title)


class RectToCircle(Scene):
    def construct(self):
        pts = []
        N = 100
        for i in range(N):
            pts.append([interpolate(-3.14, 3.14, i / N), 1, 0])
        for i in range(N):
            pts.append([interpolate(-3.14, 3.14, 1 - i / N), 2, 0])
        rect = Polygon(*pts)

        self.add(rect)

        donut = Polygon(*Circle(1).insert_n_curves(20).rotate(1.5 * np.pi).points[::-1], *Circle(2).insert_n_curves(20).rotate(1.5 * np.pi).points)
        self.play(Transform(rect, donut))

        self.wait()


class FlexibleTextMesh(Scene):
    def title(self, title: str) -> _T:
        return _T(self, title)

    def construct(self):
        with self.title('$x$軸がスケールを変えずに円に変換されるとする'):
            axes = Axes(
                x_range=[-4, 4],
                y_range=[-1.2, 1.2],
                x_length=6,
                y_length=4,
            )
            axes.move_to(LEFT * 0.6, RIGHT)

            y0 = Line(*axes.coords_to_point([-3.5, 3.5], [0, 0], [0, 0]).T, color=RED)

            self.play(Create(axes))
            self.play(Create(y0))

            length = (y0.get_right() - y0.get_left())[0]
            circ0 = Circle(length / (2 * np.pi), RED).rotate(1.5 * np.pi).move_to(RIGHT * 2.5, LEFT)
            y0_copied = y0.copy()
            self.add(y0_copied)
            self.play(Transform(y0_copied, circ0, path_func=lambda x, a, b: interpolate(x[::-1], a, b)))

            r_line = Line(circ0.get_center(), circ0.point_at_angle(np.pi / 2))
            self.play(Create(r_line), Create(MathTex('r').next_to(r_line, LEFT, SMALL_BUFF)))

            self.wait(2)

        with self.title('$(0,0)$が円の真上に変換されるとすると、'):
            p = Dot(axes.get_center(), color=YELLOW)
            q = Dot(circ0.point_at_angle(np.pi / 2), color=YELLOW)
            self.play(Create(p), Create(q))

            self.wait(3)

        with self.title('$(\pi r,0)$は円の真下に変換される'):
            self.play(
                MoveAlongPath(p, Line(axes.get_center(), axes.coords_to_point(3.5, 0, 0))),
                MoveAlongPath(q, circ0.get_subcurve(0, 0.5).reverse_points()),
                run_time=2)
            
            line = Line(axes.coords_to_point(0, -0.25, 0), axes.coords_to_point(3.5, -0.25, 0))
            line.add_tip(tip_length=0.25, tip_width=0.25, at_start=True)
            line.add_tip(tip_length=0.25, tip_width=0.25)
            line_len = MathTex(r'\pi r').next_to(line, DOWN, buff=SMALL_BUFF)
            arc = Arc(1.2, np.pi / 2, -np.pi, arc_center=circ0.get_center())
            arc.add_tip(tip_length=0.25, tip_width=0.25, at_start=True)
            arc.add_tip(tip_length=0.25, tip_width=0.25)
            arc_len = MathTex(r'\pi r').next_to(arc, buff=SMALL_BUFF)
            self.play(Create(line), Create(arc))
            self.play(Create(line_len), Create(arc_len))

            self.wait(3)

            self.remove(line, line_len, arc, arc_len, p, q)

        with self.title('このとき$(x,0)$は、'):
            p = Dot(axes.get_center(), color=YELLOW)
            q = Dot(circ0.point_at_angle(np.pi / 2), color=YELLOW)
            self.play(Create(p), Create(q))

            self.play(
                MoveAlongPath(p, Line(axes.get_center(), axes.coords_to_point(3.5 * 0.4, 0, 0))),
                MoveAlongPath(q, circ0.get_subcurve(0.3, 0.5).reverse_points()),
                run_time=2)
            
            p_pos = MathTex('(x,0)').next_to(p, DOWN, SMALL_BUFF)
            self.play(Create(p_pos))

            self.wait(2)

        with self.title('円の真上から円周を$x$動いたところに変換される'):
            arc = Arc(1.2, np.pi / 2, -np.pi * 0.4, arc_center=circ0.get_center())
            arc.add_tip(tip_length=0.2, tip_width=0.2, at_start=True)
            arc.add_tip(tip_length=0.2, tip_width=0.2)
            arc_len = MathTex(r'x').move_to(arc.get_corner(UP + RIGHT), RIGHT)
            self.play(Create(arc), Create(arc_len))

            self.wait(3)

        with self.title(r'円の真上からの角度は$\frac{x}{r}$となるので、'):
            r0 = Line(circ0.get_center(), circ0.point_at_angle(0.1 * np.pi))
            self.play(Create(r0))
            angle = Angle(r_line, r0, other_angle=True).points
            angle = VMobject().set_color(YELLOW).set_points_as_corners(np.concatenate([[circ0.get_center()], angle, [circ0.get_center()]])).set_fill(YELLOW, opacity=1)
            self.play(Create(angle))

            arr_angle = Line(angle.get_center(), [1, -1, 0])
            self.play(Create(arr_angle))

            angle_label = MathTex(r'\frac{x}{r}').next_to(arr_angle, DOWN + LEFT, SMALL_BUFF)
            self.play(Create(angle_label))

            self.wait(2)

        with self.title(r'$\sin$や$\cos$を使って計算できることがわかる'):
            self.wait(3)
            self.remove(angle, p, q, arc, arc_len, p_pos, arr_angle, angle_label)

        Y = 0.5

        with self.title(r'$y$座標が$0$ではない場合は、'):
            y1_prev = Line(*axes.coords_to_point([-3.5, 3.5], [0, 0], [0, 0]).T, color=BLUE)
            y1 = Line(*axes.coords_to_point([-3.5, 3.5], [Y, Y], [0, 0]).T, color=BLUE)

            circ1_prev = circ0.copy().set_color(BLUE).reverse_direction()
            circ1 = Circle(circ0.radius + (y1.points[0][1] - y1_prev.points[0][1]), BLUE).move_arc_center_to(circ0.get_center()).reverse_direction()

            self.play(Create(y1_prev), Create(circ1_prev))
            self.play(Transform(y1_prev, y1), Transform(circ1_prev, circ1))

            self.wait(2)

        with self.title(r'円の半径が$y+r$になり、'):
            circ_y = Line(circ0.point_at_angle(0.5 * np.pi), circ1.point_at_angle(-0.5 * np.pi))
            circ_y_label = MathTex('y').next_to(circ_y, LEFT, SMALL_BUFF)

            y_arr = DoubleArrow(*axes.coords_to_point([-0.5, -0.5], [0, Y], [0, 0]).T, buff=0)
            # y_arr.add_tip(tip_length=0.25, tip_width=0.25, at_start=True)
            # y_arr.add_tip(tip_length=0.25, tip_width=0.25)
            y_arr_label = MathTex('y').next_to(y_arr, LEFT, SMALL_BUFF)

            self.play(Create(circ_y), Create(circ_y_label), Create(y_arr), Create(y_arr_label))

            self.wait(3)
            self.remove(y_arr, y_arr_label)

        with self.title(r'$(x, y)$は円周を'):
            p = Dot(axes.coords_to_point(0, Y, 0), color=YELLOW)
            q = Dot(circ1.point_at_angle(-np.pi / 2), color=YELLOW)
            self.play(Create(p), Create(q))

            self.play(
                MoveAlongPath(p, Line(*axes.coords_to_point([0, 3.5 * 0.4], [Y, Y], [0, 0]).T)),
                MoveAlongPath(q, circ1.get_subcurve(0.75, 0.75 + 0.2)),
                run_time=2)
            
            p_pos = MathTex('(x,y)').next_to(p, DOWN, SMALL_BUFF)
            self.play(Create(p_pos))

            self.wait(2)

        with self.title(r'$x\frac{y+r}{r}$動いたところに変換される'):
            arc = Arc(Y + 1.5, np.pi / 2, -np.pi * 0.4, arc_center=circ1.get_center())
            arc.add_tip(tip_length=0.2, tip_width=0.2, at_start=True)
            arc.add_tip(tip_length=0.2, tip_width=0.2)
            arc_len = MathTex(r'x\frac{y+r}{r}').move_to(arc.get_corner(UP), LEFT)
            self.play(Create(arc), Create(arc_len))

            self.wait(3)

        with self.title(r'円の真上からの角度は$x\frac{y+r}{r}\frac{1}{y+r}=\frac{x}{r}$なので、'):
            r1 = Line(circ0.point_at_angle(0.1 * np.pi), circ1.point_at_angle(-0.1 * np.pi))
            angle = Angle(r_line, r0, other_angle=True).points
            angle = VMobject().set_color(YELLOW).set_points_as_corners(np.concatenate([[circ0.get_center()], angle, [circ0.get_center()]])).set_fill(YELLOW, opacity=1)
            self.play(Create(angle), Create(r1))

            arr_angle = Line(angle.get_center(), [1, -1, 0])
            self.play(Create(arr_angle))

            angle_label = MathTex(r'x\frac{y+r}{r}\frac{1}{y+r}=\frac{x}{r}').next_to(arr_angle, DOWN + LEFT, SMALL_BUFF)
            self.play(Create(angle_label))

            self.wait(5)

        with self.title(r'同様に$\sin$や$\cos$を使って計算できる'):
            self.wait(2)
