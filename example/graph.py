import ast
import networkx as nx
import matplotlib.pyplot as plt
import glob

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self, ignore_list=None):
        self.graph = nx.DiGraph()
        self.current_function = None
        self.ignore_list = ignore_list if ignore_list is not None else []

    def visit_FunctionDef(self, node):
        if node.name in self.ignore_list:
            self.current_function = None
        else:
            self.current_function = node.name
            self.graph.add_node(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            function_called = node.func.id
            if self.current_function and function_called and function_called not in self.ignore_list:
                self.graph.add_edge(self.current_function, function_called)
        self.generic_visit(node)

def analyze_code(path_pattern, ignore_list=None):
    analyzer = CodeAnalyzer(ignore_list)
    for filename in glob.glob(path_pattern):
        with open(filename, "r") as file:
            node = ast.parse(file.read(), filename=filename)
            analyzer.visit(node)
    return analyzer.graph

def draw_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.show()

if __name__ == "__main__":
    path_pattern = 'schubertpy/*.py'  # Adjust the path to your Python files
    ignore_list = [
        'range', 
        'all',
        'set',
        'sum',
        '__repr__',
        'isinstance',
        '__eq__',
        '__lt__',
        '__len__',
        'sorted',
        'max',
        'tuple',
        'type',
        'hash',
        'int',
        'any',
        'hashable_lru_cache',
        'func',
        'list',
        'apply',
        'len',
        'f',
        'abs',
        'Schur',
        'Exception',
        'open',
        'decode',
        'encode',
        'LinearCombination',
        'symbol',
        'print',
        'min',
        'decorator',
        'unique',
        '__init__',
        '__sub__',
        '__add__',
        '__str__',
        '__pow__',
        '__mul__',
        'fail_no_type',
        'ValueError',
        'translate_schur',
        'yd',
        'OG',
        'Gr',
        'set_type',
        'schub_type',
        'is_operator',
        '_read_csv_transformed',
        'check_bijection_with_permutation',
        'get_type',
        'unique_schur_list',
        'degree_q',
        'generators',
        'IG',
        'wrapper',
        'wraps',
        'cached_func',
        'apply_lc',
        'part_clip',
        'all_kstrict',
        '_itr_kstrict',
        'type_string',
        'TypeError',
        '__rsub__',
        'str',
        'toSchur',
        'isSchur',
        'recursive_list',
        'recursive_apply',
        '__hash__',
        'qact',
        'qtoS',
        'qmult',
        'qgiambelli',
        'qpieriD_inner',
        'pieriD_inner',
        'qpieriB_inner',
        'pieriB_inner',
        'qpieriA_inner',
        'qpieriC_inner',
        'pieriC_inner',
        'schub_classes',
    ]  # Add the names of the functions you want to ignore
    graph = analyze_code(path_pattern, ignore_list)
    draw_graph(graph)
