(set-logic QF_BV)

(declare-const x (_ BitVec 68))
(declare-const x_temp (_ BitVec 34))
(assert (= x ((_ zero_extend 34) x_temp)))

(declare-const k (_ BitVec 68))
(declare-const k_temp (_ BitVec 34))
(assert (= k_temp #b1010101010101010101010101010101010))
(assert (= k ((_ zero_extend 34) k_temp)))

(declare-const xok (_ BitVec 68))
(assert (= xok (bvor x k)))

(declare-const z (_ BitVec 68))
(declare-const z_temp (_ BitVec 34))
(assert (= z ((_ zero_extend 34) z_temp)))

(declare-const xok_z (_ BitVec 68))
(declare-const kz (_ BitVec 68))
(assert (= xok_z (bvmul xok z)))
(assert (= kz (bvmul k z)))

(assert (bvult xok_z kz))
(check-sat)
