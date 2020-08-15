(set-logic QF_BV)

(declare-const x (_ BitVec 66))
(declare-const x_temp (_ BitVec 33))
(assert (= x ((_ zero_extend 33) x_temp)))

(declare-const z (_ BitVec 66))
(declare-const z_temp (_ BitVec 33))
(assert (= z ((_ zero_extend 33) z_temp)))

(declare-const k (_ BitVec 66))
(declare-const k_temp (_ BitVec 33))
(assert (= k_temp #b010101010101010101010101010101010))
(assert (= k ((_ zero_extend 33) k_temp)))

(declare-const xok (_ BitVec 66))
(assert (= xok (bvor x k)))

(declare-const xok_zpl1 (_ BitVec 66))
(assert (= xok_zpl1 (bvmul xok (bvadd z #b000000000000000000000000000000000000000000000000000000000000000001))))
(declare-const kz (_ BitVec 66))
(assert (= kz (bvmul k z)))

(assert (bvult xok_zpl1 (bvadd kz x)))
(check-sat)
