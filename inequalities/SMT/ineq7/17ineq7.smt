(set-logic QF_BV)

(declare-const x (_ BitVec 34))
(declare-const x_temp (_ BitVec 17))
(assert (= x ((_ zero_extend 17) x_temp)))

(declare-const k (_ BitVec 34))
(declare-const k_temp (_ BitVec 17))
(assert (= k_temp #b01010101010101010))
(assert (= k ((_ zero_extend 17) k_temp)))

(declare-const xok (_ BitVec 34))
(assert (= xok (bvor x k)))

(declare-const z (_ BitVec 34))
(declare-const z_temp (_ BitVec 17))
(assert (= z ((_ zero_extend 17) z_temp)))

(declare-const xok_z (_ BitVec 34))
(declare-const kz (_ BitVec 34))
(assert (= xok_z (bvmul xok z)))
(assert (= kz (bvmul k z)))

(assert (bvult xok_z kz))
(check-sat)
