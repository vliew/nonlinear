(set-logic QF_BV)

(declare-const x (_ BitVec 62))
(declare-const x_temp (_ BitVec 31))
(assert (= x ((_ zero_extend 31) x_temp)))

(declare-const k (_ BitVec 62))
(declare-const k_temp (_ BitVec 31))
(assert (= k_temp #b0101010101010101010101010101010))
(assert (= k ((_ zero_extend 31) k_temp)))

(declare-const xok (_ BitVec 62))
(assert (= xok (bvor x k)))

(declare-const z (_ BitVec 62))
(declare-const z_temp (_ BitVec 31))
(assert (= z ((_ zero_extend 31) z_temp)))

(declare-const xok_z (_ BitVec 62))
(declare-const kz (_ BitVec 62))
(assert (= xok_z (bvmul xok z)))
(assert (= kz (bvmul k z)))

(assert (bvult xok_z kz))
(check-sat)
