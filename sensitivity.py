"""
Sensitivity Analysis Module
Analyze the cost of using wrong parameter estimates
"""

import numpy as np
import pandas as pd
from optimizer import MeanVarianceOptimizer


class SensitivityAnalyzer:
    """
    Analyze the cost of using wrong parameter estimates
    
    Key concept: Optimize using 'wrong' inputs, then evaluate portfolio
    performance under 'true' market conditions to quantify the cost of error.
    """
    
    def __init__(self, base_optimizer, base_optimal_weights):
        """
        Parameters:
        -----------
        base_optimizer : MeanVarianceOptimizer
            Optimizer with 'true' parameters
        base_optimal_weights : array
            Optimal weights based on 'true' parameters
        """
        self.base_optimizer = base_optimizer
        self.base_weights = base_optimal_weights
        
        # Calculate base portfolio metrics using TRUE parameters
        self.base_return = base_optimizer.portfolio_return(base_optimal_weights)
        self.base_volatility = base_optimizer.portfolio_volatility(base_optimal_weights)
        self.base_sharpe = base_optimizer.portfolio_sharpe_ratio(base_optimal_weights)
    
    def analyze_return_sensitivity(self, percentage_change=0.01, risk_aversion=3.0, 
                                   constraints=None, use_riskless=True):
        """
        Analyze impact of wrong expected return estimates
        
        For each asset:
        1. Change its expected return by +/- percentage_change
        2. Optimize portfolio using this wrong input
        3. Evaluate this portfolio using true parameters
        4. Calculate the impact (difference in metrics)
        """
        results = []
        
        for asset_idx in range(self.base_optimizer.n_assets):
            asset_name = self.base_optimizer.asset_names[asset_idx]
            
            for direction, multiplier in [('decrease', -1), ('increase', 1)]:
                # Create wrong input
                wrong_returns = self.base_optimizer.expected_returns.copy()
                wrong_returns[asset_idx] += multiplier * percentage_change
                
                # Optimize using wrong input
                wrong_optimizer = MeanVarianceOptimizer(
                    asset_names=self.base_optimizer.asset_names,
                    expected_returns=wrong_returns,
                    volatilities=self.base_optimizer.volatilities,
                    correlation_matrix=self.base_optimizer.correlation_matrix,
                    risk_free_rate=self.base_optimizer.risk_free_rate
                )
                
                # Get optimal portfolio using wrong parameters
                if use_riskless:
                    tangency = wrong_optimizer.find_tangency_portfolio(constraints)
                    if tangency:
                        wrong_optimal = wrong_optimizer.find_optimal_portfolio_with_riskfree(
                            tangency, risk_aversion
                        )
                    else:
                        continue
                else:
                    wrong_optimal = wrong_optimizer.find_optimal_portfolio_without_riskfree(
                        risk_aversion, constraints
                    )
                
                if wrong_optimal is None:
                    continue
                
                wrong_weights = wrong_optimal['weights']
                
                # Evaluate using TRUE parameters
                true_return = self.base_optimizer.portfolio_return(wrong_weights)
                true_volatility = self.base_optimizer.portfolio_volatility(wrong_weights)
                
                # Calculate impact (difference from base optimal)
                return_impact = true_return - self.base_return
                volatility_impact = true_volatility - self.base_volatility
                
                results.append({
                    'asset': asset_name,
                    'direction': direction,
                    'return_impact': return_impact,
                    'volatility_impact': volatility_impact
                })
        
        return pd.DataFrame(results)
    
    def analyze_volatility_sensitivity(self, percentage_change=0.01, risk_aversion=3.0,
                                      constraints=None, use_riskless=True):
        """
        Analyze impact of wrong volatility estimates
        """
        results = []
        
        for asset_idx in range(self.base_optimizer.n_assets):
            asset_name = self.base_optimizer.asset_names[asset_idx]
            
            for direction, multiplier in [('decrease', -1), ('increase', 1)]:
                wrong_vols = self.base_optimizer.volatilities.copy()
                wrong_vols[asset_idx] += multiplier * percentage_change
                
                wrong_optimizer = MeanVarianceOptimizer(
                    asset_names=self.base_optimizer.asset_names,
                    expected_returns=self.base_optimizer.expected_returns,
                    volatilities=wrong_vols,
                    correlation_matrix=self.base_optimizer.correlation_matrix,
                    risk_free_rate=self.base_optimizer.risk_free_rate
                )
                
                if use_riskless:
                    tangency = wrong_optimizer.find_tangency_portfolio(constraints)
                    if tangency:
                        wrong_optimal = wrong_optimizer.find_optimal_portfolio_with_riskfree(
                            tangency, risk_aversion
                        )
                    else:
                        continue
                else:
                    wrong_optimal = wrong_optimizer.find_optimal_portfolio_without_riskfree(
                        risk_aversion, constraints
                    )
                
                if wrong_optimal is None:
                    continue
                
                wrong_weights = wrong_optimal['weights']
                
                true_return = self.base_optimizer.portfolio_return(wrong_weights)
                true_volatility = self.base_optimizer.portfolio_volatility(wrong_weights)
                
                return_impact = true_return - self.base_return
                volatility_impact = true_volatility - self.base_volatility
                
                results.append({
                    'asset': asset_name,
                    'direction': direction,
                    'return_impact': return_impact,
                    'volatility_impact': volatility_impact
                })
        
        return pd.DataFrame(results)
