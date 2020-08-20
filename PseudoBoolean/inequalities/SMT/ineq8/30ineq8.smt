(set-logic QF_BV)

(declare-const x (_ BitVec 60))
(declare-const x_temp (_ BitVec 30))
(assert (= x ((_ zero_extend 30) x_temp)))

(declare-const z (_ BitVec 60))
(declare-const z_temp (_ BitVec 30))
(assert (= z ((_ zero_extend 30) z_temp)))

(declare-const k (_ BitVec 60))
(declare-const k_temp (_ BitVec 30))
(assert (= k_temp #b101010101010101010101010101010))
(assert (= k ((_ zero_extend 30) k_temp)))

(declare-const xoz (_ BitVec 60))
(assert (= xoz (bvor x z)))

(declare-const koz (_ BitVec 60))
(assert (= koz (bvor k z)))

(declare-const xoz_koz (_ BitVec 60))
(assert (= xoz_koz (bvmul xoz koz)))
(declare-const kx (_ BitVec 60))
(assert (= kx (bvmul k x)))

(assert (bvult xoz_koz kx))
(check-sat)
