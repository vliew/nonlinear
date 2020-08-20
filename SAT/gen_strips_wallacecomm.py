from circuits import *

numBits = 14
lowCol = 0
highCol = 24

# Map from columns to the constraints on those columns.
# We will fill col_constraints with the full set of constraints.
# A constraint is a DIMACS formatted clause.
# Constraints in column -1 will always be included.
col_constraints = {}
for i in range(-1,2*numBits+1):
    col_constraints[i] = []

keyFileName = "%dwallacecomm_%dto%d.key" % (numBits,lowCol,highCol)
cnfFileName = "%dwallacecomm_%dto%d.cnf" % (numBits,lowCol,highCol)
f_key = open(keyFileName,'w')
f_cnf = open(cnfFileName,'w')

# Initialize variable maps
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

# Write critical strip assignment to e
for i in range(lowCol,highCol):
    writeFALSE(col_constraints,i,e[i])
writeTRUE(col_constraints,highCol,e[highCol])

numClauses = 0
for clause in col_constraints[-1]:
    numClauses += 1
for col in range(lowCol,highCol+1):
    for clause in col_constraints[col]:
        numClauses += 1
f_cnf.write("p cnf %d %d \n" % (nextDIMACS, numClauses))

# Write all constraints to file
for clause in col_constraints[-1]:
    f_cnf.write(clause)
for col in range(lowCol,highCol+1):
    for clause in col_constraints[col]:
        f_cnf.write(clause)
f_cnf.close()












    
