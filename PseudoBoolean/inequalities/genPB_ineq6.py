# Constructs .opb to check:
# (x|y)z >= yz
# Where y is ...101010, & is bitwise-AND and | is bitwise-OR.

from circuits_pb import *
import sys
import os

def writeINEQ6(numBits, assist):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    if assist:
        keyFileName = "benchmarks/%darray_alg_ineq6.key" % (numBits)
        opbFileName = "benchmarks/%darray_alg_ineq6.opb" % (numBits)
    else:
        keyFileName = "benchmarks/%darray_ineq6.key" % (numBits)
        opbFileName = "benchmarks/%darray_ineq6.opb" % (numBits)
        
    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')

    # Initialize variable maps
    nextDIMACS = 1

    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
    xoy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xoy',numBits)
    z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',numBits)

    txoyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txoyz",numBits,numBits)      
    cxoyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxoyz",numBits,numBits)
    dxoyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxoyz",numBits,numBits)

    tyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyz",numBits,numBits)      
    cyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyz",numBits,numBits)
    dyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyz",numBits,numBits)

    xoyz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xoyz',2*numBits)
    yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yz',2*numBits)

    for i in range(numBits):
        writeOR(col_constraints,0,xoy[i],x[i],y[i])
        if i % 2 == 0:
            writeFALSE(col_constraints,0,y[i])
        else:
            writeTRUE(col_constraints,0,y[i])

    if not assist:
        writeARRAYMULT(col_constraints, xoy,z,cxoyz,dxoyz,txoyz,xoyz,numBits)
        writeARRAYMULT(col_constraints, y,z,cyz,dyz,tyz,yz,numBits)
    else:
        writeALGEBRA_ARRAYMULT(col_constraints, xoy,z,txoyz,xoyz,numBits)
        writeALGEBRA_ARRAYMULT(col_constraints, y,z,tyz,yz,numBits)

    # Assert (x|y)z < yz
    writeSMALLER_NUMBER(col_constraints,0,xoyz,yz,2*numBits)

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
    writeINEQ6(numBits,True)
    writeINEQ6(numBits,False)













    
