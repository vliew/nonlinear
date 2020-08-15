(set-logic QF_BV)

(declare-const x (_ BitVec 20))
(declare-const x_temp (_ BitVec 10))
(assert (= x ((_ zero_extend 10) x_temp)))

(declare-const z (_ BitVec 20))
(declare-const z_temp (_ BitVec 10))
(assert (= z ((_ zero_extend 10) z_temp)))

(declare-const k (_ BitVec 20))
(declare-const k_temp (_ BitVec 10))
(assert (= k_temp #b1010101010))
(assert (= k ((_ zero_extend 10) k_temp)))

(declare-const xoz (_ BitVec 20))
(assert (= xoz (bvor x z)))

(declare-const koz (_ BitVec 20))
(assert (= koz (bvor k z)))

(declare-const xoz_koz (_ BitVec 20))
(assert (= xoz_koz (bvmul xoz koz)))
(declare-const kx (_ BitVec 20))
(assert (= kx (bvmul k x)))

(assert (bvult xoz_koz kx))
(check-sat)
