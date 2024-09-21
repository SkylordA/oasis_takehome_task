import logging
import numpy as np

from typing import Tuple, Union
from .simulators import _estimate_mean_loss_default, _estimate_mean_loss_loopless

SIMULATORS = {
    "default": (
        _estimate_mean_loss_default,
        "Basic monte carlo simulation using for loops"
    ),
    "loopless": (
        _estimate_mean_loss_loopless,
        "Monte Carlo simulation without any loops",
    )
}


def estimate_mean_loss(
        florida_landfall_rate: float,
        florida_mean: float,
        florida_stddev: float,
        gulf_landfall_rate: float,
        gulf_mean: float,
        gulf_stddev: float,
        num_samples: int,
        simulator: str,
        debug: bool=False
    ) -> Union[float, Tuple[float, float]]:
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
    - simulator: Specifies which simulator is run from above SIMULATORS
    Returns:
    - mean_loss: Estimated average annual economic loss in billions
    """
    if simulator not in SIMULATORS.keys():
        logging.warning(
            f"Simulator \"{simulator}\" is not a valid simulator, switching to \"default\"\n. See --help for more info"
        )
        simulator = "default"
    logging.info(f"Simulator {simulator} selected.")
    mean_loss, time =  SIMULATORS[simulator][0](
        florida_landfall_rate, florida_mean, florida_stddev,
        gulf_landfall_rate, gulf_mean, gulf_stddev, num_samples
    )
    if debug:
        logging.info(f"End of simulation, time taken: {time:.4f} seconds.")
        return mean_loss, time
    return mean_loss

