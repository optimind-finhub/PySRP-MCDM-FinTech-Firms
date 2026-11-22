import numpy as np
import pandas as pd


def _minmax_normalize(X, directions):
    norm = np.zeros_like(X, dtype=float)

    for j in range(X.shape[1]):
        c_min, c_max = X[:, j].min(), X[:, j].max()

        if c_max == c_min:
            norm[:, j] = 0
        elif directions[j] == 1:
            # Benefit criterion
            norm[:, j] = (X[:, j] - c_min) / (c_max - c_min)
        else:
            # Cost criterion
            norm[:, j] = (c_max - X[:, j]) / (c_max - c_min)

    return norm


def compute_mpsi(data, directions):
    """
    Compute MPSI weights (variance-based).

    Criteria are min-max normalised (cost criteria inverted), P_j is the sum of
    squared deviations of each normalised column from its mean, and
    W_j = P_j / sum_k P_k.  Weights are returned at full precision in 'Weight'
    and rounded to 4 d.p. (the precision used in the paper) in 'Weight_4dp'.

    Parameters
    ----------
    data : DataFrame or ndarray
        Decision matrix (criteria only)

    directions : list
        1 = benefit, 0 = cost

    Returns
    -------
    DataFrame
        Criterion, Pj, Weight
    """

    if isinstance(data, pd.DataFrame):
        criteria = data.columns.tolist()
        X = data.values.astype(float)
    else:
        X = np.asarray(data, dtype=float)
        criteria = [f"C{i+1}" for i in range(X.shape[1])]

    norm = _minmax_normalize(X, directions)

    aj = np.mean(norm, axis=0)
    pj = np.sum((norm - aj) ** 2, axis=0)

    if np.sum(pj) == 0:
        weights = np.ones(len(pj)) / len(pj)
    else:
        weights = pj / np.sum(pj)

    result = pd.DataFrame({
        "Criterion": criteria,
        "Pj": pj,
        "Weight": weights,
        "Weight_4dp": np.round(weights, 4)
    })

    return result