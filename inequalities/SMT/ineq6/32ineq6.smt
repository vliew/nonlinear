(set-logic QF_BV)

(declare-const x (_ BitVec 64))
(declare-const x_temp (_ BitVec 32))
(assert (= x ((_ zero_extend 32) x_temp)))

(declare-const k (_ BitVec 64))
(declare-const k_temp (_ BitVec 32))
(assert (= k_temp #b10101010101010101010101010101010))
(assert (= k ((_ zero_extend 32) k_temp)))

(declare-const xak (_ BitVec 64))
(assert (= xak (bvand x k)))

(declare-const z (_ BitVec 64))
(declare-const z_temp (_ BitVec 32))
(assert (= z ((_ zero_extend 32) z_temp)))

(declare-const xak_z (_ BitVec 64))
(declare-const kz (_ BitVec 64))
(assert (= xak_z (bvmul xak z)))
(assert (= kz (bvmul k z)))

(assert (bvult kz xak_z))
(check-sat)
