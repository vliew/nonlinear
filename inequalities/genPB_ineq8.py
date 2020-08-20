# Constructs .opb to check:
# (x|z)(z|y) >= yx
# Where y is ...101010, & is bitwise-AND and | is bitwise-OR.

from circuits_pb import *
import sys
import os

def writeINEQ8(numBits, assist):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    if assist:
        keyFileName = "benchmarks/%darray_alg_ineq8.key" % (numBits)
        opbFileName = "benchmarks/%darray_alg_ineq8.opb" % (numBits)
    else:
        keyFileName = "benchmarks/%darray_ineq8.key" % (numBits)
        opbFileName = "benchmarks/%darray_ineq8.opb" % (numBits)
        
    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')

    # Initialize variable maps
    nextDIMACS = 1

    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
    xoy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xoy',numBits)
    yoz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yoz',numBits)
    z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',numBits)

    txoy_yoz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txoy_yoz",numBits,numBits)      
    cxoy_yoz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxoy_yoz",numBits,numBits)
    dxoy_yoz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxoy_yoz",numBits,numBits)

    tyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyx",numBits,numBits)      
    cyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyx",numBits,numBits)
    dyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyx",numBits,numBits)

    xoy_yoz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xoy_yoz',2*numBits)
    yx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yx',2*numBits)

    for i in range(numBits):
        writeOR(col_constraints,0,xoy[i],x[i],y[i])
        writeOR(col_constraints,0,yoz[i],y[i],z[i])
        if i % 2 == 0:
            writeFALSE(col_constraints,0,y[i])
        else:
            writeTRUE(col_constraints,0,y[i])

    if not assist:
        writeARRAYMULT(col_constraints, xoy,yoz,cxoy_yoz,dxoy_yoz,txoy_yoz,xoy_yoz,numBits)
        writeARRAYMULT(col_constraints, y,x,cyx,dyx,tyx,yx,numBits)
    else:
        writeALGEBRA_ARRAYMULT(col_constraints, xoy,yoz,txoy_yoz,xoy_yoz,numBits)
        writeALGEBRA_ARRAYMULT(col_constraints, y,x,tyx,yx,numBits)

    # Assert (x|z)(y|z) < yx
    writeSMALLER_NUMBER(col_constraints,0,xoy_yoz,yx,2*numBits)

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
    writeINEQ8(numBits,True)
    writeINEQ8(numBits,False)













    
