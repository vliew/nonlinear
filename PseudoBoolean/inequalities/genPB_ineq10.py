# Constructs .opb to check:
# (x|y)(z+1) >= yz + x
# Where y is ...101010, & is bitwise-AND and | is bitwise-OR.

from circuits_pb import *
import sys
import os

def writeINEQ10(numBits, assist):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    if assist:
        keyFileName = "benchmarks/%darray_alg_ineq10.key" % (numBits)
        opbFileName = "benchmarks/%darray_alg_ineq10.opb" % (numBits)
    else:
        keyFileName = "benchmarks/%darray_ineq10.key" % (numBits)
        opbFileName = "benchmarks/%darray_ineq10.opb" % (numBits)
        
    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')

    # Initialize variable maps
    nextDIMACS = 1

    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',2*numBits)
    # Pad for addition with yz
    for i in range(numBits,2*numBits):
        writeFALSE(col_constraints,0,x[i])
        
    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
    
    xoy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xoy',numBits+1)
    # Pad for multiplication with (z+1)
    writeFALSE(col_constraints,0,xoy[numBits])
    
    z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',numBits)
    one, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'one',numBits)
    # Fixing value of one
    writeTRUE(col_constraints,-1,one[0])
    for i in range(1,numBits):
        writeFALSE(col_constraints,-1,one[i])
        
    zpl1, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'zpl1',numBits+1)

    # cadd1 for (z+1)
    cadd1, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"cadd1",numBits)
    # cadd2 for yz + x
    cadd2, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"cadd2",2*numBits)

    # Using L to denote LHS multiplier (x|y)(z+1).
    tL, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tL",numBits+1,numBits+1)      
    cL, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cL",numBits+1,numBits+1)
    dL, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dL",numBits+1,numBits+1)

    L, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'L',2*numBits+2)

    tyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyz",numBits,numBits)      
    cyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyz",numBits,numBits)
    dyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyz",numBits,numBits)

    yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yz',2*numBits)
    yzplx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yzplx',2*numBits+1)

    for i in range(numBits):
        writeOR(col_constraints,0,xoy[i],x[i],y[i])
        if i % 2 == 0:
            writeFALSE(col_constraints,0,y[i])
        else:
            writeTRUE(col_constraints,0,y[i])

    if not assist:
        writeARRAYMULT(col_constraints, xoy,zpl1,cL,dL,tL,L,numBits+1)
        writeARRAYMULT(col_constraints, y,z,cyz,dyz,tyz,yz,numBits)
        writeRIPPLECARRYADDER(col_constraints,z,one,cadd1,zpl1,numBits)
        writeRIPPLECARRYADDER(col_constraints,yz,x,cadd2,yzplx,2*numBits)
    else:
        writeALGEBRA_ARRAYMULT(col_constraints, xoy,zpl1,tL,L,numBits+1)
        writeALGEBRA_ARRAYMULT(col_constraints, y,z,tyz,yz,numBits)
        writeRIPPLECARRYADDER(col_constraints,z,one,cadd1,zpl1,numBits)
        writeRIPPLECARRYADDER(col_constraints,yz,x,cadd2,yzplx,2*numBits)

    # Assert (x|y)(z+1) < yz + x
    writeSMALLER_NUMBER(col_constraints,0,L,yzplx,2*numBits+1)

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
    writeINEQ10(numBits,True)
    writeINEQ10(numBits,False)













    
