# Constructs .opb to check:
# yz >= (x&y)z
# Where y is ...101010, & is bitwise-AND and | is bitwise-OR.

from circuits_pb import *
import sys
import os

def writeINEQ7(numBits, assist):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    if assist:
        keyFileName = "benchmarks/%darray_alg_ineq7.key" % (numBits)
        opbFileName = "benchmarks/%darray_alg_ineq7.opb" % (numBits)
    else:
        keyFileName = "benchmarks/%darray_ineq7.key" % (numBits)
        opbFileName = "benchmarks/%darray_ineq7.opb" % (numBits)
        
    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')

    # Initialize variable maps
    nextDIMACS = 1

    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
    xny, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xny',numBits)
    z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',numBits)

    tyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyz",numBits,numBits)      
    cyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyz",numBits,numBits)
    dyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyz",numBits,numBits)

    txnyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txnyz",numBits,numBits)      
    cxnyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxnyz",numBits,numBits)
    dxnyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxnyz",numBits,numBits)

    yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yz',2*numBits)
    xnyz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xnyz',2*numBits)

    for i in range(numBits):
        writeAND(col_constraints,0,xny[i],x[i],y[i])
        if i % 2 == 0:
            writeFALSE(col_constraints,0,y[i])
        else:
            writeTRUE(col_constraints,0,y[i])

    if not assist:
        writeARRAYMULT(col_constraints, y,z,cyz,dyz,tyz,yz,numBits)
        writeARRAYMULT(col_constraints, xny,z,cxnyz,dxnyz,txnyz,xnyz,numBits)
    else:
        writeALGEBRA_ARRAYMULT(col_constraints, y,z,tyz,yz,numBits)
        writeALGEBRA_ARRAYMULT(col_constraints, xny,z,txnyz,xnyz,numBits)

    # Assert yz < (x&y)z
    writeSMALLER_NUMBER(col_constraints,0,yz,xnyz,2*numBits)

    # Write all constraints to file
            
    writeHEADER(f_opb, nextDIMACS, col_constraints)
    for col in range(-1,2*numBits+2):
        for clause in col_constraints[col]:
            f_opb.write(clause)
                
    f_opb.close()


if __name__ == '__main__':
    if not os.path.exists("benchmarks"):
        os.makedirs("benchmarks")

    numBits = int(sys.argv[1])
    writeINEQ7(numBits,True)
    writeINEQ7(numBits,False)













    
