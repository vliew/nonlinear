from circuits import *

numBits = 16
lowCol = 0
highCol = 10

tvars = False

# Map from columns to the constraints on those columns.
# We will fill col_constraints with the full set of constraints.
# A constraint is a DIMACS formatted clause.
# Constraints in column -1 will always be included.
col_constraints = {}
for i in range(-1,2*numBits+2):
    col_constraints[i] = []

if not tvars:
    keyFileName = "%darraycomm_%dto%d.key" % (numBits,lowCol,highCol)
    cnfFileName = "%darraycomm_%dto%d.cnf" % (numBits,lowCol,highCol)
    orderFileName = "%darraycomm_%dto%d_t.order" % (numBits,lowCol,highCol)
else:
    keyFileName = "%darraycomm_%dto%d_tvars.key" % (numBits,lowCol,highCol)
    cnfFileName = "%darraycomm_%dto%d_tvars.cnf" % (numBits,lowCol,highCol)
    orderFileName = "%darraycomm_%dto%d_tvars.order" % (numBits,lowCol,highCol)
    
f_key = open(keyFileName,'w')
f_cnf = open(cnfFileName,'w')
f_order = open(orderFileName,'w')

nextDIMACS = 1

if not tvars:
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
if not tvars:
    writeARRAYMULT(col_constraints, x,y,cxy,dxy,txy,oxy,numBits)
    writeARRAYMULT(col_constraints, y,x,cyx,dyx,tyx,oyx,numBits)
else:
    for i in range(numBits):
        for j in range(numBits):
            writeEQUAL(col_constraints, i+j, txy[(i,j)], tyx[(j,i)])
    writeARRAYSUM(col_constraints,cxy,dxy,txy,oxy,numBits)
    writeARRAYSUM(col_constraints,cyx,dyx,tyx,oyx,numBits)
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











    
