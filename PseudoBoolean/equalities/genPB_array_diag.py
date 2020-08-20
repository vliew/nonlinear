from circuits_pb import *
import sys
import os

def writeARRAY_DIAG(numBits, greater_than=True):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    # Choose filename based on settings
    keyFileName = "benchmarks/%darray_diag" % (numBits)
    opbFileName = "benchmarks/%darray_diag" % (numBits)
    if greater_than:
        keyFileName += "_greater"
        opbFileName += "_greater"
    else:
        keyFileName += "_less"
        opbFileName += "_less"
    keyFileName += ".key"
    opbFileName += ".opb"

    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')


    # Initialize variable maps
    nextDIMACS = 1

    # Create the variables

    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)

    t1, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"t",numBits+1, numBits)  
    c, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"c",numBits,numBits)
    c1, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"c1",numBits+1, numBits) 
    d, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"d",numBits,numBits)
    d1, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"d1",numBits+1, numBits)
    o, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'o',2*numBits)
    o1, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'o1',2*numBits)

    writeARRAYMULT(col_constraints, x,y,c,d,t1,o,numBits)
    # tvars defined by arraymult already.
    writeDIAGSUM(col_constraints,c1,d1,t1,o1,numBits)

    if greater_than:
        # inequality o > o1
        writeBIGGER_NUMBER(col_constraints,0,o,o1,2*numBits)
    else:
        # inequality o < o1
        writeSMALLER_NUMBER(col_constraints,0,o,o1,2*numBits)

    # Write all constraints to file
    writeHEADER(f_opb, nextDIMACS, col_constraints)
    for col in col_constraints:
        for clause in col_constraints[col]:
            f_opb.write(clause)
    f_opb.close()

if __name__ == '__main__':
    if not os.path.exists("benchmarks"):
        os.makedirs("benchmarks")
    numBits = int(sys.argv[1])
    
    writeARRAY_DIAG(numBits, True)
    writeARRAY_DIAG(numBits, False)










    
