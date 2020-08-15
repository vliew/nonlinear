(set-logic QF_BV)

(declare-const x (_ BitVec 40))
(declare-const x_temp (_ BitVec 20))
(assert (= x ((_ zero_extend 20) x_temp)))

(declare-const z (_ BitVec 40))
(declare-const z_temp (_ BitVec 20))
(assert (= z ((_ zero_extend 20) z_temp)))

(declare-const k (_ BitVec 40))
(declare-const k_temp (_ BitVec 20))
(assert (= k_temp #b10101010101010101010))
(assert (= k ((_ zero_extend 20) k_temp)))

(declare-const xaz (_ BitVec 40))
(assert (= xaz (bvand x z)))

(declare-const kaz (_ BitVec 40))
(assert (= kaz (bvand k z)))

(declare-const xaz_kaz (_ BitVec 40))
(assert (= xaz_kaz (bvmul xaz kaz)))
(declare-const kx (_ BitVec 40))
(assert (= kx (bvmul k x)))

(assert (bvult kx xaz_kaz))
(check-sat)
