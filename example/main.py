from schubertpy import *

def main():
    # Type A
    gr = Grassmannian(2, 5)
    print(gr.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(gr.qgiambelli('S[2,1]*S[2,1]'))
    print(gr.qtoS('S[2,1]*S[2,1]*S[2,1]'))

    print(gr.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(gr.giambelli('S[2,1]*S[2,1]'))
    print(gr.toS('S[2,1]*S[2,1]*S[2,1]'))

    # Type B
    og = OrthogonalGrassmannian(2, 5)
    print(og.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.qgiambelli('S[2,1]*S[2,1]'))
    print(og.qtoS('S[2,1]*S[2,1]*S[2,1]'))

    print(og.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.giambelli('S[2,1]*S[2,1]'))
    print(og.toS('S[2,1]*S[2,1]*S[2,1]'))

    # Type D
    og = OrthogonalGrassmannian(2, 6)
    print(og.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.qgiambelli('S[2,1]*S[2,1]'))
    print(og.qtoS('S[2,1]*S[2,1]*S[2,1]'))

    print(og.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.giambelli('S[2,1]*S[2,1]'))
    print(og.toS('S[2,1]*S[2,1]*S[2,1]'))

    # Type C
    ig = IsotropicGrassmannian(2, 6)
    print(ig.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(ig.qgiambelli('S[2,1]*S[2,1]'))
    print(ig.qtoS('S[2,1]*S[2,1]*S[2,1]'))

    print(ig.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(ig.giambelli('S[2,1]*S[2,1]'))
    print(ig.toS('S[2,1]*S[2,1]*S[2,1]'))


    gr = Grassmannian(3, 7)
    res = gr.toS('S[2,1]*S[2]*S[1]')
    print(res.schur_expansion())


    # Initializes a Grassmannian object for the Grassmannian Gr(2,4), 
    # which represents the space of all 2-dimensional subspaces 
    # of a 4-dimensional vector space.
    gr = Grassmannian(2, 4)
    sclasses = gr.schub_classes()
    print(sclasses)
    for c1 in sclasses:
        for c2 in sclasses:
            print(c1, "*", c2, "=", gr.qmult(c1, c2))
    
    # Init Multiplication table for the Grassmannian Gr(2,4).
    mTable = MultTable(gr)
    # Prints the multiplication table.
    mTable.print()
    # Another way to print the multiplication table as above command.
    print(mTable)
    # Converts the multiplication table back to a list of lists of LinearCombination objects.
    print(mTable.to_matrix())
    
    # Init Quantum Multiplication table for the Grassmannian Gr(2,4).
    qmTable = QMultTable(gr)
    # Prints the quantum multiplication table.
    qmTable.print()
    # Another way to print the quantum multiplication table as above command.
    print(qmTable)
    # Converts the quantum multiplication table back to a list of lists of LinearCombination objects.
    print(qmTable.to_matrix())


    # Type A
    gr = Grassmannian(2, 7)
    print(gr.mult('S[2,1]', 'S[2,1]'))
    gr = Grassmannian(2, 5)
    print("expected:\t", gr.qmult('S[2,1]', 'S[2,1]'))
    print(gr.qmult_rh('S[2,1]', 'S[2,1]'))


if __name__ == "__main__":
    main()
