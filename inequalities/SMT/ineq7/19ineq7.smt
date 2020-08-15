(set-logic QF_BV)

(declare-const x (_ BitVec 38))
(declare-const x_temp (_ BitVec 19))
(assert (= x ((_ zero_extend 19) x_temp)))

(declare-const k (_ BitVec 38))
(declare-const k_temp (_ BitVec 19))
(assert (= k_temp #b0101010101010101010))
(assert (= k ((_ zero_extend 19) k_temp)))

(declare-const xok (_ BitVec 38))
(assert (= xok (bvor x k)))

(declare-const z (_ BitVec 38))
(declare-const z_temp (_ BitVec 19))
(assert (= z ((_ zero_extend 19) z_temp)))

(declare-const xok_z (_ BitVec 38))
(declare-const kz (_ BitVec 38))
(assert (= xok_z (bvmul xok z)))
(assert (= kz (bvmul k z)))

(assert (bvult xok_z kz))
(check-sat)
