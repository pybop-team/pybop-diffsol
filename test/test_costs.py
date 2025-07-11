from pybop_diffsol import DiffsolDense, DiffsolSparse, Config, CostType
import numpy as np

import pytest

solver_classes = [
    DiffsolDense,
    DiffsolSparse,
]

cost_types = [
    CostType.NegativeGaussianLogLikelihood,
    CostType.SumOfPower,
    CostType.Minkowski,
    CostType.SumOfSquares,
    CostType.MeanAbsoluteError,
    CostType.MeanSquaredError,
    CostType.RootMeanSquaredError,
]

dp = 0.1
k = 1.0
r = 1.0
y0 = 0.1
sigma = 0.1
n = 100
times = np.linspace(0.0, 1.0, n)
p = 2
def soln(times, r, k, y0):
    return k / (1.0 + (k - y0) * np.exp(-r * times) / y0)
def dsoln_dr(times, r, k, y0):
    return -k * (k - y0) * np.exp(-r * times) / (y0 * (1.0 + (k - y0) * np.exp(-r * times) / y0) ** 2)
def dsoln_dk(times, r, k, y0):
    return (1.0 + (k - y0) * np.exp(-r * times) / y0) ** -2
soln = soln(times, r, k, y0)
soln_dp = soln(times, r + dp, k + dp, y0)

cost_expected = [
    -0.5 * np.log(2 * np.PI) - np.log(sigma) - 0.5 * np.sum((soln - soln_dp) ** 2) / (sigma ** 2),  # NegativeGaussianLogLikelihood
    np.sum((soln - soln_dp) ** p),  # SumOfPower
    np.sum((soln - soln_dp) ** p) ** (1/p),  # Minkowski
    np.sum((soln - soln_dp) ** 2),  # SumOfSquares
    np.sum(np.abs(soln - soln_dp)) / n,  # MeanAbsoluteError
    np.sum((soln - soln_dp) ** 2) / n,  # MeanSquaredError
    np.sqrt(np.mean((soln - soln_dp) ** 2 / n)),  # RootMeanSquaredError
]

dsoln = np.array([dsoln_dr(times, r, k, y0), dsoln_dk(times, r, k, y0)])

sens_expected = [
    -np.sum((soln - soln_dp) * dsoln) / (sigma ** 2),  # NegativeGaussianLogLikelihood
    np.sum((soln - soln_dp) ** (p - 1) * dsoln),  # SumOfPower
    (1.0/p) * np.sum((soln - soln_dp) ** (p - 1) * dsoln) * np.sum((soln - soln_dp) ** p) ** ((1/p) - 1),  # Minkowski
    2 * np.sum((soln - soln_dp) * dsoln),  # SumOfSquares
    np.sum(np.sign(soln - soln_dp) * dsoln) / n,  # MeanAbsoluteError
    2 * np.sum((soln - soln_dp) * dsoln) / n,  # MeanSquaredError
    np.sum((soln - soln_dp) * dsoln) / (np.sqrt(n) * np.sqrt(np.mean((soln - soln_dp) ** 2))),  # RootMeanSquaredError
]

solver_cost_type_and_expected = [
    (cls, cost, expected) for cls in solver_classes for cost, expected in zip(cost_types, cost_expected)
]
solver_sens_type_and_expected = [
    (cls, cost, expected) for cls in solver_classes for cost, expected in zip(cost_types, sens_expected)
]



def test_sens_calculation():
    dr = dsoln_dr(times, r, k, y0)
    dk = dsoln_dk(times, r, k, y0)
    eps = 1e-5
    fd_dr = (soln(times, r + eps, k, y0) - soln(times, r - eps, k, y0)) / (2 * eps)
    fd_dk = (soln(times, r, k + eps, y0) - soln(times, r, k - eps, y0)) / (2 * eps)
    np.testing.assert_allclose(dr, fd_dr, rtol=1e-5)
    np.testing.assert_allclose(dk, fd_dk, rtol=1e-5)

model_str = """
in = [r, k]
r { 1 } k { 1 }
u_i { y = 0.1 }
F_i { (r * y) * (1 - (y / k)) }
"""

@pytest.mark.parametrize("solver_class, cost_type, expected", solver_cost_type_and_expected)
def test_costs(solver_class, cost_type, expected):
    config = Config()
    model = solver_class(model_str, config)

    model.set_params(np.array([r, k]))
    data = model.solve(times)

    if cost_type == CostType.NegativeGaussianLogLikelihood:
        model.set_params(np.array([r, k]), sigma=sigma)
    else:
        model.set_params(np.array([r, k]))

    cost = model.cost(times, data, cost_type)
    np.testing.assert_allclose(cost, expected, rtol=1e-5)

@pytest.mark.parametrize("solver_class, cost_type, expected", solver_sens_type_and_expected)
def test_sens(solver_class, cost_type, expected):
    config = Config()
    model = solver_class(model_str, config)

    model.set_params(np.array([r, k]))
    data = model.solve(times)

    if cost_type == CostType.NegativeGaussianLogLikelihood:
        model.set_params(np.array([r, k]), sigma=sigma)
    else:
        model.set_params(np.array([r, k]))

    cost = model.sens(times, data, cost_type)
    np.testing.assert_allclose(cost, expected, rtol=1e-5)
 
    