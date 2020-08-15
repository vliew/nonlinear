(set-logic QF_BV)

(declare-const x (_ BitVec 40))
(declare-const x_temp (_ BitVec 20))
(assert (= x ((_ zero_extend 20) x_temp)))

(declare-const k (_ BitVec 40))
(declare-const k_temp (_ BitVec 20))
(assert (= k_temp #b10101010101010101010))
(assert (= k ((_ zero_extend 20) k_temp)))

(declare-const xak (_ BitVec 40))
(assert (= xak (bvand x k)))

(declare-const z (_ BitVec 40))
(declare-const z_temp (_ BitVec 20))
(assert (= z ((_ zero_extend 20) z_temp)))

(declare-const xak_z (_ BitVec 40))
(declare-const kz (_ BitVec 40))
(assert (= xak_z (bvmul xak z)))
(assert (= kz (bvmul k z)))

(assert (bvult kz xak_z))
(check-sat)
