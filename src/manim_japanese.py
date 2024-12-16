from manim import *

Title.set_default(tex_template=TexTemplate(
    tex_compiler = "xelatex", 
    # tex_compiler = "luatex" でも可
    output_format = ".xdv", 
    preamble = r"""
        \usepackage{amsmath}
        \usepackage{amssymb}
        \usepackage{zxjatype}
        \setCJKmainfont{Sarasa Gothic J}
        \setCJKsansfont{Sarasa Gothic J}
        \setCJKmonofont{Sarasa Mono Slab J}
    """
))

Text.set_default(font='Sarasa Gothic J')