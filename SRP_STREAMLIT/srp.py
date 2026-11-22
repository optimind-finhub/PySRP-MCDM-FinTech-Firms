import numpy as np
import pandas as pd


class SRP:
    """Simple Ranking Process (SRP).

    Steps (as in the PySRP paper, Section 3.2):
      1. weights W_j (used as supplied; see _prepare_weights)
      2. rank matrix R   : rank 1 = best; benefit -> descending, cost -> ascending
      3. Theta = W_j * R_ij
      4. TRS_i = sum_j Theta_ij
      5. S_i   = m - TRS_i
      6. final rank by S descending

    Ties: competition ranking (method='min') - tied alternatives share the best
    rank of the tied group (e.g. the seven zero-RVS firms all get rank 4).
    This is the tie rule that reproduces the published tables.
    """

    # weights whose sum is within this tolerance of 1 are used exactly as supplied.
    # (MPSI weights displayed to 4 d.p. sum to 1.0001; renormalising them would
    #  change TRS in the 4th decimal and no longer match the published results.)
    SUM_TOL = 1e-3

    def __init__(self, matrix, weights, alternatives=None, n_benefit=1):

        self.matrix = np.array(matrix, dtype=float)
        self.weights = self._prepare_weights(weights)

        self.m, self.n = self.matrix.shape
        self.n_benefit = n_benefit

        if self.weights.shape[0] != self.n:
            raise ValueError("Number of weights must equal number of criteria.")

        if alternatives is None:
            self.alternatives = [f"A{i+1}" for i in range(self.m)]
        else:
            self.alternatives = alternatives

    @classmethod
    def _prepare_weights(cls, weights):
        w = np.array(weights, dtype=float)
        s = w.sum()
        if s <= 0:
            raise ValueError("Sum of weights must be positive.")
        # Algorithm 1, step 1: normalise raw weights (e.g. equal weights 1.0000 each)
        if abs(s - 1.0) > cls.SUM_TOL:
            w = w / s
        return w

    def ranking_matrix(self):

        R = np.zeros((self.m, self.n), dtype=int)

        for j in range(self.n):

            col = pd.Series(self.matrix[:, j])

            R[:, j] = col.rank(
                ascending=(j >= self.n_benefit),   # benefit: largest = rank 1
                method="min"
            ).astype(int)

        self.R = R

    def weighted_matrix(self):
        self.Theta = self.R * self.weights

    def total_rank_score(self):
        self.TRS = np.sum(self.Theta, axis=1)

    def compute_S(self):
        self.S = self.m - self.TRS

    def final_rank(self):
        # highest S = rank 1; equal S share a rank (no arbitrary tie-breaking)
        self.Rank = (
            pd.Series(self.S).rank(ascending=False, method="min").astype(int).values
        )

    def rank(self):

        self.ranking_matrix()
        self.weighted_matrix()
        self.total_rank_score()
        self.compute_S()
        self.final_rank()

        return pd.DataFrame({
            "Alternative": self.alternatives,
            "TRS": self.TRS,
            "S": self.S,
            "Rank": self.Rank
        }).sort_values("Rank", kind="stable")
