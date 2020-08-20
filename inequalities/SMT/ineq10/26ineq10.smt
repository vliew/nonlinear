(set-logic QF_BV)

(declare-const x (_ BitVec 52))
(declare-const x_temp (_ BitVec 26))
(assert (= x ((_ zero_extend 26) x_temp)))

(declare-const z (_ BitVec 52))
(declare-const z_temp (_ BitVec 26))
(assert (= z ((_ zero_extend 26) z_temp)))

(declare-const k (_ BitVec 52))
(declare-const k_temp (_ BitVec 26))
(assert (= k_temp #b10101010101010101010101010))
(assert (= k ((_ zero_extend 26) k_temp)))

(declare-const xok (_ BitVec 52))
(assert (= xok (bvor x k)))

(declare-const xok_zpl1 (_ BitVec 52))
(assert (= xok_zpl1 (bvmul xok (bvadd z #b0000000000000000000000000000000000000000000000000001))))
(declare-const kz (_ BitVec 52))
(assert (= kz (bvmul k z)))

(assert (bvult xok_zpl1 (bvadd kz x)))
(check-sat)
