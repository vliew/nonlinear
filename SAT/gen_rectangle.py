# This program generates a rectangular grid of full adders that adds up
# each row (binary number)
#
# This is a very old generator and should be rewritten using circuits.py

# Toggle whether rectangle has unconstrained carry-in bits
hasCarryIn = True

numCols = 5
numRows = 14

# Write c = MAJ(a_0,a_1,a_2) to f_cnf
def writeMAJ(f_cnf,c,a_0,a_1,a_2):
	f_cnf.write("%d -%d -%d 0 \n" %(c,a_0,a_1))
	f_cnf.write("%d -%d -%d 0 \n" %(c,a_0,a_2))
	f_cnf.write("%d -%d -%d 0 \n" %(c,a_1,a_2))
	f_cnf.write("-%d %d %d 0 \n" %(c,a_0,a_1))
	f_cnf.write("-%d %d %d 0 \n" %(c,a_0,a_2))
	f_cnf.write("-%d %d %d 0 \n" %(c,a_1,a_2))

# Write c = AND(a_0,a_1) to f_cnf
def writeAND(f_cnf,c,a_0,a_1):
	f_cnf.write("-%d %d 0 \n" % (c,a_0))
	f_cnf.write("-%d %d 0 \n" % (c,a_1))
	f_cnf.write("%d -%d -%d 0 \n" % (c,a_0,a_1))

# Write d = XOR(a_0,a_1,a_2) to f_cnf	
def writeXOR3(f_cnf,d,a_0,a_1,a_2):
    # Should be all clauses with odd number of negations
	f_cnf.write("-%d %d %d %d 0 \n" %(d,a_0,a_1,a_2))
	f_cnf.write("%d -%d %d %d 0 \n" %(d,a_0,a_1,a_2))
	f_cnf.write("%d %d -%d %d 0 \n" %(d,a_0,a_1,a_2))
	f_cnf.write("%d %d %d -%d 0 \n" %(d,a_0,a_1,a_2))
	f_cnf.write("%d -%d -%d -%d 0 \n" %(d,a_0,a_1,a_2))
	f_cnf.write("-%d %d -%d -%d 0 \n" %(d,a_0,a_1,a_2))
	f_cnf.write("-%d -%d %d -%d 0 \n" %(d,a_0,a_1,a_2))
	f_cnf.write("-%d -%d -%d %d 0 \n" %(d,a_0,a_1,a_2))

# Write d = XOR(a_0,a_1) to f_cnf	
def writeXOR2(f_cnf,d,a_0,a_1):
	# Should be all clauses with odd number of negations
	f_cnf.write("-%d %d %d 0 \n" %(d,a_0,a_1))
	f_cnf.write("-%d -%d -%d 0 \n" %(d,a_0,a_1))
	f_cnf.write("%d -%d %d 0 \n" %(d,a_0,a_1))
	f_cnf.write("%d %d -%d 0 \n" %(d,a_0,a_1))



def writeCNF(keyFileName,cnfFileName):
    f_key = open(keyFileName,'w')
    f_cnf = f = open(cnfFileName,'w')

    nextDIMACS = 1

    t = {}
    t1 = {}
    d = {}
    d1 ={}
    c = {}
    c1 ={}
    o = {}
    o1 = {}
    for i in range(numCols):
        for j in range(numRows):
            t[(i,j)] = nextDIMACS
            f_key.write("DEFINING %d FOR t_%d_%d \n" % (nextDIMACS, i,j))
            nextDIMACS += 1
            
            d[(i,j)] = nextDIMACS
            f_key.write("DEFINING %d FOR d_%d_%d \n" % (nextDIMACS, i,j))
            nextDIMACS += 1

            c[(i-1,j)] = nextDIMACS
            f_key.write("DEFINING %d FOR c_%d_%d \n" % (nextDIMACS, i-1,j))
            nextDIMACS += 1

            c1[(i-1,j)] = nextDIMACS
            f_key.write("DEFINING %d FOR c1_%d_%d \n" % (nextDIMACS, i-1,j))
            nextDIMACS += 1
                
            t1[(i,j)] = nextDIMACS
            f_key.write("DEFINING %d FOR t1_%d_%d \n" % (nextDIMACS, i,j))
            nextDIMACS += 1
            
            d1[(i,j)] = nextDIMACS
            f_key.write("DEFINING %d FOR d1_%d_%d \n" % (nextDIMACS, i,j))
            nextDIMACS += 1

        
    f_key.write("\n WRITING o AND o1 VARIABLES \n")
    for i in range(numCols):
        o[i] = nextDIMACS
        f_key.write("DEFINING %d FOR o_%d \n" % (nextDIMACS, i))
        nextDIMACS += 1
        
        o1[i] = nextDIMACS
        f_key.write("DEFINING %d FOR o1_%d \n" % (nextDIMACS, i))
        nextDIMACS += 1

    f_cnf.write("p cnf %d 2085 \n" % nextDIMACS)


    # Tableau equality constraints so the rows appear in reverse order
    # in the alternate circuit
    for i in range(numCols):
        for j in range(numRows):
            f_cnf.write("%d -%d 0 \n" % (t[(i,j)],t1[(i,numRows-j-1)]))
            f_cnf.write("-%d %d 0 \n" % (t[(i,j)],t1[(i,numRows-j-1)]))            

    # First row: d_i0 = t_i0
    f_cnf.write("c Writing first row's contraints: d_i0 = t_i0 \n")
    for i in range(numCols):
        f_cnf.write("-%d %d 0 \n" %(d[(i,0)],t[(i,0)]))
        f_cnf.write("%d -%d 0 \n" %(d[(i,0)],t[(i,0)]))
        
        # bizarro version
        f_cnf.write("-%d %d 0 \n" %(d1[(i,0)],t1[(i,0)]))
        f_cnf.write("%d -%d 0 \n" %(d1[(i,0)],t1[(i,0)]))

    # The inside d variables
    f_cnf.write("c d_ij = d_{i,j-1} + c_i-1,j + t_ij \n")
    for i in range(numCols):
        if i==0 and (not hasCarryIn):
            for j in range(1,numRows):
                writeXOR2(f_cnf,d[(i,j)],d[(i,j-1)],t[(i,j)])
                writeXOR2(f_cnf,d1[(i,j)],d1[(i,j-1)],t1[(i,j)])
        else:
            for j in range(1,numRows):
                writeXOR3(f_cnf,d[(i,j)],d[(i,j-1)],c[(i-1,j)],t[(i,j)])
                writeXOR3(f_cnf,d1[(i,j)],d1[(i,j-1)],c1[(i-1,j)],t1[(i,j)])

    # The inside c variables
    f_cnf.write("c c_ij = MAJ(d_{i,j-1}, c_i-1,j, t_ij) \n")
    for i in range(numCols-1):
        if i==0 and (not hasCarryIn):
            for j in range(1,numRows):
                writeAND(f_cnf,c[(i,j)],d[(i,j-1)],t[(i,j)])
                writeAND(f_cnf,c1[(i,j)],d1[(i,j-1)],t1[(i,j)])
        else:
            for j in range(1,numRows):
                writeMAJ(f_cnf,c[(i,j)],d[(i,j-1)],c[(i-1,j)],t[(i,j)])
                writeMAJ(f_cnf,c1[(i,j)],d1[(i,j-1)],c1[(i-1,j)],t1[(i,j)])

    # Outputs: o_i = d_0_i
    f_cnf.write("c Outputs: o_i = d_i_{numRows-1} \n")
    for i in range(numCols):
        f_cnf.write("%d -%d 0 \n" % (o[i],d[(i,numRows-1)]))
        f_cnf.write("-%d %d 0 \n" % (o[i],d[(i,numRows-1)]))

        f_cnf.write("%d -%d 0 \n" % (o1[i],d1[(i,numRows-1)]))
        f_cnf.write("-%d %d 0 \n" % (o1[i],d1[(i,numRows-1)]))
        
    # All but the most significant outputs agree
    f_cnf.write("%d %d 0 \n" % (o[numCols-1], o1[numCols-1]))
    f_cnf.write("-%d -%d 0 \n" % (o[numCols-1], o1[numCols-1]))
    for i in range(numCols-1):
        f_cnf.write("%d -%d 0 \n" % (o[i], o1[i]))
        f_cnf.write("-%d %d 0 \n" % (o[i], o1[i]))
    return

cnfFileName = "%dby%d_rectangle.cnf" % (numCols,numRows)
keyFileName = "%dby%d_rectangle.key" % (numCols,numRows)
writeCNF(keyFileName,cnfFileName)

