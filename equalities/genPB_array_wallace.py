from circuits_pb import *
import sys
import os

def writeARRAY_WALLACE(numBits, greater_than=True, t_equals=True):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+6):
        col_constraints[i] = []

    # Choose filename based on settings
    keyFileName = "benchmarks/%darray_wallace" % (numBits)
    opbFileName = "benchmarks/%darray_wallace" % (numBits)
    if greater_than:
        keyFileName += "_greater"
        opbFileName += "_greater"
    else:
        keyFileName += "_less"
        opbFileName += "_less"
    if t_equals:
        keyFileName += "_teq"
        opbFileName += "_teq"
    keyFileName += ".key"
    opbFileName += ".opb"
        
    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')

    nextDIMACS = 1

    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
        
    txy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txy",numBits,numBits)
    txy2, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,'txy2',numBits)      
    cxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxy",numBits,numBits)
    dxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxy",numBits,numBits)
    zeroes, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'zeroes',2*numBits+3)
    c, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'c',2*numBits)

    oxy2, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'oxy2',2*numBits+1)
    oxy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'oxy',2*numBits)

    # Write t-equalities
    if t_equals:
        for i in range(numBits):
            for j in range(numBits):
                if i+j < numBits:
                    writeEQUAL(col_constraints, -1, txy[(i,j)], txy2[(0,i+j,j)])
                else:
                    writeEQUAL(col_constraints, -1, txy[(i,j)], txy2[(0,i+j,numBits-i-1)])

    writeARRAYMULT(col_constraints, x,y,cxy,dxy,txy,oxy,numBits)
    writeWALLACEMULT(col_constraints, x,y,txy2,oxy2,c,zeroes,numBits)

    if greater_than:
        # inequality xy > yx
        writeBIGGER_NUMBER(col_constraints,0,oxy,oxy2,2*numBits)
    else:
        # inequality xy < yx
        writeSMALLER_NUMBER(col_constraints,0,oxy,oxy2,2*numBits)

    # Write all constraints to file
    writeHEADER(f_opb, nextDIMACS, col_constraints)
    for col in range(-1,2*numBits+4):
        for clause in col_constraints[col]:
            f_opb.write(clause)
    f_opb.close()

if __name__ == '__main__':
    if not os.path.exists("benchmarks"):
        os.makedirs("benchmarks")
    # Set t_equals to False to turn off preprocessing t-equalities.
    t_equals = True
    numBits = int(sys.argv[1])
    
    writeARRAY_WALLACE(numBits, True, t_equals)
    writeARRAY_WALLACE(numBits, False, t_equals)














    
