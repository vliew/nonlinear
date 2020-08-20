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

(declare-const xaz (_ BitVec 18))
(assert (= xaz (bvand x z)))

(declare-const kaz (_ BitVec 18))
(assert (= kaz (bvand k z)))

(declare-const xaz_kaz (_ BitVec 18))
(assert (= xaz_kaz (bvmul xaz kaz)))
(declare-const kx (_ BitVec 18))
(assert (= kx (bvmul k x)))

(assert (bvult kx xaz_kaz))
(check-sat)
