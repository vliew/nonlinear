(set-logic QF_BV)

(declare-const x (_ BitVec 58))
(declare-const x_temp (_ BitVec 29))
(assert (= x ((_ zero_extend 29) x_temp)))

(declare-const z (_ BitVec 58))
(declare-const z_temp (_ BitVec 29))
(assert (= z ((_ zero_extend 29) z_temp)))

(declare-const k (_ BitVec 58))
(declare-const k_temp (_ BitVec 29))
(assert (= k_temp #b01010101010101010101010101010))
(assert (= k ((_ zero_extend 29) k_temp)))

(declare-const xoz (_ BitVec 58))
(assert (= xoz (bvor x z)))

(declare-const koz (_ BitVec 58))
(assert (= koz (bvor k z)))

(declare-const xoz_koz (_ BitVec 58))
(assert (= xoz_koz (bvmul xoz koz)))
(declare-const kx (_ BitVec 58))
(assert (= kx (bvmul k x)))

(assert (bvult xoz_koz kx))
(check-sat)
