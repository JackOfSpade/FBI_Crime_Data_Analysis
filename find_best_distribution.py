import warnings
import numpy as np
import pandas as pd
import scipy.stats as st

# Find best-fit distribution to data
def best_fit_distribution(data, bins=200, ax=None):
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)

    # Get center of each bin --------------------------------
    x = (x + np.roll(x, -1))[:-1] / 2.0

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

    # Best holders
    best_distribution = None
    best_params = None
    best_residual_sum_of_squares = None

    # Estimate distribution parameters from data
    for distribution in distributions:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                residual_sum_of_squares = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                except Exception:
                    pass

                # identify if this distribution is better
                if best_residual_sum_of_squares > residual_sum_of_squares > 0:
                    best_distribution = distribution
                    best_params = params
                    best_residual_sum_of_squares = residual_sum_of_squares

        except Exception:
            pass

    return (best_distribution.name, best_params)


