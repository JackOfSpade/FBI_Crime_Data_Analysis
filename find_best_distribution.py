import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import os
import os.path as path

# Find best-fit distribution to data
# Note:
# bin_heights is the height of the bins
# bin_centers is the bin centers of the histogram
def best_fit_distribution(file_name, data, bin_heights, bin_centers):
    # Distributions to check
    distributions = [
        st.alpha, st.anglit, st.arcsine, st.argus, st.beta, st.betaprime, st.bradford, st.burr, st.burr12, st.cauchy,
        st.chi, st.chi2, st.cosine, st.crystalball, st.dgamma, st.dweibull, st.erlang, st.expon, st.exponnorm,
        st.exponweib, st.exponpow, st.f, st.fatiguelife, st.fisk, st.foldcauchy, st.foldnorm, st.frechet_r,
        st.frechet_l, st.genlogistic, st.gennorm, st.genpareto, st.genexpon, st.genextreme, st.gausshyper, st.gamma,
        st.gengamma, st.genhalflogistic, st.geninvgauss, st.gilbrat, st.gompertz, st.gumbel_r, st.gumbel_l,
        st.halfcauchy, st.halflogistic, st.halfnorm, st.halfgennorm, st.hypsecant, st.invgamma, st.invgauss,
        st.invweibull, st.johnsonsb, st.johnsonsu, st.kappa4, st.kappa3, st.kstwobign, st.laplace, st.levy,
        st.levy_l, st.logistic, st.loggamma, st.loglaplace, st.lognorm, st.loguniform, st.lomax,
        st.maxwell, st.mielke, st.moyal, st.nakagami, st.norm, st.norminvgauss, st.pareto,
        st.pearson3, st.powerlaw, st.powerlognorm, st.powernorm, st.rdist, st.rayleigh, st.rice, st.recipinvgauss,
        st.semicircular, st.skewnorm, st.t, st.trapz, st.triang, st.truncexpon, st.truncnorm, st.uniform, st.vonmises, st.vonmises_line, st.wald, st.weibull_min, st.weibull_max, st.wrapcauchy
    ]

    # st.levy_stable, st.ncf, st.nct, st.ncx2, st.tukeylambda, st.ksone

    if path.exists(path=file_name + ".npy"):
        saved_distribution = np.load(file=file_name + ".npy", allow_pickle=True)
        best_distribution = saved_distribution[0]
        best_parameters = saved_distribution[1]
        best_residual_sum_of_squares = saved_distribution[2]
        # Temporary
        try:
            progress_index = saved_distribution[3]
        except:
            progress_index = len(distributions) - 1
    else:
        best_distribution = None
        best_parameters = None
        best_residual_sum_of_squares = np.inf
        progress_index = 0

    distributions = distributions[progress_index:]




    # Estimate distribution parameters from data
    for distribution in distributions:
        print(distribution.name)
        # Try to fit the distribution, skip if error occurs (data cannot be fit)
        try:
            # Ignore warnings
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit distribution to data
                parameters = distribution.fit(data)

                # Separate the parameters
                shape_parameters = parameters[:-2]
                location_parameter = parameters[-2]
                scale_parameter = parameters[-1]

                # Calculate fitted PDF and error with fit in distribution
                predicted_height = distribution.pdf(bin_centers, shape_parameters, loc=location_parameter, scale=scale_parameter)
                residual_sum_of_squares = np.sum(np.power(bin_heights - predicted_height, 2.0))

                # identify if this distribution is better
                if best_residual_sum_of_squares > residual_sum_of_squares:
                    best_distribution = distribution
                    best_parameters = (shape_parameters, location_parameter, scale_parameter)
                    best_residual_sum_of_squares = residual_sum_of_squares
        except Exception:
            pass

        progress_index += 1

        # Save after every distribution type fit
        with open(file=file_name + ".npy", mode="w") as file_out:
            file_out.write("")

        np.save(file=file_name + ".npy",
                arr=np.array(object=[best_distribution, best_parameters, best_residual_sum_of_squares, progress_index]))



    return (best_distribution, best_parameters, best_residual_sum_of_squares)
