from circuits_pb import *
import sys
import os

def writeWALLACE_SPEC(numBits, greater_than=True, t_equals=True, tvars=False):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    # Choose filename based on settings
    keyFileName = "benchmarks/%dwallace_spec" % (numBits)
    opbFileName = "benchmarks/%dwallace_spec" % (numBits)
    if greater_than:
        keyFileName += "_greater"
        opbFileName += "_greater"
    else:
        keyFileName += "_less"
        opbFileName += "_less"
    if tvars:
        keyFileName += "_tvars"
        opbFileName += "_tvars"	
    keyFileName += ".key"
    opbFileName += ".opb"

    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')


    # Initialize variable maps
    nextDIMACS = 1

    # Create the variables
    xy2, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xy2',2*numBits)
    xy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xy',2*numBits+1)

    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)


    txy, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,'txy2',numBits)
    txy2, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txy",numBits,numBits)
    zeroes, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'zeroes',2*numBits+3)
    c, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'c',2*numBits)



    # Write t-equalities
    if t_equals:
        for i in range(numBits):
            for j in range(numBits):
                if i+j < numBits:
                    writeEQUAL(col_constraints, -1, txy2[(i,j)], txy[(0,i+j,j)])
                else:
                    writeEQUAL(col_constraints, -1, txy2[(i,j)], txy[(0,i+j,numBits-i-1)])
    if not tvars:
        writeWALLACEMULT(col_constraints, x,y,txy,xy,c,zeroes,numBits)
        writeALGEBRA_ARRAYMULT(col_constraints, x,y,txy2,xy2,numBits)
    else:
        writeWALLACESUM(col_constraints, txy,xy,c,zeroes,numBits)
        writeALGEBRA_ARRAYSUM(col_constraints, txy2,xy2,numBits)        

    if greater_than:
        # inequality xy > xy2
        writeBIGGER_NUMBER(col_constraints,0,xy,xy2,2*numBits)
    else:
        # inequality xy < xy2
        writeSMALLER_NUMBER(col_constraints,0,xy,xy2,2*numBits)

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

    t_equals = True
    tvars = False
    
    writeWALLACE_SPEC(numBits, True, t_equals, tvars)
    writeWALLACE_SPEC(numBits, False, t_equals, tvars)










    
