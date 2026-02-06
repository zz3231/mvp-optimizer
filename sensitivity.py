"""
Sensitivity Analysis Module
Analyze impact of parameter misestimation on portfolio performance
"""

import numpy as np
import pandas as pd


class SensitivityAnalyzer:
    """
    Sensitivity Analysis: Use FIXED optimal weights, vary parameters
    
    Key concept: What happens to my portfolio if market parameters 
    differ from my estimates, but I'm stuck with weights optimized 
    using the wrong estimates?
    """
    
    def __init__(self, base_optimizer, optimal_weights):
        """
        Parameters:
        -----------
        base_optimizer : MeanVarianceOptimizer
            Optimizer with user's estimated parameters
        optimal_weights : array
            Optimal portfolio weights (these stay FIXED)
        """
        self.base_optimizer = base_optimizer
        self.optimal_weights = optimal_weights
        
        # Base portfolio metrics using user's estimated parameters
        self.base_return = base_optimizer.portfolio_return(optimal_weights)
        self.base_volatility = base_optimizer.portfolio_volatility(optimal_weights)
    
    def analyze_return_sensitivity(self, percentage_change=0.01):
        """
        Analyze impact if true expected returns differ from estimates
        
        Logic:
        1. Use FIXED optimal weights (don't re-optimize!)
        2. Change true market return by +/- percentage_change
        3. Calculate portfolio performance with these changed returns
        4. Compare to base case
        """
        results = []
        
        for asset_idx in range(self.base_optimizer.n_assets):
            asset_name = self.base_optimizer.asset_names[asset_idx]
            
            for direction, multiplier in [('decrease', -1), ('increase', 1)]:
                # Market reality: returns differ from estimates
                true_returns = self.base_optimizer.expected_returns.copy()
                true_returns[asset_idx] += multiplier * percentage_change
                
                # Calculate portfolio performance with FIXED weights
                # but different market returns
                portfolio_return = np.dot(self.optimal_weights, true_returns)
                
                # Volatility doesn't change (only depends on vols and correlations)
                portfolio_volatility = self.base_volatility
                
                # Calculate impact
                return_impact = portfolio_return - self.base_return
                volatility_impact = 0.0  # No change in this case
                
                results.append({
                    'asset': asset_name,
                    'direction': direction,
                    'return_impact': return_impact,
                    'volatility_impact': volatility_impact
                })
        
        return pd.DataFrame(results)
    
    def analyze_volatility_sensitivity(self, percentage_change=0.01):
        """
        Analyze impact if true volatilities differ from estimates
        
        Logic:
        1. Use FIXED optimal weights
        2. Change true market volatility by +/- percentage_change
        3. Recalculate covariance matrix with new volatility
        4. Calculate portfolio volatility with fixed weights
        5. Compare to base case
        """
        results = []
        
        for asset_idx in range(self.base_optimizer.n_assets):
            asset_name = self.base_optimizer.asset_names[asset_idx]
            
            for direction, multiplier in [('decrease', -1), ('increase', 1)]:
                # Market reality: volatilities differ from estimates
                true_vols = self.base_optimizer.volatilities.copy()
                true_vols[asset_idx] += multiplier * percentage_change
                
                # Recalculate covariance matrix with new volatility
                true_cov = np.zeros((self.base_optimizer.n_assets, 
                                    self.base_optimizer.n_assets))
                for i in range(self.base_optimizer.n_assets):
                    for j in range(self.base_optimizer.n_assets):
                        true_cov[i, j] = (self.base_optimizer.correlation_matrix[i, j] * 
                                         true_vols[i] * true_vols[j])
                
                # Calculate portfolio performance with FIXED weights
                # Expected return doesn't change (only depends on returns)
                portfolio_return = self.base_return
                
                # Volatility DOES change
                portfolio_variance = np.dot(self.optimal_weights, 
                                           np.dot(true_cov, self.optimal_weights))
                portfolio_volatility = np.sqrt(max(0, portfolio_variance))
                
                # Calculate impact
                return_impact = 0.0  # No change in this case
                volatility_impact = portfolio_volatility - self.base_volatility
                
                results.append({
                    'asset': asset_name,
                    'direction': direction,
                    'return_impact': return_impact,
                    'volatility_impact': volatility_impact
                })
        
        return pd.DataFrame(results)
