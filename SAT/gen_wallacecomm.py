from circuits import *

numBits = 12
lowCol = 0
highCol = 2*numBits+1

# Map from columns to the constraints on those columns.
# We will fill col_constraints with the full set of constraints.
# A constraint is a DIMACS formatted clause.
# Constraints in column -1 will always be included.
col_constraints = {}
for i in range(-1,2*numBits+1):
    col_constraints[i] = []

keyFileName = "%dwallacecomm.key" % (numBits)
cnfFileName = "%dwallacecomm.cnf" % (numBits)
f_key = open(keyFileName,'w')
f_cnf = open(cnfFileName,'w')

nextDIMACS = 1

f_key.write("\n WRITING x,y VARIABLES \n")
x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
zeroes, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'zeroes',2*numBits)

f_key.write("\n WRITING txy, tyx VARIABLES \n")
txy, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"txy",numBits)
tyx, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"tyx",numBits)       

oxy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'oxy',2*numBits+1)
oyx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'oyx',2*numBits+1)
e, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'e',2*numBits)

cxy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cxy',2*numBits)
cyx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cyx',2*numBits)

writeWALLACEMULT(col_constraints, x,y,txy,oxy,cxy,zeroes,numBits)
writeWALLACEMULT(col_constraints, y,x,tyx,oyx,cyx,zeroes,numBits)
writeNOTEQUAL_NUMBERS(col_constraints,e,oxy,oyx,2*numBits)

numClauses = 0
for col in col_constraints:
    for clause in col_constraints[col]:
        numClauses += 1
f_cnf.write("p cnf %d %d \n" % (nextDIMACS, numClauses))

# Write all constraints to file
for col in col_constraints:
    for clause in col_constraints[col]:
        f_cnf.write(clause)
f_cnf.close()












    
