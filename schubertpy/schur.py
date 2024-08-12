import ast
from typing import *

import matplotlib.pyplot as plt
import sympy as sp

from .const import *
from .partition import *
from .util import *

class Schur(object):
    def __init__(self, p: Union[List[int], sp.Expr, str, 'Schur']):
        # Set self.p to p or [] if p is None
        if isinstance(p, (list, tuple)):
            self.p = p if p is not None else []
            return
        if isinstance(p, Schur):
            self.p = p.p
            return
        p = toSchur(p)
        self.p = p.p

    def __str__(self):
        return f"S{self.p}".replace(' ', '')

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        # Check if 'other' is instance of Schur and compare
        if isinstance(other, Schur):
            return self.p == other.p
        return NotImplemented

    def __lt__(self, other):
        # Check if 'other' is instance of Schur and compare
        if isinstance(other, Schur):
            return self.p < other.p
        return NotImplemented
    
    def __hash__(self):
        return hash(str(self.p))
    

    def __add__(self, other):
        if isinstance(other, Schur):
            return self.symbol() + other.symbol()
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return self.symbol() + other
        if other.expr and isinstance(other.expr, sp.Expr):
            return self.symbol() + other.expr
        raise ValueError(f"Invalid type for addition: {type(other)}")
    
    __radd__ = __add__
    
    def __mul__(self, other):
        if isinstance(other, Schur):
            return self.symbol() * other.symbol()
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return self.symbol() * other
        if other.expr and isinstance(other.expr, sp.Expr):
            return self.symbol() * other.expr
        raise ValueError(f"Invalid type for addition: {type(other)}")
    
    __rmul__ = __mul__
    
    def __pow__(self, other):
        if isinstance(other, Schur):
            return self.symbol() ** other.symbol()
        if isinstance(other, (int, float, sp.Expr, sp.Number)):
            return self.symbol() ** other
        if other.expr and isinstance(other.expr, sp.Expr):
            return self.symbol() ** other.expr
        raise ValueError(f"Invalid type for addition: {type(other)}")

    def symbol(self) -> sp.Symbol:
        return sp.parse_expr(self.__str__().translate(ftable))

    def partition(self) -> List[int]:
        return self.p
    
    def has_part_zero_padding(self) -> bool:
        return part_clip(self.p) != self.p
    
    def print_partition(self) -> None:
        """Prints the partition as a Young tableau to the console using ASCII characters."""
        for row_length in self.p:
            print("[ ]" * row_length)

    def latex(self) -> str:
        """Exports the partition as a LaTeX tikzpicture with 5mm squares."""
        return self._generate_tikzpicture(standalone=False)

    def latex_standalone(self) -> str:
        """Exports the partition as a standalone LaTeX document with a tikzpicture of 5mm squares."""
        return self._generate_tikzpicture(standalone=True)

    def _generate_tikzpicture(self, standalone: bool) -> str:
        """Helper method to generate TikZ picture code."""
        tikz_lines = []
        if standalone:
            tikz_lines.extend([
                "\\documentclass{standalone}",
                "\\usepackage{tikz}",
                "\\begin{document}"
            ])
        tikz_lines.extend([
            "\\begin{tikzpicture}",
            "\\usetikzlibrary{shapes.geometric}",
            "\\tikzstyle{every node}=[draw, minimum size=5mm, inner sep=0pt]",
            f"\\node[draw=none, anchor=south] at ({len(self.p) * 2.5}mm, 5mm) {{$S_{{{tuple(self.p)}}}$}};"
        ])
        y = 0
        for row_length in self.p:
            x = 0
            for _ in range(row_length):
                tikz_lines.append(f"\\node at ({x * 5}mm, {-y * 5}mm) {{}};")
                x += 1
            y += 1
        tikz_lines.append("\\end{tikzpicture}")
        if standalone:
            tikz_lines.append("\\end{document}")
        return "\n".join(tikz_lines)
    
    def plot_partition(self):
        """Plots the partition using Matplotlib."""
        max_row_length = max(self.p) if self.p else 0
        num_rows = len(self.p)
        
        fig_width = max_row_length * 1  # Adjust the scale factor as needed
        fig_height = num_rows * 1 + 1  # Adjust the scale factor to add space for the label
        
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        
        # Add the label above the partition
        label = f"$S_{{{tuple(self.p)}}}$"
        plt.text(max_row_length / 2, 1, label, ha='center', va='bottom', fontsize=24)
        
        for y, row_length in enumerate(self.p):
            for x in range(row_length):
                rect = plt.Rectangle((x, -y), 1, 1, fill=None, edgecolor='black')
                ax.add_patch(rect)
                
        ax.set_aspect('equal')
        ax.set_xlim(-1, max_row_length + 1)
        ax.set_ylim(-num_rows - 1, 1)
        plt.axis('off')
        return fig, ax

    def export_png(self, filename: str) -> None:
        """Exports the partition as a PNG image."""
        fig, ax = self.plot_partition()
        plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
    
    def to_polinomial_str(self, n) -> str:
        """
        Converts the Schur object to a polynomial expression.

        Parameters:
        - n: int, the number of variables of the polynomial.

        Returns:
        - sp.Expr: The polynomial expression.

        """
        res = SchurPol(n, self.partition())
        return str(res.expr).replace('_', '').replace('**', '^')

def unique_schur_list(schur_list: List[Schur]):
    return  sorted(list(set(schur_list)))



def isSchur(expr: sp.Expr) -> bool:
    return expr.is_Symbol and str(expr).startswith('S')


def translate_schur(sym: Union[sp.Symbol, str]) -> str:
    # Convert symbol back to string and translate using reverse table
    return str(sym).translate(btable)

def toSchur(sym: Union[sp.Symbol, str]) -> Schur:
        # Convert symbol back to string and translate using reverse table
        parsed_str = str(sym).translate(btable).replace('S', '')
        # Parse the string back into a list structure
        pl = ast.literal_eval(parsed_str)
        if isinstance(pl, list) and all(isinstance(i, list) or isinstance(i, int) for i in pl):
            return Schur(pl)
        raise ValueError("Input string does not represent a list of lists")
        