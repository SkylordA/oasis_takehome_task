import logging
import numpy as np
from numba import njit

from .utils import timer


@timer
def _estimate_mean_loss_default(
        florida_landfall_rate: float,
        florida_mean: float,
        florida_stddev: float,
        gulf_landfall_rate: float,
        gulf_mean: float,
        gulf_stddev: float,
        num_samples: int,
    ) -> float:
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
    logging.info(f"Total loss over {num_samples} years: {total_loss}")
    return total_loss / num_samples

@timer
def _estimate_mean_loss_loopless(
        florida_landfall_rate: float,
        florida_mean: float,
        florida_stddev: float,
        gulf_landfall_rate: float,
        gulf_mean: float,
        gulf_stddev: float,
        num_samples: int,
    ) -> float:
    # Simulate all events
    florida_events = np.random.poisson(lam=florida_landfall_rate, size=num_samples)
    gulf_events = np.random.poisson(lam=gulf_landfall_rate, size=num_samples)
    num_fl_events = np.sum(florida_events)
    num_gs_events = np.sum(gulf_events)
    # Simulate all losses
    florida_loss = np.random.lognormal(florida_mean, florida_stddev, size=(num_fl_events,))
    gulf_loss = np.random.lognormal(gulf_mean, gulf_stddev, size=(num_gs_events,))
    # Accumulate
    florida_loss = np.sum(florida_loss)
    gulf_loss = np.sum(gulf_loss)
    total_loss = florida_loss + gulf_loss
    logging.info(f"Total Florida loss over {num_samples} years: {florida_loss}")
    logging.info(f"Total Gulf loss over {num_samples} years: {gulf_loss}")
    logging.info(f"Total loss over {num_samples} years: {total_loss}")
    return total_loss / num_samples


@timer
@njit(parallel=True, fastmath=True)
def _estimate_mean_loss_numba(
        florida_landfall_rate: float,
        florida_mean: float,
        florida_stddev: float,
        gulf_landfall_rate: float,
        gulf_mean: float,
        gulf_stddev: float,
        num_samples: int,
    ) -> float:
    # Simulate all events
    florida_events = np.random.poisson(lam=florida_landfall_rate, size=num_samples)
    gulf_events = np.random.poisson(lam=gulf_landfall_rate, size=num_samples)
    num_fl_events = np.sum(florida_events)
    num_gs_events = np.sum(gulf_events)
    # Simulate all losses
    florida_loss = np.random.lognormal(florida_mean, florida_stddev, size=(num_fl_events,))
    gulf_loss = np.random.lognormal(gulf_mean, gulf_stddev, size=(num_gs_events,))
    # Accumulate
    florida_loss = np.sum(florida_loss)
    gulf_loss = np.sum(gulf_loss)
    total_loss = florida_loss + gulf_loss
    return total_loss / num_samples