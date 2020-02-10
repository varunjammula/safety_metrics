class SafetyMetrics:
    def __init__(self):
        print("Loading Safety Metrics")

    def compute_SEV_longitudinal(self, vel_fol, vel_lead, rho, acc_fol, acc_max_brake_lead, acc_min_brake_fol):
        # vr - follwing_vel, vf- leading_vel, a_accel - following_acc_inst, a_max_brake -  max dec of leading, a_min_brake -  min_dec of following
        d_long = ((vel_fol * rho) + 0.5 * acc_fol * rho ** 2 + (vel_fol + rho * acc_fol ** 2) / (2 * acc_min_brake_fol) - vel_lead ** 2 / (
                2 * acc_max_brake_lead))
        return d_long

    def compute_SEV_lateral(self, v1, v2, mu, rho, alat_max_brake, alat_min_brake):
        v1_rho = v1 + rho * alat_max_brake
        v2_rho = v2 - rho * alat_max_brake
        d_lat = mu + (((v1 + v1_rho) * rho) / 2 + (v1_rho ** 2 / 2 * alat_min_brake) - ((v2 + v2_rho) * rho) / 2 - (
                    v2_rho ** 2 / 2 * alat_min_brake))
        return d_lat

    def compute_SEV_longitudinal_opposite(self, v1, v2, rho, a_min_brake, a_min_brake_correct, a_max_acc):
        v1_rho = v1 + rho * a_max_acc
        v2_rho = abs(v2) + rho * a_max_acc
        d_long_opp = (((v1 + v1_rho) * rho) / 2 + (v1_rho ** 2 / 2 * a_min_brake_correct) + (
                    (abs(v2) + v2_rho) * rho) / 2 + (v2_rho ** 2 / 2 * a_min_brake))
        return d_long_opp

    def compute_SER(self):
        return

    def compute_SEF_lat(self):
        return

    def compute_SECE(self):
        return

    def compute_TTC(self, X_L, X_F, I_L, V_F, V_L):
        return (X_L - X_F - I_L) / (V_F - V_L)

    def compute_MTTC(self):
        return

    def compute_PET(self):
        return

    def compute_CI(self):
        return

    def compute_EA(self):
        return

    def compute_AD(self):
        return

    def compute_RRV(self):
        return

    def compute_HTCDE(self):
        return

    def compute_HTCVR(self):
        return

    def compute_HTCA(self):
        self.compute_HTCDE()
        self.compute_HTCVR()
        return

    def compute_ECER(self):
        return

    def compute_ETER(self):
        return

    def compute_LE(self):
        return

    def compute_ABC(self):
        return

    def compute_ADSA(self):
        return
