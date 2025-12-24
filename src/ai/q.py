import numpy as np


class Q:
    def __init__(
        self,
        alpha=0.1,
        gamma=0.99,
        epsilon=1.0
    ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.vdiff_bins = np.linspace(-200, 200, 19)
        self.dx_bins = np.linspace(0, 400, 19)
        self.vel_bins = np.linspace(-15, 15, 14)

        self.n_v = len(self.vdiff_bins) + 1
        self.n_dx = len(self.dx_bins) + 1
        self.n_vel = len(self.vel_bins) + 1

        self.n_states = self.n_v * self.n_dx * self.n_vel
        self.Q = np.zeros((self.n_states, 2))

    def _bin_index(self, value, bins):
        return int(np.digitize([value], bins)[0])

    def get_state_index(self, vdiff, dx, vel):
        v_idx = self._bin_index(vdiff, self.vdiff_bins)
        dx_idx = self._bin_index(dx, self.dx_bins)
        vel_idx = self._bin_index(vel, self.vel_bins)
        return (v_idx * self.n_dx + dx_idx) * self.n_vel + vel_idx

    def take_action(self, s):
        if np.random.rand() < self.epsilon:
            return np.random.randint(2)
        return int(np.argmax(self.Q[s]))

    def update(self, s, a, r, s_next):
        td_target = r + self.gamma * np.max(self.Q[s_next])
        self.Q[s, a] += self.alpha * (td_target - self.Q[s, a])
