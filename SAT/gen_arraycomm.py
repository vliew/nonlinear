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

keyFileName = "%darraycomm.key" % (numBits)
cnfFileName = "%darraycomm.cnf" % (numBits)
f_key = open(keyFileName,'w')
f_cnf = open(cnfFileName,'w')

# Initialize variable maps
nextDIMACS = 1

f_key.write("\n WRITING x,y VARIABLES \n")
x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)

f_key.write("\n WRITING txy, tyx VARIABLES \n")
txy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txy",numBits,numBits)
tyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyx",numBits,numBits)       
cxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxy",numBits,numBits)
cyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyx",numBits,numBits)
dxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxy",numBits,numBits)
dyx, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyx",numBits,numBits)

oxy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'oxy',2*numBits)
oyx, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'oyx',2*numBits)
e, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'e',2*numBits)

writeARRAYMULT(col_constraints, x,y,cxy,dxy,txy,oxy,numBits)
writeARRAYMULT(col_constraints, y,x,cyx,dyx,tyx,oyx,numBits)
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












    
