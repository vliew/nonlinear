from circuits import *
from utils import *

numBits = 11

# Map from columns to the constraints on those columns.
# We will fill col_constraints with the full set of constraints.
# A constraint is a DIMACS formatted clause.
# Constraints in column -1 will always be included.
col_constraints = {}
for i in range(-1,2*numBits+2):
    col_constraints[i] = []

keyFileName = "%dwallace_array.key" % (numBits)
cnfFileName = "%dwallace_array.cnf" % (numBits)
f_key = open(keyFileName,'w')
f_cnf = f = open(cnfFileName,'w')

# Initialize variable maps
nextDIMACS = 1
t, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,'t',numBits)
x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
o, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'o',2*numBits+1)
zeroes, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'zeroes',2*numBits)
c, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'c',2*numBits)
writeWALLACEMULT(col_constraints, x,y,t,o,c,zeroes,numBits)

c1, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"c1",numBits,numBits)
d1, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"d1",numBits,numBits)
t1, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"t1",numBits,numBits)
o1, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'o1',2*numBits)
writeARRAYMULT(col_constraints, x,y,c1,d1,t1,o1,numBits)

e, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'e',2*numBits)
# Don't need to compare o_{2n}.
writeNOTEQUAL_NUMBERS(col_constraints,e,o,o1,2*numBits)

numClauses = 0
for col in col_constraints:
    for clause in col_constraints[col]:
        numClauses += 1
f_cnf.write("p cnf %d %d \n" % (nextDIMACS, numClauses))

# Write all constraints to file
for col in range(-1,2*numBits+2):
    for clause in col_constraints[col]:
        f_cnf.write(clause)
f_cnf.close()
