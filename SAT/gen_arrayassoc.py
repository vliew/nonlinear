from circuits import *
# Knobs to set
numBits = 8
truncate = False

# Map from columns to the constraints on those columns.
# We will fill col_constraints with the full set of constraints.
# A constraint is a DIMACS formatted clause.
# Constraints in column -1 will always be included.
col_constraints = {}
for i in range(-1,4*numBits+2):
    col_constraints[i] = []

# Choose filename based on settings
keyFileName = "%darrayassoc" % (numBits)
cnfFileName = "%darrayassoc" % (numBits)
keyFileName += ".key"
cnfFileName += ".cnf"

f_key = open(keyFileName,'w')
f_cnf = open(cnfFileName,'w')

# Initialize variable maps
nextDIMACS = 1

# Create the variables
# We will pad a leading n zeroes for x and z
f_key.write("\n WRITING x,y,z VARIABLES \n")
x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',2*numBits)
y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',2*numBits)

f_key.write("\n WRITING xy VARIABLES \n")
txy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txy",numBits,numBits)
cxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxy",numBits,numBits)
dxy, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxy",numBits,numBits)
oxy, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'oxy',2*numBits)

f_key.write("\n WRITING yz VARIABLES \n")
tyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyz",numBits,numBits)
cyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyz",numBits,numBits)
dyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyz",numBits,numBits)
oyz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'oyz',2*numBits)

f_key.write("\n WRITING xy_z VARIABLES \n")
txy_z, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txy_z",2*numBits,2*numBits)
cxy_z, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxy_z",2*numBits,2*numBits)
dxy_z, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxy_z",2*numBits,2*numBits)
oxy_z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"oxy_z",4*numBits)

f_key.write("\n WRITING x_yz VARIABLES \n")
tx_yz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tx_yz",2*numBits,2*numBits)
cx_yz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cx_yz",2*numBits,2*numBits)
dx_yz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dx_yz",2*numBits,2*numBits)
ox_yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"ox_yz",4*numBits)

e, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'e',3*numBits)

# Set padded digits of x and z to zero
for i in range(numBits):
    writeFALSE(col_constraints, -1, x[numBits+i])
    writeFALSE(col_constraints, -1, z[numBits+i])

writeARRAYMULT(col_constraints, x,y,cxy,dxy,txy,oxy,numBits)
writeARRAYMULT(col_constraints, y,z,cyz,dyz,tyz,oyz,numBits)
writeARRAYMULT(col_constraints, oxy,z,cxy_z,dxy_z,txy_z,oxy_z,2*numBits)
writeARRAYMULT(col_constraints, x,oyz,cx_yz,dx_yz,tx_yz,ox_yz,2*numBits)

writeNOTEQUAL_NUMBERS(col_constraints,e,oxy_z,ox_yz,3*numBits)

# Write all constraints to file
numClauses = 0
for col in col_constraints:
    for clause in col_constraints[col]:
        numClauses += 1
f_cnf.write("p cnf %d %d \n" % (nextDIMACS, numClauses))

for col in col_constraints:
    for clause in col_constraints[col]:
        f_cnf.write(clause)
f_cnf.close()












    
