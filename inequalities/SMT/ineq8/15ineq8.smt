(set-logic QF_BV)

(declare-const x (_ BitVec 30))
(declare-const x_temp (_ BitVec 15))
(assert (= x ((_ zero_extend 15) x_temp)))

(declare-const z (_ BitVec 30))
(declare-const z_temp (_ BitVec 15))
(assert (= z ((_ zero_extend 15) z_temp)))

(declare-const k (_ BitVec 30))
(declare-const k_temp (_ BitVec 15))
(assert (= k_temp #b010101010101010))
(assert (= k ((_ zero_extend 15) k_temp)))

(declare-const xoz (_ BitVec 30))
(assert (= xoz (bvor x z)))

(declare-const koz (_ BitVec 30))
(assert (= koz (bvor k z)))

(declare-const xoz_koz (_ BitVec 30))
(assert (= xoz_koz (bvmul xoz koz)))
(declare-const kx (_ BitVec 30))
(assert (= kx (bvmul k x)))

(assert (bvult xoz_koz kx))
(check-sat)
