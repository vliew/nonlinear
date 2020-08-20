# Constructs .opb to check:
# yx >= (x&z)(z&y)
# Where y is ...101010, & is bitwise-AND and | is bitwise-OR.

from circuits_pb import *
import sys
import os

def writeINEQ9(numBits, assist):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    if assist:
        keyFileName = "benchmarks/%darray_alg_ineq9.key" % (numBits)
        opbFileName = "benchmarks/%darray_alg_ineq9.opb" % (numBits)
    else:
        keyFileName = "benchmarks/%darray_ineq9.key" % (numBits)
        opbFileName = "benchmarks/%darray_ineq9.opb" % (numBits)
        
    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')

    # Initialize variable maps
    nextDIMACS = 1

    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
    xny, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xny',numBits)
    ynz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'ynz',numBits)
    z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',numBits)

    txny_ynz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txny_ynz",numBits,numBits)      
    cxny_ynz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxny_ynz",numBits,numBits)
    dxny_ynz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxny_ynz",numBits,numBits)

    tyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyx",numBits,numBits)      
    cyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyx",numBits,numBits)
    dyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyx",numBits,numBits)

    xny_ynz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xny_ynz',2*numBits)
    yx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yx',2*numBits)

    for i in range(numBits):
        writeAND(col_constraints,0,xny[i],x[i],y[i])
        writeAND(col_constraints,0,ynz[i],y[i],z[i])
        if i % 2 == 0:
            writeFALSE(col_constraints,0,y[i])
        else:
            writeTRUE(col_constraints,0,y[i])

    if not assist:
        writeARRAYMULT(col_constraints, xny,ynz,cxny_ynz,dxny_ynz,txny_ynz,xny_ynz,numBits)
        writeARRAYMULT(col_constraints, y,x,cyx,dyx,tyx,yx,numBits)
    else:
        writeALGEBRA_ARRAYMULT(col_constraints, xny,ynz,txny_ynz,xny_ynz,numBits)
        writeALGEBRA_ARRAYMULT(col_constraints, y,x,tyx,yx,numBits)

    # Assert yx < (x&z)(z&y)
    writeSMALLER_NUMBER(col_constraints,0,yx,xny_ynz,2*numBits)

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
    writeINEQ9(numBits,True)
    writeINEQ9(numBits,False)













    
