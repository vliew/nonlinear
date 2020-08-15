(set-logic QF_BV)

(declare-const x (_ BitVec 42))
(declare-const x_temp (_ BitVec 21))
(assert (= x ((_ zero_extend 21) x_temp)))

(declare-const k (_ BitVec 42))
(declare-const k_temp (_ BitVec 21))
(assert (= k_temp #b010101010101010101010))
(assert (= k ((_ zero_extend 21) k_temp)))

(declare-const xok (_ BitVec 42))
(assert (= xok (bvor x k)))

(declare-const z (_ BitVec 42))
(declare-const z_temp (_ BitVec 21))
(assert (= z ((_ zero_extend 21) z_temp)))

(declare-const xok_z (_ BitVec 42))
(declare-const kz (_ BitVec 42))
(assert (= xok_z (bvmul xok z)))
(assert (= kz (bvmul k z)))

(assert (bvult xok_z kz))
(check-sat)
