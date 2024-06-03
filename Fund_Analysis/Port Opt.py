returns = df_target[['return','port_1_return','port_2_return']]
annualized_vol = returns.std()*np.sqrt(12)
annualized_vol.plot.bar()

##port opt
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage


portfolio = df_target[['close','port_1_close','port_2_close','port_3_close','port_4_close','port_5_close']]
print (portfolio)
mu = mean_historical_return(portfolio)
S = CovarianceShrinkage(portfolio).ledoit_wolf()
from pypfopt.efficient_frontier import EfficientFrontier
print (mu)
print (S)
ef = EfficientFrontier(mu, S)
weights = ef.max_quadratic_utility()

cleaned_weights = ef.clean_weights()
print(dict(cleaned_weights))
ef.portfolio_performance(verbose=True)

from pypfopt import HRPOpt
returns = portfolio.pct_change().dropna()
hrp = HRPOpt(returns)
hrp_weights = hrp.optimize()
hrp.portfolio_performance(verbose=True)
print(dict(hrp_weights))
from pypfopt.efficient_frontier import EfficientCVaR
S = portfolio.cov()
ef_cvar = EfficientCVaR(mu, S)
cvar_weights = ef_cvar.min_cvar()

cleaned_weights = ef_cvar.clean_weights()
print(dict(cleaned_weights))

