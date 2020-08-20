# Constructs SMT formula to check:
# (x|z)(k|z) >= (kx)
# Where k is ...101010, & is bitwise-AND and | is bitwise-OR.
import sys
import os

def writeINEQ8(numBits):
    smtFileName = "benchmarks/%dineq8.smt" % (numBits)
    f_smt = open(smtFileName,'w')
    f_smt.write("(set-logic QF_BV)\n\n")

    f_smt.write("(declare-const x (_ BitVec %d))\n" % (2*numBits))
    f_smt.write("(declare-const x_temp (_ BitVec %d))\n" % numBits)
    f_smt.write("(assert (= x ((_ zero_extend %d) x_temp)))\n\n" % numBits)

    f_smt.write("(declare-const z (_ BitVec %d))\n" % (2*numBits))
    f_smt.write("(declare-const z_temp (_ BitVec %d))\n" % numBits)
    f_smt.write("(assert (= z ((_ zero_extend %d) z_temp)))\n\n" % numBits)
    
    f_smt.write("(declare-const k (_ BitVec %d))\n" % (2*numBits))
    f_smt.write("(declare-const k_temp (_ BitVec %d))\n" % numBits)
    extra = ""
    if numBits % 2 == 1:
        extra = "0"
    k_temp = extra + "10" * (numBits / 2) 
    f_smt.write("(assert (= k_temp #b%s))\n" % (k_temp))
    f_smt.write("(assert (= k ((_ zero_extend %d) k_temp)))\n\n" % numBits)

    f_smt.write("(declare-const xoz (_ BitVec %d))\n" % (2*numBits))
    f_smt.write("(assert (= xoz (bvor x z)))\n\n")

    f_smt.write("(declare-const koz (_ BitVec %d))\n" % (2*numBits))
    f_smt.write("(assert (= koz (bvor k z)))\n\n")

    f_smt.write("(declare-const xoz_koz (_ BitVec %d))\n" % (2*numBits))
    f_smt.write("(assert (= xoz_koz (bvmul xoz koz)))\n")

    f_smt.write("(declare-const kx (_ BitVec %d))\n" % (2*numBits))
    f_smt.write("(assert (= kx (bvmul k x)))\n\n")

    f_smt.write("(assert (bvult xoz_koz kx))\n")
    f_smt.write("(check-sat)\n")

if not os.path.exists("benchmarks"):
    os.makedirs("benchmarks")

for i in range(9,37):
    writeINEQ8(i)









    
