import logging
import numpy as np


def estimate_mean_loss(florida_landfall_rate, florida_mean, florida_stddev,
                              gulf_landfall_rate, gulf_mean, gulf_stddev, num_samples):
    """
    Simulate the average annual hurricane losses using Monte Carlo method.
    Parameters:
    - florida_landfall_rate: Poisson rate for Florida hurricane landfall
    - florida_mean: Mean of lognormal distribution for Florida hurricane losses
    - florida_stddev: Standard deviation of lognormal distribution for Florida hurricane losses
    - gulf_landfall_rate: Poisson rate for Gulf states hurricane landfall
    - gulf_mean: Mean of lognormal distribution for Gulf states hurricane losses
    - gulf_stddev: Standar deviation of lognormal distribution for Gulf states hurricane losses
    - num_samples: Number of Monte Carlo simulation samples (years)
    Returns:
    - mean_loss: Estimated average annual economic loss in billions
    """
    total_loss = 0
    for year in range(num_samples):
        # Simulate Florida Events
        florida_events = np.random.poisson(lam=florida_landfall_rate, size=1)[0]
        florida_loss = 0
        for _ in range(florida_events):
            florida_loss += np.random.lognormal(florida_mean, florida_stddev)
        # Simulate Gulf state Events
        gulf_events = np.random.poisson(lam=gulf_landfall_rate, size=1)[0]
        gulf_loss = 0
        for k in range(gulf_events):
            gulf_loss += np.random.lognormal(gulf_mean, gulf_stddev)
        # Accumulate
        total_loss += florida_loss + gulf_loss
        logging.info(f"Year: {year} - Florida Loss: {florida_loss} - Gulf Loss: {gulf_loss}")
    logging.info(f"Total loss over {year} years: {total_loss}")
    logging.info(f"Total loss per year: {total_loss / num_samples}")
    return total_loss / num_samples