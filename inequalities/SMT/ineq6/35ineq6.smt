(set-logic QF_BV)

(declare-const x (_ BitVec 70))
(declare-const x_temp (_ BitVec 35))
(assert (= x ((_ zero_extend 35) x_temp)))

(declare-const k (_ BitVec 70))
(declare-const k_temp (_ BitVec 35))
(assert (= k_temp #b01010101010101010101010101010101010))
(assert (= k ((_ zero_extend 35) k_temp)))

(declare-const xak (_ BitVec 70))
(assert (= xak (bvand x k)))

(declare-const z (_ BitVec 70))
(declare-const z_temp (_ BitVec 35))
(assert (= z ((_ zero_extend 35) z_temp)))

(declare-const xak_z (_ BitVec 70))
(declare-const kz (_ BitVec 70))
(assert (= xak_z (bvmul xak z)))
(assert (= kz (bvmul k z)))

(assert (bvult kz xak_z))
(check-sat)
