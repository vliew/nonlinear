(set-logic QF_BV)

(declare-const x (_ BitVec 46))
(declare-const x_temp (_ BitVec 23))
(assert (= x ((_ zero_extend 23) x_temp)))

(declare-const k (_ BitVec 46))
(declare-const k_temp (_ BitVec 23))
(assert (= k_temp #b01010101010101010101010))
(assert (= k ((_ zero_extend 23) k_temp)))

(declare-const xak (_ BitVec 46))
(assert (= xak (bvand x k)))

(declare-const z (_ BitVec 46))
(declare-const z_temp (_ BitVec 23))
(assert (= z ((_ zero_extend 23) z_temp)))

(declare-const xak_z (_ BitVec 46))
(declare-const kz (_ BitVec 46))
(assert (= xak_z (bvmul xak z)))
(assert (= kz (bvmul k z)))

(assert (bvult kz xak_z))
(check-sat)
