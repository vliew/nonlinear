(set-logic QF_BV)

(declare-const x (_ BitVec 32))
(declare-const x_temp (_ BitVec 16))
(assert (= x ((_ zero_extend 16) x_temp)))

(declare-const z (_ BitVec 32))
(declare-const z_temp (_ BitVec 16))
(assert (= z ((_ zero_extend 16) z_temp)))

(declare-const k (_ BitVec 32))
(declare-const k_temp (_ BitVec 16))
(assert (= k_temp #b1010101010101010))
(assert (= k ((_ zero_extend 16) k_temp)))

(declare-const xaz (_ BitVec 32))
(assert (= xaz (bvand x z)))

(declare-const kaz (_ BitVec 32))
(assert (= kaz (bvand k z)))

(declare-const xaz_kaz (_ BitVec 32))
(assert (= xaz_kaz (bvmul xaz kaz)))
(declare-const kx (_ BitVec 32))
(assert (= kx (bvmul k x)))

(assert (bvult kx xaz_kaz))
(check-sat)
