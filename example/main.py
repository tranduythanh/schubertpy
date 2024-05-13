from schubertpy import Grassmannian, IsotropicGrassmannian, OrthogonalGrassmannian

def main():
    # Initialize the Grassmannian object with dimensions
    gr = Grassmannian(2, 5)
    print(gr.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(gr.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(gr.qgiambelli('S[2,1]*S[2,1]'))
    print(gr.qmult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(gr.qtoS('S[2,1]*S[2,1]*S[2,1]'))
    print(gr.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(gr.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(gr.giambelli('S[2,1]*S[2,1]'))
    print(gr.mult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(gr.toS('S[2,1]*S[2,1]*S[2,1]'))
    print(gr.dualize('S[1]+S[2]'))


    ig = Grassmannian(2, 6)
    print(ig.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(ig.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(ig.qgiambelli('S[2,1]*S[2,1]'))
    print(ig.qmult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(ig.qtoS('S[2,1]*S[2,1]*S[2,1]'))
    print(ig.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(ig.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(ig.giambelli('S[2,1]*S[2,1]'))
    print(ig.mult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(ig.toS('S[2,1]*S[2,1]*S[2,1]'))
    print(ig.dualize('S[1]+S[2]'))

    og = Grassmannian(2, 6)
    print(og.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(og.qgiambelli('S[2,1]*S[2,1]'))
    print(og.qmult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(og.qtoS('S[2,1]*S[2,1]*S[2,1]'))
    print(og.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(og.giambelli('S[2,1]*S[2,1]'))
    print(og.mult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(og.toS('S[2,1]*S[2,1]*S[2,1]'))
    print(og.dualize('S[1]+S[2]'))

    og = Grassmannian(2, 7)
    print(og.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(og.qgiambelli('S[2,1]*S[2,1]'))
    print(og.qmult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(og.qtoS('S[2,1]*S[2,1]*S[2,1]'))
    print(og.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(og.giambelli('S[2,1]*S[2,1]'))
    print(og.mult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(og.toS('S[2,1]*S[2,1]*S[2,1]'))
    print(og.dualize('S[1]+S[2]'))


    gr = Grassmannian(3, 7)
    res = gr.toS('S[2,1]*S[2]*S[1]')
    print(res.schur_expansion())


    # Initializes a Grassmannian object for the Grassmannian Gr(2,4), 
    # which represents the space of all 2-dimensional subspaces 
    # of a 4-dimensional vector space.
    gr = Grassmannian(2, 4)
    sclasses = gr.schub_classes()
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


if __name__ == "__main__":
    main()
