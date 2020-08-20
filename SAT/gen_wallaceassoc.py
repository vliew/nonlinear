from circuits import *

numBits = 7

# Map from columns to the constraints on those columns.
# We will fill col_constraints with the full set of constraints.
# A constraint is a DIMACS formatted clause.
# Constraints in column -1 will always be included.
col_constraints = {}
for i in range(-1,4*numBits+1):
    col_constraints[i] = []

keyFileName = "%dwallaceassoc.key" % (numBits)
cnfFileName = "%dwallaceassoc.cnf" % (numBits)
f_key = open(keyFileName,'w')
f_cnf = open(cnfFileName,'w')

# Initialize variable maps
nextDIMACS = 1

# We will pad a leading n zeroes for x and z
f_key.write("\n WRITING x,y,z VARIABLES \n")
x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',2*numBits)
y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',2*numBits)
zeroes, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'zeroes',4*numBits+1)
# Set padded digits of x and z to zero
for i in range(numBits):
    writeFALSE(col_constraints, -1, x[numBits+i])
    writeFALSE(col_constraints, -1, z[numBits+i])

f_key.write("\n WRITING xy VARIABLES \n")
txy, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"txy",numBits)
xy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xy',2*numBits+1)
cxy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cxy',2*numBits)

f_key.write("\n WRITING yz VARIABLES \n")
tyz, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"tyz",numBits)
yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yz',2*numBits+1)
cyz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cyz',2*numBits)

f_key.write("\n WRITING xy_z VARIABLES \n")
txy_z, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"txy_z",2*numBits)
xy_z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"xy_z",4*numBits+1)
cxy_z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"cxy_z",4*numBits)

f_key.write("\n WRITING x_yz VARIABLES \n")
tx_yz, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"tx_yz",2*numBits)
x_yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"x_yz",4*numBits+1)
cx_yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"cx_yz",4*numBits)

e, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'e',3*numBits)

writeWALLACEMULT(col_constraints, x,y,txy,xy,cxy,zeroes,numBits)
writeWALLACEMULT(col_constraints, y,z,tyz,yz,cyz,zeroes,numBits)

writeWALLACEMULT(col_constraints, xy,z,txy_z,xy_z,cxy_z,zeroes,2*numBits)
writeWALLACEMULT(col_constraints, x,yz,tx_yz,x_yz,cx_yz,zeroes,2*numBits)

writeNOTEQUAL_NUMBERS(col_constraints,e,xy_z,x_yz,3*numBits)

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












    
