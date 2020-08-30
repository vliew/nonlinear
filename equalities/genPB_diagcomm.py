from circuits_pb import *
import sys
import os


# writeDIAGCOMM
#
# writeDIAGCOMM generates a decision problem for verification of multiplier
# commutativity x*y = y*x by specifying either that
#
#    \sum_i 2^i * (x*y)_i >= 1 + \sum_i 2^i * (y*x)_i
#
# (if the argument greater_than is true) or that
#
#    \sum_i 2^i * (x*y)_i <= -1 + \sum_i 2^i * (y*x)_i
#
# (if greater_than is false).

def writeDIAGCOMM(numBits, greater_than=True, only_tvars=False, t_equals=True):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    # Choose filename based on settings
    # (Adding a suffix "_dec" here to indicate decision version -JN)
    keyFileName = "benchmarks/%ddiagcomm_dec" % (numBits)
    opbFileName = "benchmarks/%ddiagcomm_dec" % (numBits)
    if greater_than:
        keyFileName += "_greater"
        opbFileName += "_greater"
    else:
        keyFileName += "_less"
        opbFileName += "_less"
    if t_equals:
        keyFileName += "_teq"
        opbFileName += "_teq"
    if only_tvars:
        keyFileName += "_tvars"
        opbFileName += "_tvars"
    keyFileName += ".key"
    opbFileName += ".opb"

    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')
        
    nextDIMACS = 1

    if not only_tvars:
        x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
        y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
        
    txy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txy",numBits,numBits)
    tyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyx",numBits,numBits)       
    cxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxy",numBits,numBits)
    cyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyx",numBits,numBits)
    dxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxy",numBits,numBits)
    dyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyx",numBits,numBits)

    yx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yx',2*numBits)
    xy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xy',2*numBits)

    if not only_tvars:
        writeDIAGMULT(col_constraints, x,y,cxy,dxy,txy,xy,numBits)
        writeDIAGMULT(col_constraints, y,x,cyx,dyx,tyx,yx,numBits)
    else:
        writeDIAGSUM(col_constraints,cxy,dxy,txy,xy,numBits)
        writeDIAGSUM(col_constraints,cyx,dyx,tyx,yx,numBits)

    # Write t-equalities
    if t_equals:
        for i in range(numBits):
            for j in range(numBits):
                writeEQUAL(col_constraints, i+j, txy[(i,j)], tyx[(j,i)])

    if greater_than:
        writeBIGGER_NUMBER(col_constraints,0,xy,yx,2*numBits)
    else:
        writeSMALLER_NUMBER(col_constraints,0,xy,yx,2*numBits)

    # Write file header (with some added nice-to-have information)
    writeHEADER(f_opb, nextDIMACS, col_constraints)
    f_opb.write("* \n")
    f_opb.write("* Multiplier commutativity verification problem \n")
    if greater_than:
        f_opb.write("* %d-bit numbers; decision problem; greater-than version \n"
                    % numBits)
    else:
        f_opb.write("* %d-bit numbers; decision problem; less-than version \n"
                    % numBits)
    f_opb.write("* \n")
    
    # Write all constraints to file
    for col in range(-1,2*numBits+2):
        for constraint in col_constraints[col]:
            f_opb.write(constraint)
    f_opb.close()


# writeDIAGCOMMOPT
#
# writeDIAGCOMMOPT generates an optimization problem for verification of
# multiplier commutativity x*y = y*x by asking to minimize
#
#    \sum_i 2^i * (y*x)_i - \sum_i 2^i * (x*y)_i 
#
# (if the argument greater_than is true) or to minimize
#
#    \sum_i 2^i * (x*y)_i - \sum_i 2^i * (y*x)_i 
#
# (if greater_than is false). The fact that multiplication is commutative means
# that the optimal value is 0 for both problems.

def writeDIAGCOMMOPT(numBits, greater_than=True, only_tvars=False, t_equals=True):
    # Map from columns to the constraints on those columns.
    # We will fill col_constraints with the full set of constraints.
    # Constraints in column -1 will always be included.
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []

    # Choose filename based on settings
    # (Adding a suffix "_dec" here to indicate decision version -JN)
    keyFileName = "benchmarks/%ddiagcomm_opt" % (numBits)
    opbFileName = "benchmarks/%ddiagcomm_opt" % (numBits)
    if greater_than:
        keyFileName += "_greater"
        opbFileName += "_greater"
    else:
        keyFileName += "_less"
        opbFileName += "_less"
    if t_equals:
        keyFileName += "_teq"
        opbFileName += "_teq"
    if only_tvars:
        keyFileName += "_tvars"
        opbFileName += "_tvars"
    keyFileName += ".key"
    opbFileName += ".opb"

    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')
        
    nextDIMACS = 1

    if not only_tvars:
        x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
        y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
        
    txy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txy",numBits,numBits)
    tyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyx",numBits,numBits)       
    cxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxy",numBits,numBits)
    cyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyx",numBits,numBits)
    dxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxy",numBits,numBits)
    dyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyx",numBits,numBits)

    yx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yx',2*numBits)
    xy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xy',2*numBits)

    if not only_tvars:
        writeDIAGMULT(col_constraints, x,y,cxy,dxy,txy,xy,numBits)
        writeDIAGMULT(col_constraints, y,x,cyx,dyx,tyx,yx,numBits)
    else:
        writeDIAGSUM(col_constraints,cxy,dxy,txy,xy,numBits)
        writeDIAGSUM(col_constraints,cyx,dyx,tyx,yx,numBits)

    # Write t-equalities
    if t_equals:
        for i in range(numBits):
            for j in range(numBits):
                writeEQUAL(col_constraints, i+j, txy[(i,j)], tyx[(j,i)])

    # Write file header (with some added nice-to-have information)
    writeHEADER(f_opb, nextDIMACS, col_constraints)
    f_opb.write("* \n")
    f_opb.write("* Multiplier commutativity verification problem \n")
    if greater_than:
        f_opb.write("* %d-bit numbers; optimization problem; greater-than version \n"
                    % numBits)
    else:
        f_opb.write("* %d-bit numbers; optimization problem; less-than version \n"
                    % numBits)
    f_opb.write("* \n")
    
    # Specify objective function
    if greater_than:
        writeBIGGER_NUMBER_OPT (f_opb, xy, yx, 2*numBits)
    else:
        writeSMALLER_NUMBER_OPT(f_opb, xy, yx, 2*numBits)

    # Write all constraints to file
    for col in range(-1,2*numBits+2):
        for constraint in col_constraints[col]:
            f_opb.write(constraint)
    f_opb.close()

    
#
# "Main" function in script
#

if __name__ == '__main__':
    if not os.path.exists("benchmarks"):
        os.makedirs("benchmarks")
    # Set only_tvars to True to remove xy-variables.
    only_tvars = False
    # Set t_equals to False to turn off preprocessing t-equalities.
    t_equals = True

    numBits = int(sys.argv[1])
    
    writeDIAGCOMM(numBits, True, only_tvars, t_equals)
    writeDIAGCOMM(numBits, False, only_tvars, t_equals)
    writeDIAGCOMMOPT(numBits, True, only_tvars, t_equals)
    writeDIAGCOMMOPT(numBits, False, only_tvars, t_equals)

