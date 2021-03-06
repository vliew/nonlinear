(set-logic QF_BV)

(declare-const x (_ BitVec 40))
(declare-const x_temp (_ BitVec 20))
(assert (= x ((_ zero_extend 20) x_temp)))

(declare-const k (_ BitVec 40))
(declare-const k_temp (_ BitVec 20))
(assert (= k_temp #b10101010101010101010))
(assert (= k ((_ zero_extend 20) k_temp)))

(declare-const xok (_ BitVec 40))
(assert (= xok (bvor x k)))

(declare-const z (_ BitVec 40))
(declare-const z_temp (_ BitVec 20))
(assert (= z ((_ zero_extend 20) z_temp)))

(declare-const xok_z (_ BitVec 40))
(declare-const kz (_ BitVec 40))
(assert (= xok_z (bvmul xok z)))
(assert (= kz (bvmul k z)))

(assert (bvult xok_z kz))
(check-sat)
