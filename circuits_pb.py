import os
# Module providing encodings for some useful circuits. This version
# provides pseudo-Boolean encodings. 
# 
# Each write function takes some circuit variables as input, but does
# *not* create variables. Use the create functions to introduce some
# useful variable mappings.
#

# If writing all columns, just pass in col_constraints.
# For strip instances, use optional input num_constraints.
def writeHEADER(f_opb, nextDIMACS, col_constraints, num_constraints=0):
    if num_constraints == 0:  
        for col in col_constraints:
            num_constraints += len(col_constraints[col])
    f_opb.write("* #variable= %d #constraint= %d \n" % (nextDIMACS-1, num_constraints))

# Input: string representing inequality
# Output: string with negated inequality
def Negate(inequality):
    inequality_split = inequality.split(" ")
    neg_inequality = ""
    seen_geq = False
    for i in range(len(inequality_split)):
        if inequality_split[i][0] == '-':
            if not seen_geq:
                neg_inequality += '+' + inequality_split[i][1:] + ' '
            else:
                neg_inequality += '+' + str((int(inequality_split[i][1:])+1)) + ' '
                
        elif inequality_split[i][0] == '+':
            if not seen_geq:
                neg_inequality += '-' + inequality_split[i][1:] + ' '
            else:
                # No negative sign if RHS becomes 0.
                neg = ''
                if int(inequality_split[i][1:])-1 != 0:
                    neg = '-'                    
                neg_inequality += neg + str((int(inequality_split[i][1:])-1)) + ' '
        elif inequality_split[i][0] == '0' and seen_geq:
            neg_inequality += "1 " 
        elif inequality_split[i][0] == '>':
            seen_geq = True
            neg_inequality += inequality_split[i] + ' '
        else:
            neg_inequality += inequality_split[i] + ' '
    return neg_inequality

def createBITVECTOR(inDIMACS,f_key,label,numBits):
    v = {}
    nextDIMACS = inDIMACS
    for i in range(numBits):
        v[i] = nextDIMACS
        f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d \n" % i)
        nextDIMACS += 1
    return v, nextDIMACS

def createGRID_VARIABLES(inDIMACS,f_key,label,length,width):
    v = {}
    nextDIMACS = inDIMACS
    for i in range(width):
        for j in range(length):
            v[(i,j)] = nextDIMACS
            f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d_%d \n" % (i,j))
            nextDIMACS += 1
    return v, nextDIMACS

def writeFALSE(col_constraints,col,a):
    col_constraints[col].append("+1 x%d = 0 ;\n" % a)

def writeTRUE(col_constraints,col,a):
    col_constraints[col].append("+1 x%d = 1 ;\n" % a)

def writeEQUAL(col_constraints,col,a,b):
    col_constraints[col].append("+1 x%d -1 x%d = 0 ;\n" %(a,b))

def writeNOTEQUAL(col_constraints,col,a,b):
    # Rule out (1,1)
    col_constraints[col].append("-1 x%d -1 x%d >= -1 ;\n" %(a,b))
    # Rule out (0,0)
    col_constraints[col].append("+1 x%d +1 x%d >= 1 ;\n" %(a,b))

# Given two bits a,b, write e = (a!=b)
def writeSTORE_NOTEQUAL(col_constraints,col,e,a,b):
    col_constraints[col].append("-1 x%d -1 x%d -1 x%d >= -2 ;\n" %(e,a,b))
    col_constraints[col].append("-1 x%d +1 x%d +1 x%d >= 0 ;\n" %(e,a,b))
    col_constraints[col].append("+1 x%d -1 x%d +1 x%d >= 0 ;\n" %(e,a,b))
    col_constraints[col].append("+1 x%d +1 x%d -1 x%d >= 0 ;\n" %(e,a,b))

# Given two bitvectors, assert that they are not equal in their
# first n entries
# e holds intermediate comparison bits.
def writeNOTEQUAL_NUMBERS(col_constraints,e,a,b,numBits):
    clause = ""
    for i in range(numBits):
        writeSTORE_NOTEQUAL(col_constraints,i,e[i],a[i],b[i])
        clause += "+1 x%d" % e[i] + " "
    clause += ">= 1 ;\n"
    col_constraints[-1].append(clause)

# Write Weight(x) - Weight(y) >= 1
def writeBIGGER_NUMBER(col_constraints,col,x,y,numBits):
    clause = ""
    for i in range(numBits):
        clause += "+%d x%d -%d x%d " % (2**i, x[i], 2**i, y[i])
    clause += ">= 1 ;\n"
    col_constraints[col].append(clause)

# Write Weight(y) - Weight(x) >= 1
def writeSMALLER_NUMBER(col_constraints,col,x,y,numBits):
    clause = ""
    for i in range(numBits):
        clause += "+%d x%d -%d x%d " % (2**i, y[i], 2**i, x[i])
    clause += ">= 1 ;\n"
    col_constraints[col].append(clause)    

# writeSMALLER_NUMBER_OPT produces an objective function asking to
# minimize Weight(x) - Weight(y)
def writeSMALLER_NUMBER_OPT(f_opb, x, y, numBits):
    f_opb.write("* Objective: minimize <1st product> - <2nd product> \n");
    f_opb.write("* (finding optimum 0 shows that <1st product> >= <2nd product>) \n");
    objective = "min: "
    for i in range(numBits):
        objective += "+%d x%d -%d x%d " % (2**i, x[i], 2**i, y[i])
    objective += " ;\n"
    f_opb.write(objective)
                
# writeBIGGER_NUMBER_OPT produces an objective function asking to
# minimize Weight(y) - Weight(x)
def writeBIGGER_NUMBER_OPT(f_opb, x, y, numBits):
    f_opb.write("* Objective: minimize <2nd product> - <1st product> \n");
    f_opb.write("* (finding optimum 0 shows that <1st product> <= <2nd product>) \n");
    objective = "min: "
    for i in range(numBits):
        objective += "+%d x%d -%d x%d " % (2**i, y[i], 2**i, x[i])
    objective += " ;\n"
    f_opb.write(objective)
                
# Write c = MAJ(a_0,a_1,a_2) to f_cnf
def writeMAJ(col_constraints, col, c, a_0, a_1, a_2):
    col_constraints[col].append("+1 x%d -1 x%d -1 x%d >= -1 ;\n" %(c,a_0,a_1))
    col_constraints[col].append("+1 x%d -1 x%d -1 x%d >= -1 ;\n" %(c,a_0,a_2))
    col_constraints[col].append("+1 x%d -1 x%d -1 x%d >= -1 ;\n" %(c,a_1,a_2))
    col_constraints[col].append("-1 x%d +1 x%d +1 x%d >= 0 ;\n" %(c,a_0,a_1))
    col_constraints[col].append("-1 x%d +1 x%d +1 x%d >= 0 ;\n" %(c,a_0,a_2))
    col_constraints[col].append("-1 x%d +1 x%d +1 x%d >= 0 ;\n" %(c,a_1,a_2))

# Write c = AND(a_0,a_1) to f_cnf
def writeAND(col_constraints, col, c, a_0, a_1):
    col_constraints[col].append("-1 x%d +1 x%d >= 0 ;\n" % (c,a_0))
    col_constraints[col].append("-1 x%d +1 x%d >= 0 ;\n" % (c,a_1))
    col_constraints[col].append("+1 x%d -1 x%d -1 x%d >= -1 ;\n" % (c,a_0,a_1))

# Write c = OR(a_0,a_1) to f_cnf
def writeOR(col_constraints, col, c, a_0, a_1):
    col_constraints[col].append("+1 x%d -1 x%d >= 0 ;\n" % (c,a_0))
    col_constraints[col].append("+1 x%d -1 x%d >= 0 ;\n" % (c,a_1))
    col_constraints[col].append("-1 x%d +1 x%d +1 x%d >= 0 ;\n" % (c,a_0,a_1))

# Write d = XOR(a_0,a_1,a_2) to f_cnf	
def writeXOR3(col_constraints, col,d,a_0,a_1,a_2):
    col_constraints[col].append("-1 x%d +1 x%d +1 x%d +1 x%d >= 0 ;\n" %(d,a_0,a_1,a_2))
    col_constraints[col].append("+1 x%d -1 x%d +1 x%d +1 x%d >= 0 ;\n" %(d,a_0,a_1,a_2))
    col_constraints[col].append("+1 x%d +1 x%d -1 x%d +1 x%d >= 0 ;\n" %(d,a_0,a_1,a_2))
    col_constraints[col].append("+1 x%d +1 x%d +1 x%d -1 x%d >= 0 ;\n" %(d,a_0,a_1,a_2))
    col_constraints[col].append("+1 x%d -1 x%d -1 x%d -1 x%d >= -2 ;\n" %(d,a_0,a_1,a_2))
    col_constraints[col].append("-1 x%d +1 x%d -1 x%d -1 x%d >= -2 ;\n" %(d,a_0,a_1,a_2))
    col_constraints[col].append("-1 x%d -1 x%d +1 x%d -1 x%d >= -2 ;\n" %(d,a_0,a_1,a_2))
    col_constraints[col].append("-1 x%d -1 x%d -1 x%d +1 x%d >= -2 ;\n" %(d,a_0,a_1,a_2))

# Write d = XOR(a_0,a_1,a_2) to f_cnf	
def writeXOR2(col_constraints, col,d,a_0,a_1):
    col_constraints[col].append("-1 x%d +1 x%d +1 x%d >= 0 ;\n" %(d,a_0,a_1))
    col_constraints[col].append("-1 x%d -1 x%d -1 x%d >= -2 ;\n" %(d,a_0,a_1))
    col_constraints[col].append("+1 x%d -1 x%d +1 x%d >= 0 ;\n" %(d,a_0,a_1))
    col_constraints[col].append("+1 x%d +1 x%d -1 x%d >= 0 ;\n" %(d,a_0,a_1))

# clause_adder toggles between the clausal representation and the arithmetic representation.
def writeFULLADDER(col_constraints, col, c_in, d_in, t, c_out, d_out, clauses=False):
    if clauses:
        writeXOR3(col_constraints,col,d_out,c_in,d_in,t)
        writeMAJ(col_constraints,col,c_out,c_in,d_in,t)
    else:
        # Arithmetic version: 2*c_out + d_out - c_in - d_in - t = 0
        col_constraints[col].append("+2 x%d +1 x%d -1 x%d -1 x%d -1 x%d = 0 ;\n" %(c_out,d_out,t,c_in,d_in))

def writeHALFADDER(col_constraints, col, d_in, t, c_out, d_out, clauses=False):
    if clauses:
        writeXOR2(col_constraints,col,d_out,d_in,t)
        writeAND(col_constraints,col,c_out,d_in,t)
    else:
        # Arithmetic version: 2*c_out + d_out - d_in - t = 0
        col_constraints[col].append("+2 x%d +1 x%d -1 x%d -1 x%d = 0 ;\n" %(c_out,d_out,t,d_in))

# Requires:
# len(x) = len(y) = len(c) = numBits
# len(o) = numBits+1
def writeRIPPLECARRYADDER(col_constraints,x,y,c,o,numBits):
    # Write to column -1 since the critical strip includes the full ripple-carry-adder.
    writeHALFADDER(col_constraints, -1, y[0], x[0], c[0], o[0])
    for col in range(1,numBits):
        writeFULLADDER(col_constraints, -1, c[col-1], y[col], x[col], c[col], o[col])
    writeEQUAL(col_constraints, -1,c[numBits-1],o[numBits])

# Requires:
# len(x) = len(y) = len(c) = numBits
# len(o) = numBits+1
def writeALGEBRA_RIPPLECARRYADDER(col_constraints,x,y,o,numBits):
    # Write to column -1 since the critical strip includes the full ripple-carry-adder.
    clause = ""
    for i in range(numBits):
        clause += "+%d x%d +%d x%d " % (2**i,x[i],2**i,y[i])
    for i in range(numBits+1):
        clause += "-%d x%d " % (2**i,o[i])
    clause += "= 0; \n"
    col_constraints[-1].append(clause)

# x,y are n-bit input bitvectors.
# low_col specifies where to place the beginning of the CLA.
# c[i] holds the carry bit sent to column i. May need to add constraint c[0] = False.
# g, p are the "generate" and "propagate" bits. They can be n-bit input bitvectors.
# terms is a length 16 bitvector that holds some of the terms used to compute carries.
# P,G are each an int (DIMACS variable) representing the "group propagate" and "group generate".
def write4BIT_CLA(col_constraints, low_col, x,y,c,g,p,o,P,G,term):
    writeFALSE(col_constraints, low_col, c[0])
    for col in range(low_col, low_col+4):
        # Compute each g_i, p_i
        writeAND(col_constraints,col,g[col],x[col],y[col])
        writeXOR2(col_constraints,col,p[col],x[col],y[col])
    # Compute terms used to find carries
    # term[0] = p[0] c[0]
    writeAND(col_constraints,low_col,term[0],p[low_col],c[low_col])
    # term[1] = g[0] p[1]
    writeAND(col_constraints,low_col+1,term[1],g[low_col],p[low_col+1])
    # term[2] = term[0] p[1] = c[0] p[0] p[1]
    writeAND(col_constraints,low_col+1,term[2],term[0],p[low_col+1])
    # term[3] = g[1] p[2]
    writeAND(col_constraints,low_col+2,term[3],g[low_col+1],p[low_col+2])
    # term[4] = term[1] p[2] = g[0] p[1] p[2]
    writeAND(col_constraints,low_col+2,term[4],term[1],p[low_col+2])
    # term[5] = term[2] p[2] = c[0] p[0] p[1] p[2]
    writeAND(col_constraints,low_col+2,term[5],term[2],p[low_col+2])
    # term[6] = g[2] p[3]
    writeAND(col_constraints,low_col+3,term[6],g[low_col+2],p[low_col+3])
    # term[7] = term[3] p[3] = g[1]p[2]p[3]
    writeAND(col_constraints,low_col+3,term[7],term[3],p[low_col+3])
    # term[8] = term[4] p[3] = g[0] p[1] p[2] p[3]
    writeAND(col_constraints,low_col+3,term[8],term[4],p[low_col+3])
    # term[9] = term[5] p[3] = c[0] p[0] p[1] p[2] p[3]
    writeAND(col_constraints,low_col+3,term[9],term[5],p[low_col+3])

    # Compute partial sums of terms so that we only need XOR2 and XOR3.
    # term[10] = g[2] + term[3]
    # term[11] = term[4] + term[5]
    writeXOR2(col_constraints, low_col+2,term[10],g[2],term[3])
    writeXOR2(col_constraints, low_col+2,term[11],term[4],term[5])
    # term[12] = g[3] + term[6] + term[7]
    # term[13] = term[8] + term[9]
    writeXOR3(col_constraints, low_col+3,term[12],g[3],term[6],term[7])
    writeXOR2(col_constraints, low_col+3,term[13],term[8],term[9])
    
    # Compute each carry c_i
    # c[1] = g[0] + term[0]
    writeXOR2(col_constraints, low_col,c[low_col+1],g[0],term[0])
    # c[2] = g[1] + term[1] + term[2]
    writeXOR3(col_constraints, low_col+1,c[low_col+2],g[1],term[1],term[2])
    # c[3] = term[10]+term[11]
    writeXOR2(col_constraints, low_col+2,c[low_col+3],term[10],term[11])
    # c[4] = term[12] + term[13]
    writeXOR2(col_constraints, low_col+3,c[low_col+4],term[12],term[13])

    # Compute outputs.
    # o[i] = c[i] + x[i] + y[i] = c[i] + p[i]
    for i in range(low_col,low_col+4):
        writeXOR2(col_constraints, i,o[i],c[i],p[i])
    
    writeEQUAL(col_constraints, low_col+5, o[4], c[4])
    
    # Compute intermediate terms for P
    # term[14] = p[0] p[1]
    # term[15] = p[2] p[3]
    writeAND(col_constraints,low_col+3,term[14],p[low_col],p[low_col+1])
    writeAND(col_constraints,low_col+3,term[15],p[low_col+2],p[low_col+3])
    
    # Compute the group propagate and group generate
    # P = term[14] term[15]
    writeAND(col_constraints,low_col+3,P,term[14],term[15])
    # G = term[12] + term[8]
    writeXOR2(col_constraints,low_col+3,G,term[12],term[8])

# Second part of Array multiplier summing the t-variables.
def writeARRAYSUM(col_constraints,c,d,t,o,numBits):
    for row in range(numBits):
        for i in range(numBits):
            col = i+row
            # Zero-th row of adders: d_i_0 = t_i_0
            if row == 0 and col < numBits:
                writeEQUAL(col_constraints, col,d[(i,0)],t[(i,0)])
                
            # First row of adders
            elif row == 1:
                # Row endpoints
                if i == 0:
                    writeHALFADDER(col_constraints, col,d[(i+1,row-1)],t[(i,row)], c[(i,row)], d[(i,row)])
                elif i == numBits-1:
                    writeHALFADDER(col_constraints, col,c[(i-1,row)],t[(i,row)], c[(i,row)], d[(i,row)])
                # Middle of row
                else:
                    writeFULLADDER(col_constraints, col, c[(i-1,row)], d[(i+1,row-1)], t[(i,row)], c[(i,row)], d[(i,row)])
                    
            # Remaining rows of adders
            else:
                if i == 0:
                    writeHALFADDER(col_constraints, col,d[(i+1,row-1)],t[(i,row)], c[(i,row)], d[(i,row)])
                elif i == numBits-1:
                    writeFULLADDER(col_constraints, col, c[(i-1,row)], c[(i,row-1)], t[(i,row)], c[(i,row)], d[(i,row)])
                else:
                    writeFULLADDER(col_constraints, col, c[(i-1,row)], d[(i+1,row-1)], t[(i,row)], c[(i,row)], d[(i,row)])

    # Write to output variables.
    for col in range(numBits):
        writeEQUAL(col_constraints, col, d[(0,col)], o[col])
    for col in range(numBits,2*numBits-1):
        i = col - numBits + 1 
        writeEQUAL(col_constraints, col, d[(i,numBits-1)], o[col])
    # Last output is the leftmost adder's carry bit.
    col = 2*numBits-1
    writeEQUAL(col_constraints, col, c[(numBits-1,numBits-1)], o[col])

# x,y are inputs to the array multiplier. t stores the tableau.
# c,d are maps from (i,j) to c_i_j or d_i_j.
# o stores the output variables.
def writeARRAYMULT(col_constraints, x,y,c,d,t,o,numBits):
    # Tableau constraints: x_i AND y_row = t_i_row
    for row in range(numBits):
        for i in range(numBits):
            col = row+i
            writeAND(col_constraints, col,t[(i,row)],x[i],y[row])
    writeARRAYSUM(col_constraints,c,d,t,o,numBits)

# x,y are inputs to the array multiplier. t stores the tableau.
# c,d are maps from (i,j) to c_i_j or d_i_j.
# o stores the output variables.
def writeALGEBRA_ARRAYMULT(col_constraints, x,y,t,o,numBits):
    # Tableau constraints: x_i AND y_row = t_i_row
    for row in range(numBits):
        for i in range(numBits):
            col = row+i
            writeAND(col_constraints, col,t[(i,row)],x[i],y[row])
    clause = ""
    for row in range(numBits):
        for i in range(numBits):
            col = row+i
            clause += "+%d x%d " % (2**col,t[(i,row)])
    for i in range(2*numBits):
        clause += "-%d x%d " % (2**i,o[i])
    clause += "= 0; \n"
    col_constraints[0].append(clause)

# x,y are inputs to the array multiplier. t stores the tableau.
# c,d are maps from (i,j) to c_i_j or d_i_j.
# o stores the output variables.
def writeALGEBRA_ARRAYSUM(col_constraints,t,o,numBits):
    clause = ""
    for row in range(numBits):
        for i in range(numBits):
            col = row+i
            clause += "+%d x%d " % (2**col,t[(i,row)])
    for i in range(2*numBits):
        clause += "-%d x%d " % (2**i,o[i])
    clause += "= 0; \n"
    col_constraints[0].append(clause)


# Returns a mapping t from (l,i,j) to wallace tableau (or other) variables t_l_i_j, as well as nextDIMACS.
# t_l_i_j is the tableau variable in layer l occupying the i-th column
# and j-th row.
# Iteratively constructs the next layer from the previous one.
#
# returns the correct nextDIMACS value.
def createWALLACEVARS(inDIMACS,f_key,label,numBits):
    nextDIMACS = inDIMACS
    f_key.write("\n WRITING t VARIABLES \n")
    t = {}
    # Create initial tableau at layer = 0
    layer = 0
    for col in range(numBits):
        for row in range(col+1):
            t[(0,col,row)] = nextDIMACS
            f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d_%d_%d \n" % (layer, col, row))
            nextDIMACS += 1
    for col in range(numBits,2*numBits-1):
        for row in range(2*numBits-col-1):
            t[(0,col,row)] = nextDIMACS
            f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d_%d_%d \n" % (layer, col, row))
            nextDIMACS += 1
    num_rows = numBits

    # Create next layer from previous one.
    while(num_rows > 2):
        previous_num_rows = num_rows
        previous_layer = layer
        layer += 1

        # Figure out value of previous_num_cols by checking the keys of t
        previous_num_cols = 0
        while((previous_layer, previous_num_cols, 0) in t):
            previous_num_cols += 1
        
        # adders[row] contains the r-th row of adders represented as a list
        # of pairs: (col, 'a') for a two-output adder
        #           (col, 'w') for a one-output wire.
        adders = []
        # Group together every 3 rows of the previous tableau:
        # (3*adder_row, 3*adder_row+1, 3*adder_row+2)
        for adder_row in range((previous_num_rows / 3) + 1):
            a_row = []
            for col in range(previous_num_cols):
                # two-output adder
                if (previous_layer, col, 3*adder_row) in t and (previous_layer, col, 3*adder_row+1) in t:
                    a_row += [(col,'a')]
                # one-output wire
                elif (previous_layer, col, 3*adder_row) in t:
                    a_row += [(col,'w')]
            if len(a_row) > 0:
                adders += [a_row]

        # Create tableau variables for this layer.
        for adder_row in range(len(adders)):
            a_row = adders[adder_row]
            last_col = a_row[-1][0]
            for adder in a_row:
                col = adder[0]
                adder_type = adder[1]

                # The carry-bit always shifts up a row unless this is the last adder.
                if adder_type == "a" and col != last_col:
                    t[(layer,col+1,2*adder_row+1)] = nextDIMACS
                    f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d_%d_%d \n" % (layer, col+1, 2*adder_row+1))
                    nextDIMACS += 1

                    t[(layer,col,2*adder_row)] = nextDIMACS
                    f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d_%d_%d \n" % (layer,col,2*adder_row))
                    nextDIMACS += 1

                elif adder_type == "a" and col == last_col:
                    t[(layer,col+1,2*adder_row)] = nextDIMACS
                    f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d_%d_%d \n" % (layer, col+1, 2*adder_row))
                    nextDIMACS += 1

                    t[(layer,col,2*adder_row)] = nextDIMACS
                    f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d_%d_%d \n" % (layer,col,2*adder_row))
                    nextDIMACS += 1   

                elif adder_type == "w":
                    t[(layer,col,2*adder_row)] = nextDIMACS
                    f_key.write(("DEFINING %d FOR " % nextDIMACS) + label + "_%d_%d_%d \n" % (layer,col,2*adder_row))
                    nextDIMACS += 1   


        # Now find how many rows were produced.
        # The tallest column will not be at an endpoint.
        num_rows = 0
        for col in range(previous_num_cols):
            length = 0
            while((layer,col,length) in t):
                length += 1
            num_rows = max(num_rows, length)
    return (t, nextDIMACS)

# Helper method giving number of layers in a given Wallace tree multiplier.
def num_wallace_layers(numBits):
    nextDIMACS = 1
    f_key = open("temp_layer_count",'w')
    # dummy value of nextDIMACS
    t, nextDIMACS = createWALLACEVARS(nextDIMACS,f_key,'t',numBits)
    num_layers = 0
    for key in t:
        if key[0]+1 > num_layers:
            num_layers = key[0]+1
    f_key.close()
    os.remove("temp_layer_count")
    return num_layers
    
# This Wallace Multiplier uses a ripple-carry adder to sum the final layer.
#
# x,y are n-bit inputs to the array multiplier.
# t is map from (l,i,j) to tableau variables t_l_i_j (generated by createWALLACEVARS).
# c stores the 2n carries in the 2n-bit ripple-carry adder
# zeroes is a 2n bitvector of zeroes used for padding.
# o is a length 2n+1 bitvector holding the output variables.
# However, o_{2n} is always 0, only have it for the RCA.
def writeWALLACEMULT(col_constraints, x,y,t,o,c,zeroes,numBits):
    # Write initial tableau values
    for i in range(numBits):
        for j in range(numBits):
            if i+j < numBits:
                writeAND(col_constraints, i+j, t[(0, i+j, j)], x[i], y[j])
            else:
                writeAND(col_constraints, i+j, t[(0, i+j, numBits-i-1)], x[i], y[j])    
    writeWALLACESUM(col_constraints,t,o,c,zeroes,numBits)


def writeWALLACESUM(col_constraints,t,o,c,zeroes,numBits):
    # Set zeroes
    for i in range(2*numBits):
        writeFALSE(col_constraints,i,zeroes[i])
    
    # Check number of layers
    num_layers = 0
    for key in t:
        if key[0]+1 > num_layers:
            num_layers = key[0]+1
    
    # Connect adder outputs from curr_layer to next_layer.
    for curr_layer in range(num_layers-1):
        # Find number of columns in curr_layer
        num_cols = 0
        while((curr_layer, num_cols, 0) in t):
            num_cols += 1
        # Find number of rows in curr_layer
        num_rows = 0
        for col in range(num_cols):
            length = 0
            while((curr_layer,col,length) in t):
                length += 1
            num_rows = max(num_rows, length)
        
        # adders[row] contains the row-th row of adders represented as a list
        # of pairs: (col, 'full') for a full adder,
        #           (col, 'half') for a half adder,
        #           (col, 'wire') for a one-output wire.
        adders = []
        # Group together every 3 rows of the tableau:
        # (3*adder_row, 3*adder_row+1, 3*adder_row+2)
        for adder_row in range((num_rows / 3) + 1):
            a_row = []
            for col in range(num_cols):
                # full adder
                if (curr_layer, col, 3*adder_row) in t and (curr_layer, col, 3*adder_row+1) in t and (curr_layer, col, 3*adder_row+2) in t:
                    a_row += [(col,"full")]
                # half adder
                elif (curr_layer, col, 3*adder_row) in t and (curr_layer, col, 3*adder_row+1) in t:
                    a_row += [(col,"half")]
                # one-output wire
                elif (curr_layer, col, 3*adder_row) in t:
                    a_row += [(col,"wire")]
            if len(a_row) > 0:
                adders += [a_row]

        # Now connect adder outputs to the next layer.
        #
        # adder_row contains adders taking input from
        # rows (adder_row, adder_row+1, adder_row+2) of curr_layer.
        # These adders output to rows (2*adder_row, 2*adder_row + 1) of curr_layer+1.
        for adder_row in range(len(adders)):
            a_row = adders[adder_row]
            last_col = a_row[-1][0]
            for adder in a_row:
                col = adder[0]
                adder_type = adder[1]

                # The carry-bit always shifts up a row unless this is the last adder of the adder_row.
                if adder_type == "full" and col != last_col:
                    writeFULLADDER(col_constraints, col, t[(curr_layer,col,3*adder_row)], t[(curr_layer,col,3*adder_row+1)], t[(curr_layer,col,3*adder_row+2)],
                                   t[(curr_layer+1,col+1,2*adder_row+1)], t[(curr_layer+1,col,2*adder_row)])
                elif adder_type == "full" and col == last_col:
                    writeFULLADDER(col_constraints, col, t[(curr_layer,col,3*adder_row)], t[(curr_layer,col,3*adder_row+1)], t[(curr_layer,col,3*adder_row+2)],
                                   t[(curr_layer+1,col+1,2*adder_row)], t[(curr_layer+1,col,2*adder_row)])

                elif adder_type == "half" and col != last_col:
                    writeHALFADDER(col_constraints, col, t[(curr_layer,col,3*adder_row)], t[(curr_layer,col,3*adder_row+1)],
                                   t[(curr_layer+1,col+1,2*adder_row+1)], t[(curr_layer+1,col,2*adder_row)])                                
                elif adder_type == "half" and col == last_col:
                    writeHALFADDER(col_constraints, col, t[(curr_layer,col,3*adder_row)], t[(curr_layer,col,3*adder_row+1)],
                                   t[(curr_layer+1,col+1,2*adder_row)], t[(curr_layer+1,col,2*adder_row)])         

                elif adder_type == "wire":
                    writeEQUAL(col_constraints,col,t[(curr_layer,col,3*adder_row)],t[(curr_layer+1,col,2*adder_row)])
                    

    # Now put in a (2n-1)-bit ripple-carry adder to sum the final layer.
    top_row = []
    bot_row = []
    for i in range(2*numBits):
        top_row += [t[(num_layers-1,i,0)]]
    # We will need to pad the second row with zeroes where the variable is undefined.
    for i in range(2*numBits):
        if (num_layers-1,i,1) in t:
            bot_row += [t[(num_layers-1,i,1)]]
        else:
            bot_row += [zeroes[i]]
    # This adder takes (2n-1)-bit inputs and outputs a 2n-bit number, the final result.
    writeRIPPLECARRYADDER(col_constraints,top_row,bot_row,c,o,2*numBits)

# This bugged Wallace Multiplier uses a ripple-carry adder to sum the final layer.
#
# x,y are n-bit inputs to the array multiplier.
# t is map from (l,i,j) to tableau variables t_l_i_j (generated by createWALLACEVARS).
# c stores the 2n-1 carries in the 2n-1-bit ripple-carry adder
# zeroes is a 2n-1 bitvector of zeroes used for padding.
# o stores the 2n output variables.
def writeBUGGED_WALLACEMULT(col_constraints, x,y,t,o,c,zeroes,numBits):
    # Set zeroes
    for i in range(2*numBits-1):
        writeFALSE(col_constraints,i,zeroes[i])
    # Write initial tableau values
    for i in range(numBits):
        for j in range(numBits):
            if i+j < numBits:
                writeAND(col_constraints, i+j, t[(0, i+j, j)], x[i], y[j])
            else:
                writeAND(col_constraints, i+j, t[(0, i+j, numBits-i-1)], x[i], y[j])
    
    # Check number of layers
    num_layers = 0
    for key in t:
        if key[0]+1 > num_layers:
            num_layers = key[0]+1
    
    # Connect adder outputs from curr_layer to next_layer.
    for curr_layer in range(num_layers-1):
        # Find number of columns in curr_layer
        num_cols = 0
        while((curr_layer, num_cols, 0) in t):
            num_cols += 1
        # Find number of rows in curr_layer
        num_rows = 0
        for col in range(num_cols):
            length = 0
            while((curr_layer,col,length) in t):
                length += 1
            num_rows = max(num_rows, length)
        
        # adders[row] contains the row-th row of adders represented as a list
        # of pairs: (col, 'full') for a full adder,
        #           (col, 'half') for a half adder,
        #           (col, 'wire') for a one-output wire.
        adders = []
        # Group together every 3 rows of the tableau:
        # (3*adder_row, 3*adder_row+1, 3*adder_row+2)
        for adder_row in range((num_rows / 3) + 1):
            a_row = []
            for col in range(num_cols):
                # full adder
                if (curr_layer, col, 3*adder_row) in t and (curr_layer, col, 3*adder_row+1) in t and (curr_layer, col, 3*adder_row+2) in t:
                    a_row += [(col,"full")]
                # half adder
                elif (curr_layer, col, 3*adder_row) in t and (curr_layer, col, 3*adder_row+1) in t:
                    a_row += [(col,"half")]
                # one-output wire
                elif (curr_layer, col, 3*adder_row) in t:
                    a_row += [(col,"wire")]
            if len(a_row) > 0:
                adders += [a_row]

        # Now connect adder outputs to the next layer.
        #
        # adder_row contains adders taking input from
        # rows (adder_row, adder_row+1, adder_row+2) of curr_layer.
        # These adders output to rows (2*adder_row, 2*adder_row + 1) of curr_layer+1.
        for adder_row in range(len(adders)):
            a_row = adders[adder_row]
            for adder in a_row:
                col = adder[0]
                adder_type = adder[1]

                # The carry-bit always shifts up a row unless this is the last adder.
                if adder_type == "full" and col != num_cols-1:
                    writeFULLADDER(col_constraints, col, t[(curr_layer,col,3*adder_row)], t[(curr_layer,col,3*adder_row+1)], t[(curr_layer,col,3*adder_row+2)],
                                   t[(curr_layer+1,col+1,2*adder_row+1)], t[(curr_layer+1,col,2*adder_row)])
                elif adder_type == "full" and col == num_cols-1:
                    writeFULLADDER(col_constraints, col, t[(curr_layer,col,3*adder_row)], t[(curr_layer,col,3*adder_row+1)], t[(curr_layer,col,3*adder_row+2)],
                                   t[(curr_layer+1,col+1,2*adder_row)], t[(curr_layer+1,col,2*adder_row)])

                elif adder_type == "half" and col != num_cols-1:
                    writeHALFADDER(col_constraints, col, t[(curr_layer,col,3*adder_row)], t[(curr_layer,col,3*adder_row+1)],
                                   t[(curr_layer+1,col+1,2*adder_row+1)], t[(curr_layer+1,col,2*adder_row)])                                
                elif adder_type == "half" and col == num_cols-1:
                    writeHALFADDER(col_constraints, col, t[(curr_layer,col,3*adder_row)], t[(curr_layer,col,3*adder_row+1)],
                                   t[(curr_layer+1,col+1,2*adder_row)], t[(curr_layer+1,col,2*adder_row)])         

                elif adder_type == "wire":
                    writeEQUAL(col_constraints,col,t[(curr_layer,col,3*adder_row)],t[(curr_layer+1,col,2*adder_row)])
                    

    # Now put in a (2n-1)-bit ripple-carry adder to sum the final layer.
    top_row = []
    bot_row = []
    for i in range(2*numBits-1):
        top_row += [t[(num_layers-1,i,0)]]
    # We will need to pad the second row with zeroes where the variable is undefined.
    for i in range(2*numBits-1):
        if (num_layers-1,i,1) in t:
            bot_row += [t[(num_layers-1,i,1)]]
        else:
            bot_row += [zeroes[i]]
    # This adder takes (2n-1)-bit inputs and outputs a 2n-bit number, the final result.
    writeRIPPLECARRYADDER(col_constraints,top_row,bot_row,c,o,2*numBits-1)

# Second part of diagonal multiplier summing the t-variables.
def writeDIAGSUM(col_constraints,c,d,t,o,numBits):
    for row in range(numBits):
        for i in range(numBits):
            col = i+row
            # Zero-th row of adders: d_i_0 = t_i_0
            if row == 0 and col < numBits:
                writeEQUAL(col_constraints, col,d[(i,0)],t[(i,0)])
                
            # First row of adders
            elif row == 1:
                # Row endpoints
                if i == 0:
                    writeHALFADDER(col_constraints, col,d[(i+1,row-1)],t[(i,row)], c[(i,row)], d[(i,row)])
                elif i == numBits-1:
                    writeHALFADDER(col_constraints, col,c[(i-1,row)],t[(i,row)], c[(i,row)], d[(i,row)])
                # Middle of row
                else:
                    writeFULLADDER(col_constraints, col, c[(i-1,row)], d[(i+1,row-1)], t[(i,row)], c[(i,row)], d[(i,row)])
                    
            # Remaining rows of adders
            else:
                if i == 0:
                    writeHALFADDER(col_constraints, col,d[(i+1,row-1)],t[(i,row)], c[(i,row)], d[(i,row)])
                elif i == numBits-1:
                    writeFULLADDER(col_constraints, col, c[(i-1,row)], c[(i,row-1)], t[(i,row)], c[(i,row)], d[(i,row)])
                else:
                    writeFULLADDER(col_constraints, col, c[(i-1,row)], d[(i+1,row-1)], t[(i,row)], c[(i,row)], d[(i,row)])

    # Write to output variables.
    for col in range(numBits):
        writeEQUAL(col_constraints, col, d[(0,col)], o[col])
    for col in range(numBits,2*numBits-1):
        i = col - numBits + 1 
        writeEQUAL(col_constraints, col, d[(i,numBits-1)], o[col])
    # Last output is the leftmost adder's carry bit.
    col = 2*numBits-1
    writeEQUAL(col_constraints, col, c[(numBits-1,numBits-1)], o[col])

# x,y are inputs to the array multiplier. t stores the tableau.
# c,d are maps from (i,j) to c_i_j or d_i_j.
# o stores the output variables.
def writeDIAGMULT(col_constraints, x,y,c,d,t,o,numBits):
    # Tableau constraints: x_i AND y_row = t_i_row
    for row in range(numBits):
        for i in range(numBits):
            col = row+i
            writeAND(col_constraints, col,t[(i,row)],x[i],y[row])
    writeDIAGSUM(col_constraints,c,d,t,o,numBits)

    
