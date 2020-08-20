(set-logic QF_BV)

(declare-const x (_ BitVec 52))
(declare-const x_temp (_ BitVec 26))
(assert (= x ((_ zero_extend 26) x_temp)))

(declare-const k (_ BitVec 52))
(declare-const k_temp (_ BitVec 26))
(assert (= k_temp #b10101010101010101010101010))
(assert (= k ((_ zero_extend 26) k_temp)))

(declare-const xak (_ BitVec 52))
(assert (= xak (bvand x k)))

(declare-const xok (_ BitVec 52))
(assert (= xok (bvor x k)))

(declare-const z (_ BitVec 52))
(declare-const z_temp (_ BitVec 26))
(assert (= z ((_ zero_extend 26) z_temp)))

(declare-const xak_z (_ BitVec 52))
(declare-const xok_z (_ BitVec 52))
(assert (= xak_z (bvmul xak z)))
(assert (= xok_z (bvmul xok z)))

(assert (bvult xok_z xak_z))
(check-sat)
