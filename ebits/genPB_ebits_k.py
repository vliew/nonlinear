from circuits_pb import *
import sys
import os

def writeEBITS(numBits,k):
    col_constraints = {}
    for i in range(-1,2*numBits+2):
        col_constraints[i] = []
        
    keyFileName = "benchmarks/%debits_%d.key" % (numBits,k)
    opbFileName = "benchmarks/%debits_%d.opb" % (numBits,k)

    f_key = open(keyFileName,'w')
    f_opb = open(opbFileName,'w')

    nextDIMACS = 1
    x, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'x',numBits)
    y, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'y',numBits)

    # Assert that Weight(x) - Weight(y) = 0.
    clause = ""
    for i in range(numBits):
        weight = 2**i
        clause += "+%d x%d -%d x%d " % (weight, x[i], weight, y[i])
    clause += "= 0 ;\n"
    col_constraints[-1].append(clause)

    ## Assert that some output bit is not equal
    #e, nextDIMACS = createBITVECTOR(nextDIMACS,f_key,'e',numBits)
    #writeNOTEQUAL_NUMBERS(col_constraints,e,x,y,numBits)

    ## Assert that k-th output bit is not equal
    clause = "-1 x%d -1 x%d >= -1; \n" % (x[k], y[k])
    col_constraints[-1].append(clause)
    clause = "+1 x%d +1 x%d >= 1; \n" % ( x[k], y[k])
    col_constraints[-1].append(clause)

    # Write all constraints to file
    writeHEADER(f_opb, nextDIMACS, col_constraints)
    for col in col_constraints:
        for clause in col_constraints[col]:
            f_opb.write(clause)
    f_opb.close()

if __name__ == '__main__':
    if not os.path.exists("benchmarks"):
        os.makedirs("benchmarks")
        
    numBits = int(sys.argv[1])
    k = int(sys.argv[2])
    writeEBITS(numBits,k)
