from circuits import *

numBits = 8

# Map from columns to the constraints on those columns.
# We will fill col_constraints with the full set of constraints.
# A constraint is a DIMACS formatted clause.
# Constraints in column -1 will always be included.
col_constraints = {}
for i in range(-1,2*numBits+3):
    col_constraints[i] = []

keyFileName = "%dwallacedist.key" % (numBits)
cnfFileName = "%dwallacedist.cnf" % (numBits)
f_key = open(keyFileName,'w')
f_cnf = open(cnfFileName,'w')

nextDIMACS = 1

f_key.write("\n WRITING x,y VARIABLES \n")
x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',numBits+1)
writeFALSE(col_constraints,-1,z[numBits])
e, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'e',2*numBits+2)
zeroes, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'zeroes',2*numBits+2)

txz, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"txz",numBits)
tyz, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"tyz",numBits)
txply_z, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,"txply_z",numBits+1)

cadd2, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"cadd2",2*numBits+2)
cadd1, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"cadd1",numBits)

xply, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xply',numBits+1)
xply_z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xply_z',2*numBits+3)

xz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xz',2*numBits+1)
yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yz',2*numBits+1)
xzplyz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xzplyz',2*numBits+2)

cxz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cxz',2*numBits)
cyz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cyz',2*numBits)
cxply_z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'cxply_z',2*numBits+2)

writeWALLACEMULT(col_constraints, x,z,txz,xz,cxz,zeroes,numBits)
writeWALLACEMULT(col_constraints, y,z,tyz,yz,cyz,zeroes,numBits)
writeRIPPLECARRYADDER(col_constraints,x,y,cadd1,xply,numBits)

writeWALLACEMULT(col_constraints, xply,z,txply_z,xply_z,cxply_z,zeroes,numBits+1)
writeRIPPLECARRYADDER(col_constraints,xz,yz,cadd2,xzplyz,2*numBits+1)

writeNOTEQUAL_NUMBERS(col_constraints,e,xply_z,xzplyz,2*numBits+2)

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












    
