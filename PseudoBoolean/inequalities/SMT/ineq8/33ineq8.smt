(set-logic QF_BV)

(declare-const x (_ BitVec 66))
(declare-const x_temp (_ BitVec 33))
(assert (= x ((_ zero_extend 33) x_temp)))

(declare-const z (_ BitVec 66))
(declare-const z_temp (_ BitVec 33))
(assert (= z ((_ zero_extend 33) z_temp)))

(declare-const k (_ BitVec 66))
(declare-const k_temp (_ BitVec 33))
(assert (= k_temp #b010101010101010101010101010101010))
(assert (= k ((_ zero_extend 33) k_temp)))

(declare-const xoz (_ BitVec 66))
(assert (= xoz (bvor x z)))

(declare-const koz (_ BitVec 66))
(assert (= koz (bvor k z)))

(declare-const xoz_koz (_ BitVec 66))
(assert (= xoz_koz (bvmul xoz koz)))
(declare-const kx (_ BitVec 66))
(assert (= kx (bvmul k x)))

(assert (bvult xoz_koz kx))
(check-sat)
