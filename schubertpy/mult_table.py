from abc import ABC, abstractmethod
from typing import *
import pandas as pd
from .lc import *
from .abstract_grassmannian import *

class AbstractMultTable(ABC):
    gr = AbstractGrassmannian
    df = pd.DataFrame

    def __init__(self, gr: AbstractGrassmannian):
        """
        Initializes the multiplication table for a given Grassmannian.
    
        This constructor takes an AbstractGrassmannian object, computes the Schubert classes associated with it,
        and populates a multiplication table based on these classes. The table is stored as a pandas DataFrame
        with both rows and columns labeled by the Schubert classes.
    
        Parameters:
        - gr (AbstractGrassmannian): The Grassmannian object for which the multiplication table is to be created.
    
        Attributes:
        - gr (AbstractGrassmannian): Stores the provided Grassmannian object.
        - df (pd.DataFrame): A pandas DataFrame representing the multiplication table, with Schubert classes as both
          row and column labels, and entries representing the product of these classes.
        """
        self.gr = gr
        # Retrieve the Schubert classes from the Grassmannian.
        labels = self.gr.schub_classes() 
        n = len(labels)  
        
        # Initialize an empty matrix
        table = [[0] * n for _ in range(n)]
        
        # Populate the multiplication table
        for i in range(n):
            for j in range(n):
                # Compute the product of Schubert classes.
                table[i][j] = self.mult(labels[i], labels[j])  
        
        # Create a DataFrame from the matrix.
        self.df = pd.DataFrame(table, index=labels, columns=labels)

    @abstractmethod
    def mult(self):
        pass

    def print(self):
        """
        Prints the multiplication table in a readable format.

        This method applies a transformation to the DataFrame such that each cell is converted to a string representation.
        Cells with `None` values are replaced with an empty string for clarity. The resulting DataFrame is then printed
        to the standard output.
        """
        df = self.df.applymap(lambda x: str(x) if x is not None else "")
        print(df)

    def to_matrix(self) -> List[List]:
        """Converts the DataFrame back to a list of lists of LinearCombination objects"""
        return self.df.values.tolist()

    def __str__(self):
        return str(self.df)

    def __repr__(self):
        return str(self.df)


class MultTable(AbstractMultTable):
    def __init__(self, gr: AbstractGrassmannian):
        super().__init__(gr)

    def mult(self, a: List[int], b: List[int]) -> LinearCombination:
        return self.gr.mult(a, b)

    
    

class QMultTable(AbstractMultTable):
    def __init__(self, gr: AbstractGrassmannian):
        super().__init__(gr)
    
    def mult(self, a: List[int], b: List[int]) -> LinearCombination:
        return self.gr.qmult(a, b)