from circuits import *

numBits = 8
lowCol = 0
highCol = 15

# Map from columns to the constraints on those columns.
# We will fill col_constraints with the full set of constraints.
# A constraint is a DIMACS formatted clause.
# Constraints in column -1 will always be included.
col_constraints = {}
for i in range(-1,2*numBits+2):
    col_constraints[i] = []

keyFileName = "%darraydistrib_%dto%d.key" % (numBits,lowCol,highCol)
cnfFileName = "%darraydistrib_%dto%d.cnf" % (numBits,lowCol,highCol)
f_key = open(keyFileName,'w')
f_cnf = f = open(cnfFileName,'w')

nextDIMACS = 1
x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)
z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'z',numBits+1)

xply, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xply',numBits+1)
xply_z, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xply_z',2*numBits+2)

xz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xz',2*numBits)
yz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'yz',2*numBits)
xzplyz, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'xzplyz',2*numBits+1)

e, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'e',2*numBits+1)
cadd2, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"cadd2",2*numBits)

cadd1, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,"cadd1",numBits)

txz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txz",numBits,numBits)
cxz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxz",numBits,numBits)
dxz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxz",numBits,numBits)    

tyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"tyz",numBits,numBits)
cyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cyz",numBits,numBits)
dyz, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dyz",numBits,numBits)

txply_z, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"txply_z",numBits+1,numBits+1)
cxply_z, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"cxply_z",numBits+1,numBits+1)
dxply_z, nextDIMACS = createGRID_VARIABLES(nextDIMACS,f_key,"dxply_z",numBits+1,numBits+1)

writeRIPPLECARRYADDER(col_constraints,x,y,cadd1,xply,numBits)
writeRIPPLECARRYADDER(col_constraints,xz,yz,cadd2,xzplyz,2*numBits)

writeARRAYMULT(col_constraints, x,z,cxz,dxz,txz,xz,numBits)
writeARRAYMULT(col_constraints, y,z,cyz,dyz,tyz,yz,numBits)
writeFALSE(col_constraints,-1,z[numBits])
writeARRAYMULT(col_constraints, xply,z,cxply_z,dxply_z,txply_z,xply_z,numBits+1)

writeNOTEQUAL_NUMBERS(col_constraints,e,xply_z,xzplyz,2*numBits+1)

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
