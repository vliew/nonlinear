(set-logic QF_BV)

(declare-const x (_ BitVec 48))
(declare-const x_temp (_ BitVec 24))
(assert (= x ((_ zero_extend 24) x_temp)))

(declare-const z (_ BitVec 48))
(declare-const z_temp (_ BitVec 24))
(assert (= z ((_ zero_extend 24) z_temp)))

(declare-const k (_ BitVec 48))
(declare-const k_temp (_ BitVec 24))
(assert (= k_temp #b101010101010101010101010))
(assert (= k ((_ zero_extend 24) k_temp)))

(declare-const xoz (_ BitVec 48))
(assert (= xoz (bvor x z)))

(declare-const koz (_ BitVec 48))
(assert (= koz (bvor k z)))

(declare-const xoz_koz (_ BitVec 48))
(assert (= xoz_koz (bvmul xoz koz)))
(declare-const kx (_ BitVec 48))
(assert (= kx (bvmul k x)))

(assert (bvult xoz_koz kx))
(check-sat)
