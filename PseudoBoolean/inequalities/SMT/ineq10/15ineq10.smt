(set-logic QF_BV)

(declare-const x (_ BitVec 30))
(declare-const x_temp (_ BitVec 15))
(assert (= x ((_ zero_extend 15) x_temp)))

(declare-const z (_ BitVec 30))
(declare-const z_temp (_ BitVec 15))
(assert (= z ((_ zero_extend 15) z_temp)))

(declare-const k (_ BitVec 30))
(declare-const k_temp (_ BitVec 15))
(assert (= k_temp #b010101010101010))
(assert (= k ((_ zero_extend 15) k_temp)))

(declare-const xok (_ BitVec 30))
(assert (= xok (bvor x k)))

(declare-const xok_zpl1 (_ BitVec 30))
(assert (= xok_zpl1 (bvmul xok (bvadd z #b000000000000000000000000000001))))
(declare-const kz (_ BitVec 30))
(assert (= kz (bvmul k z)))

(assert (bvult xok_zpl1 (bvadd kz x)))
(check-sat)
