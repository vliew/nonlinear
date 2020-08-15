from circuits_pb import *
import sys
import os


def writeWALLACECOMM(numBits, greater_than=True, t_equals=True):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # A constraint is a DIMACS formatted clause.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+4):
        col_constraints[i] = []

    # Choose filename based on settings
    keyFileName = "benchmarks/%dwallacecomm" % (numBits)
    opbFileName = "benchmarks/%dwallacecomm" % (numBits)
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


    # Initialize variable maps
    nextDIMACS = 1

    # Create the variables
    yx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yx',2*numBits+1)
    xy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xy',2*numBits+1)
    
    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)

    txy, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"txy",numBits)
    tyx, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"tyx",numBits)
    zeroes, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'zeroes',2*numBits+3)
    cxy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cxy',2*numBits)
    cyx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cyx',2*numBits)


    writeWALLACEMULT(col_constraints, x,y,txy,xy,cxy,zeroes,numBits)
    writeWALLACEMULT(col_constraints, y,x,tyx,yx,cyx,zeroes,numBits)
    
    # Write t-equalities
    if t_equals:
        for i in range(numBits):
            for j in range(numBits):
                if i+j < numBits:
                    writeEQUAL(col_constraints, -1, txy[(0,i+j,j)], tyx[(0,i+j,i)])
                else:
                    writeEQUAL(col_constraints, -1, txy[(0,i+j,(numBits-1)-j)], tyx[(0,i+j,(numBits-1)-i)])


    if greater_than:
        # inequality xy > yx
        writeBIGGER_NUMBER(col_constraints,0,xy,yx,2*numBits)
    else:
        # inequality xy < yx
        writeSMALLER_NUMBER(col_constraints,0,xy,yx,2*numBits)

    # Write all constraints to file
    writeHEADER(f_opb, nextDIMACS, col_constraints)
    for col in col_constraints:
        for clause in col_constraints[col]:
            f_opb.write(clause)
    f_opb.close()

if __name__ == '__main__':
    if not os.path.exists("benchmarks"):
        os.makedirs("benchmarks")
    # Set t_equals to False to turn off preprocessing t-equalities.
    t_equals = True
    numBits = int(sys.argv[1])
    
    writeWALLACECOMM(numBits, True, t_equals)
    writeWALLACECOMM(numBits, False, t_equals)










    
