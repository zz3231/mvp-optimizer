"""
验证计算正确性 - 使用Excel中的相同数据
"""

import numpy as np
import sys
sys.path.append('.')

from optimizer import MeanVarianceOptimizer

# 从Excel截图中的数据
print("="*70)
print("测试：使用Excel中的相同数据")
print("="*70)

# Excel中的数据（从截图）
asset_names = ['Domestic Equity', 'Foreign Equity', 'Emerging Markets']
expected_returns = [0.10, 0.065, 0.085]  # 10%, 6.5%, 8.5%
volatilities = [0.16, 0.17, 0.20]  # 16%, 17%, 20%

# 相关性矩阵（需要从Excel中确认具体值）
# 先用典型值测试
correlation_matrix = np.array([
    [1.0, 0.5, 0.4],
    [0.5, 1.0, 0.25],
    [0.4, 0.25, 1.0]
])

risk_free_rate = 0.05  # 5%
risk_aversion = 3.0

print(f"\n输入数据:")
print(f"  Risk-Free Rate: {risk_free_rate:.2%}")
print(f"  Risk Aversion: {risk_aversion}")
print(f"\n资产数据:")
for i, name in enumerate(asset_names):
    print(f"  {name:20s}: Return={expected_returns[i]:.2%}, Vol={volatilities[i]:.2%}")

print(f"\n相关性矩阵:")
print(correlation_matrix)

# 创建优化器
optimizer = MeanVarianceOptimizer(
    asset_names=asset_names,
    expected_returns=expected_returns,
    volatilities=volatilities,
    correlation_matrix=correlation_matrix,
    risk_free_rate=risk_free_rate
)

print("\n" + "="*70)
print("无约束优化（允许做空）")
print("="*70)

# Tangency Portfolio - Unconstrained
constraints_unconstrained = {
    'lower_bounds': [-np.inf, -np.inf, -np.inf],
    'upper_bounds': [np.inf, np.inf, np.inf]
}

tangency = optimizer.find_tangency_portfolio(constraints_unconstrained)

if tangency:
    print("\nTangency Portfolio (Unconstrained):")
    print(f"  Expected Return: {tangency['expected_return']:.2%}")
    print(f"  Volatility: {tangency['volatility']:.2%}")
    print(f"  Sharpe Ratio: {tangency['sharpe_ratio']:.4f}")
    print(f"\n  Weights:")
    for asset, weight in tangency['weights_dict'].items():
        print(f"    {asset:20s}: {weight:8.2%}")

# Optimal Portfolio - Unconstrained with Risk-Free
optimal = optimizer.find_optimal_portfolio_with_riskfree(tangency, risk_aversion)

if optimal:
    print("\nOptimal Portfolio (Unconstrained, With Risk-Free):")
    print(f"  Expected Return: {optimal['expected_return']:.2%}")
    print(f"  Volatility: {optimal['volatility']:.2%}")
    print(f"  Sharpe Ratio: {optimal['sharpe_ratio']:.4f}")
    print(f"\n  Weight on Risk-Free: {optimal['weight_riskfree']:.2%}")
    print(f"  Weight on Tangency: {optimal['weight_tangency']:.2%}")
    print(f"\n  Weights on Risky Assets:")
    for asset, weight in optimal['weights_dict'].items():
        print(f"    {asset:20s}: {weight:8.2%}")

print("\n" + "="*70)
print("有约束优化（0-100%）")
print("="*70)

# Constrained
constraints_constrained = {
    'lower_bounds': [0.0, 0.0, 0.0],
    'upper_bounds': [1.0, 1.0, 1.0]
}

tangency_c = optimizer.find_tangency_portfolio(constraints_constrained)

if tangency_c:
    print("\nTangency Portfolio (Constrained):")
    print(f"  Expected Return: {tangency_c['expected_return']:.2%}")
    print(f"  Volatility: {tangency_c['volatility']:.2%}")
    print(f"  Sharpe Ratio: {tangency_c['sharpe_ratio']:.4f}")
    print(f"\n  Weights:")
    for asset, weight in tangency_c['weights_dict'].items():
        print(f"    {asset:20s}: {weight:8.2%}")

optimal_c = optimizer.find_optimal_portfolio_with_riskfree(tangency_c, risk_aversion)

if optimal_c:
    print("\nOptimal Portfolio (Constrained, With Risk-Free):")
    print(f"  Expected Return: {optimal_c['expected_return']:.2%}")
    print(f"  Volatility: {optimal_c['volatility']:.2%}")
    print(f"  Sharpe Ratio: {optimal_c['sharpe_ratio']:.4f}")
    print(f"\n  Weight on Risk-Free: {optimal_c['weight_riskfree']:.2%}")
    print(f"  Weight on Tangency: {optimal_c['weight_tangency']:.2%}")
    print(f"\n  Weights on Risky Assets:")
    for asset, weight in optimal_c['weights_dict'].items():
        print(f"    {asset:20s}: {weight:8.2%}")

print("\n" + "="*70)
print("验证：Sharpe Ratio是否一致")
print("="*70)
print(f"\nTangency Sharpe: {tangency['sharpe_ratio']:.6f}")
print(f"Optimal Sharpe:  {optimal['sharpe_ratio']:.6f}")
print(f"差异: {abs(tangency['sharpe_ratio'] - optimal['sharpe_ratio']):.6f}")

if abs(tangency['sharpe_ratio'] - optimal['sharpe_ratio']) < 1e-6:
    print("✓ Sharpe Ratio一致！计算正确！")
else:
    print("✗ Sharpe Ratio不一致，可能有问题")
