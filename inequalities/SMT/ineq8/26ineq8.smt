(set-logic QF_BV)

(declare-const x (_ BitVec 52))
(declare-const x_temp (_ BitVec 26))
(assert (= x ((_ zero_extend 26) x_temp)))

(declare-const z (_ BitVec 52))
(declare-const z_temp (_ BitVec 26))
(assert (= z ((_ zero_extend 26) z_temp)))

(declare-const k (_ BitVec 52))
(declare-const k_temp (_ BitVec 26))
(assert (= k_temp #b10101010101010101010101010))
(assert (= k ((_ zero_extend 26) k_temp)))

(declare-const xoz (_ BitVec 52))
(assert (= xoz (bvor x z)))

(declare-const koz (_ BitVec 52))
(assert (= koz (bvor k z)))

(declare-const xoz_koz (_ BitVec 52))
(assert (= xoz_koz (bvmul xoz koz)))
(declare-const kx (_ BitVec 52))
(assert (= kx (bvmul k x)))

(assert (bvult xoz_koz kx))
(check-sat)
