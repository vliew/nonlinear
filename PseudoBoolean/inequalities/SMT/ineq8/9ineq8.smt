(set-logic QF_BV)

(declare-const x (_ BitVec 18))
(declare-const x_temp (_ BitVec 9))
(assert (= x ((_ zero_extend 9) x_temp)))

(declare-const z (_ BitVec 18))
(declare-const z_temp (_ BitVec 9))
(assert (= z ((_ zero_extend 9) z_temp)))

(declare-const k (_ BitVec 18))
(declare-const k_temp (_ BitVec 9))
(assert (= k_temp #b010101010))
(assert (= k ((_ zero_extend 9) k_temp)))

(declare-const xoz (_ BitVec 18))
(assert (= xoz (bvor x z)))

(declare-const koz (_ BitVec 18))
(assert (= koz (bvor k z)))

(declare-const xoz_koz (_ BitVec 18))
(assert (= xoz_koz (bvmul xoz koz)))
(declare-const kx (_ BitVec 18))
(assert (= kx (bvmul k x)))

(assert (bvult xoz_koz kx))
(check-sat)
