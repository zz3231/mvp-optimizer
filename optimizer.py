"""
Mean-Variance Portfolio Optimizer
Core optimization engine for Modern Portfolio Theory
"""

import numpy as np
from scipy.optimize import minimize


class MeanVarianceOptimizer:
    """
    Mean-Variance Portfolio Optimizer implementing Modern Portfolio Theory
    """
    
    def __init__(self, asset_names, expected_returns, volatilities, 
                 correlation_matrix, risk_free_rate=0.02):
        """
        Initialize optimizer
        
        Parameters:
        -----------
        asset_names : list of str
        expected_returns : array-like of float (decimal form)
        volatilities : array-like of float (decimal form)
        correlation_matrix : array-like, shape (n, n)
        risk_free_rate : float (decimal form)
        """
        self.asset_names = list(asset_names)
        self.n_assets = len(asset_names)
        self.expected_returns = np.array(expected_returns, dtype=float)
        self.volatilities = np.array(volatilities, dtype=float)
        self.correlation_matrix = np.array(correlation_matrix, dtype=float)
        self.risk_free_rate = float(risk_free_rate)
        
        self.covariance_matrix = self._calculate_covariance_matrix()
        self.excess_returns = self.expected_returns - risk_free_rate
        
    def _calculate_covariance_matrix(self):
        """Calculate covariance matrix from correlation and volatilities"""
        cov_matrix = np.zeros((self.n_assets, self.n_assets))
        for i in range(self.n_assets):
            for j in range(self.n_assets):
                cov_matrix[i, j] = (self.correlation_matrix[i, j] * 
                                   self.volatilities[i] * self.volatilities[j])
        return cov_matrix
    
    def portfolio_return(self, weights):
        """Calculate portfolio expected return"""
        return np.dot(weights, self.expected_returns)
    
    def portfolio_volatility(self, weights):
        """Calculate portfolio volatility"""
        variance = np.dot(weights, np.dot(self.covariance_matrix, weights))
        return np.sqrt(max(0, variance))
    
    def portfolio_sharpe_ratio(self, weights):
        """Calculate Sharpe ratio"""
        port_return = self.portfolio_return(weights)
        port_vol = self.portfolio_volatility(weights)
        if port_vol > 1e-8:
            return (port_return - self.risk_free_rate) / port_vol
        return 0.0
    
    def utility_function(self, weights, risk_aversion):
        """Utility: U = E[r] - 0.5 * A * sigma^2"""
        port_return = self.portfolio_return(weights)
        port_variance = np.dot(weights, np.dot(self.covariance_matrix, weights))
        return port_return - 0.5 * risk_aversion * port_variance
    
    def find_tangency_portfolio(self, constraints=None):
        """Find tangency portfolio (maximum Sharpe ratio)"""
        x0 = np.ones(self.n_assets) / self.n_assets
        
        if constraints is not None:
            lower = np.array(constraints['lower_bounds'])
            upper = np.array(constraints['upper_bounds'])
            # Handle infinite bounds
            lower = np.where(np.isinf(lower), -1e10, lower)
            upper = np.where(np.isinf(upper), 1e10, upper)
            bounds = tuple(zip(lower, upper))
        else:
            # Default: no short selling
            bounds = tuple((0, 1) for _ in range(self.n_assets))
        
        constraint_sum = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        objective = lambda x: -self.portfolio_sharpe_ratio(x)
        
        result = minimize(objective, x0, method='SLSQP',
                        bounds=bounds, constraints=[constraint_sum],
                        options={'maxiter': 1000, 'ftol': 1e-9})
        
        if result.success:
            weights = result.x
            return {
                'weights': weights,
                'weights_dict': dict(zip(self.asset_names, weights)),
                'expected_return': self.portfolio_return(weights),
                'volatility': self.portfolio_volatility(weights),
                'sharpe_ratio': self.portfolio_sharpe_ratio(weights),
                'success': True
            }
        return None
    
    def find_global_minimum_variance(self, constraints=None):
        """Find global minimum variance portfolio"""
        x0 = np.ones(self.n_assets) / self.n_assets
        
        if constraints is not None:
            lower = np.array(constraints['lower_bounds'])
            upper = np.array(constraints['upper_bounds'])
            # Handle infinite bounds
            lower = np.where(np.isinf(lower), -1e10, lower)
            upper = np.where(np.isinf(upper), 1e10, upper)
            bounds = tuple(zip(lower, upper))
        else:
            bounds = tuple((0, 1) for _ in range(self.n_assets))
        
        constraint_sum = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        objective = lambda x: self.portfolio_volatility(x)
        
        result = minimize(objective, x0, method='SLSQP',
                        bounds=bounds, constraints=[constraint_sum],
                        options={'maxiter': 1000, 'ftol': 1e-9})
        
        if result.success:
            weights = result.x
            return {
                'weights': weights,
                'weights_dict': dict(zip(self.asset_names, weights)),
                'expected_return': self.portfolio_return(weights),
                'volatility': self.portfolio_volatility(weights),
                'sharpe_ratio': self.portfolio_sharpe_ratio(weights),
                'success': True
            }
        return None
    
    def find_optimal_portfolio_with_riskfree(self, tangency_portfolio, risk_aversion):
        """
        Find optimal portfolio as combination of tangency and risk-free asset
        Formula: w* = (E[r_tangency] - r_f) / (A * sigma_tangency^2)
        """
        r_tangency = tangency_portfolio['expected_return']
        sigma_tangency = tangency_portfolio['volatility']
        
        # Weight on tangency portfolio
        w_tangency = (r_tangency - self.risk_free_rate) / (risk_aversion * sigma_tangency**2)
        w_riskfree = 1 - w_tangency
        
        # Weights on individual risky assets
        risky_weights = w_tangency * tangency_portfolio['weights']
        
        # Portfolio metrics
        port_return = w_riskfree * self.risk_free_rate + w_tangency * r_tangency
        port_vol = abs(w_tangency) * sigma_tangency
        port_sharpe = tangency_portfolio['sharpe_ratio']
        
        return {
            'weights': risky_weights,
            'weights_dict': dict(zip(self.asset_names, risky_weights)),
            'weight_tangency': w_tangency,
            'weight_riskfree': w_riskfree,
            'expected_return': port_return,
            'volatility': port_vol,
            'sharpe_ratio': port_sharpe,
            'success': True
        }
    
    def find_optimal_portfolio_without_riskfree(self, risk_aversion, constraints=None):
        """Find optimal portfolio by maximizing utility among risky assets"""
        x0 = np.ones(self.n_assets) / self.n_assets
        
        if constraints is not None:
            lower = np.array(constraints['lower_bounds'])
            upper = np.array(constraints['upper_bounds'])
            # Handle infinite bounds
            lower = np.where(np.isinf(lower), -1e10, lower)
            upper = np.where(np.isinf(upper), 1e10, upper)
            bounds = tuple(zip(lower, upper))
        else:
            bounds = tuple((0, 1) for _ in range(self.n_assets))
        
        constraint_sum = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        objective = lambda x: -self.utility_function(x, risk_aversion)
        
        result = minimize(objective, x0, method='SLSQP',
                        bounds=bounds, constraints=[constraint_sum],
                        options={'maxiter': 1000, 'ftol': 1e-9})
        
        if result.success:
            weights = result.x
            return {
                'weights': weights,
                'weights_dict': dict(zip(self.asset_names, weights)),
                'expected_return': self.portfolio_return(weights),
                'volatility': self.portfolio_volatility(weights),
                'sharpe_ratio': self.portfolio_sharpe_ratio(weights),
                'utility': self.utility_function(weights, risk_aversion),
                'success': True
            }
        return None
    
    def find_target_return_portfolio_with_riskfree(self, tangency_portfolio, target_return):
        """Find portfolio on CAL with target return"""
        r_tangency = tangency_portfolio['expected_return']
        sigma_tangency = tangency_portfolio['volatility']
        
        if target_return < self.risk_free_rate:
            target_return = self.risk_free_rate
        
        # Weight on tangency portfolio
        w_tangency = (target_return - self.risk_free_rate) / (r_tangency - self.risk_free_rate)
        w_riskfree = 1 - w_tangency
        
        # Weights on individual risky assets
        risky_weights = w_tangency * tangency_portfolio['weights']
        
        # Portfolio metrics
        port_vol = abs(w_tangency) * sigma_tangency
        port_sharpe = tangency_portfolio['sharpe_ratio']
        
        return {
            'weights': risky_weights,
            'weights_dict': dict(zip(self.asset_names, risky_weights)),
            'weight_tangency': w_tangency,
            'weight_riskfree': w_riskfree,
            'expected_return': target_return,
            'volatility': port_vol,
            'sharpe_ratio': port_sharpe,
            'success': True
        }
    
    def compute_efficient_frontier(self, n_points=50, constraints=None):
        """Compute efficient frontier"""
        # Extend range significantly beyond min/max asset returns
        min_return = np.min(self.expected_returns) * 0.5
        max_return = np.max(self.expected_returns) * 1.5
        target_returns = np.linspace(min_return, max_return, n_points)
        
        frontier_volatility = []
        frontier_returns = []
        
        for target in target_returns:
            x0 = np.ones(self.n_assets) / self.n_assets
            
            if constraints is not None:
                lower = np.array(constraints['lower_bounds'])
                upper = np.array(constraints['upper_bounds'])
                # Handle infinite bounds
                lower = np.where(np.isinf(lower), -1e10, lower)
                upper = np.where(np.isinf(upper), 1e10, upper)
                bounds = tuple(zip(lower, upper))
            else:
                bounds = tuple((0, 1) for _ in range(self.n_assets))
            
            constraint_sum = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
            constraint_return = {'type': 'eq', 'fun': lambda x: self.portfolio_return(x) - target}
            
            objective = lambda x: self.portfolio_volatility(x)
            
            result = minimize(objective, x0, method='SLSQP',
                            bounds=bounds, 
                            constraints=[constraint_sum, constraint_return],
                            options={'maxiter': 1000, 'ftol': 1e-9})
            
            if result.success:
                weights = result.x
                frontier_returns.append(self.portfolio_return(weights))
                frontier_volatility.append(self.portfolio_volatility(weights))
        
        return {
            'returns': np.array(frontier_returns),
            'volatilities': np.array(frontier_volatility)
        }
