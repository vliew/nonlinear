(set-logic QF_BV)

(declare-const x (_ BitVec 50))
(declare-const x_temp (_ BitVec 25))
(assert (= x ((_ zero_extend 25) x_temp)))

(declare-const k (_ BitVec 50))
(declare-const k_temp (_ BitVec 25))
(assert (= k_temp #b0101010101010101010101010))
(assert (= k ((_ zero_extend 25) k_temp)))

(declare-const xok (_ BitVec 50))
(assert (= xok (bvor x k)))

(declare-const z (_ BitVec 50))
(declare-const z_temp (_ BitVec 25))
(assert (= z ((_ zero_extend 25) z_temp)))

(declare-const xok_z (_ BitVec 50))
(declare-const kz (_ BitVec 50))
(assert (= xok_z (bvmul xok z)))
(assert (= kz (bvmul k z)))

(assert (bvult xok_z kz))
(check-sat)
