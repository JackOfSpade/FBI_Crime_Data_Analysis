import warnings
import numpy as np
import pandas as pd
import scipy.stats as st

# Find best-fit distribution to data
# Note: x is the bin-edge centers of histogram
def best_fit_distribution(data, y, x, bins=200, ax=None):
    # Distributions to check
    distributions = [
        st.alpha, st.anglit, st.arcsine, st.argus, st.beta, st.betaprime, st.bradford, st.burr, st.burr12, st.cauchy,
        st.chi, st.chi2, st.cosine, st.crystalball, st.dgamma, st.dweibull, st.erlang, st.expon, st.exponnorm,
        st.exponweib, st.exponpow, st.f, st.fatiguelife, st.fisk, st.foldcauchy, st.foldnorm, st.frechet_r,
        st.frechet_l, st.genlogistic, st.gennorm, st.genpareto, st.genexpon, st.genextreme, st.gausshyper, st.gamma,
        st.gengamma, st.genhalflogistic, st.geninvgauss, st.gilbrat, st.gompertz, st.gumbel_r, st.gumbel_l,
        st.halfcauchy, st.halflogistic, st.halfnorm, st.halfgennorm, st.hypsecant, st.invgamma, st.invgauss,
        st.invweibull, st.johnsonsb, st.johnsonsu, st.kappa4, st.kappa3, st.ksone, st.kstwobign, st.laplace, st.levy,
        st.levy_l, st.levy_stable, st.logistic, st.loggamma, st.loglaplace, st.lognorm, st.loguniform, st.lomax,
        st.maxwell, st.mielke, st.moyal, st.nakagami, st.ncx2, st.ncf, st.nct, st.norm, st.norminvgauss, st.pareto,
        st.pearson3, st.powerlaw, st.powerlognorm, st.powernorm, st.rdist, st.rayleigh, st.rice, st.recipinvgauss,
        st.semicircular, st.skewnorm, st.t, st.trapz, st.triang, st.truncexpon, st.truncnorm, st.tukeylambda,
        st.uniform, st.vonmises, st.vonmises_line, st.wald, st.weibull_min, st.weibull_max, st.wrapcauchy
    ]

    best_distribution = None
    best_parameters = None
    best_residual_sum_of_squares = np.inf

    # Estimate distribution parameters from data
    for distribution in distributions:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            # with warnings.catch_warnings():
            #     warnings.filterwarnings('ignore')

            # fit distribution to data
            parameters = distribution.fit(data)

            # Separate the parameters
            shape_parameters = parameters[:-2]
            location_parameter = parameters[-2]
            scale_parameter = parameters[-1]

            # Calculate fitted PDF and error with fit in distribution
            predicted_probability = distribution.pdf(x, shape_parameters, loc=location_parameter, scale=scale_parameter)
            residual_sum_of_squares = np.sum(np.power(y - predicted_probability, 2.0))

            # identify if this distribution is better
            if best_residual_sum_of_squares > residual_sum_of_squares:
                best_distribution = distribution
                best_parameters = (shape_parameters, location_parameter, scale_parameter)
                best_residual_sum_of_squares = residual_sum_of_squares

        except Exception:
            pass

    return (best_distribution, best_parameters, best_residual_sum_of_squares)

# best_distribution.name
