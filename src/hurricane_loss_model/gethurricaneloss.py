import argparse
import logging

from typing import Dict, Optional, Tuple
from .meanloss import estimate_mean_loss, SIMULATORS

def parse_args() -> Dict:
    """
    Parse Arguments.
    Parameters:
    Returns:
    - args: Dictionary of arguments
    """
    parser = argparse.ArgumentParser(
        description="Calculates the average annual hurricane loss in $Billions",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "florida_landfall_rate",
        type=float,
        help="Annual rate of landfalling hurricanes in Florida"
    )
    parser.add_argument(
        "florida_mean",
        type=float,
        help="Mean (LogNormal) of lognormal distribution for Florida losses"
    )
    parser.add_argument(
        "florida_stddev",
        type=float,
        help="Stddev (LogNormal) of lognormal distribution for Florida losses"
    )
    parser.add_argument(
        "gulf_landfall_rate",
        type=float,
        help="Annual rate of landfalling hurricanes in Gulf states"
    )
    parser.add_argument(
        "gulf_mean",
        type=float,
        help="Mean (LogNormal) of lognormal distribution for Gulf losses"
    )
    parser.add_argument(
        "gulf_stddev",
        type=float,
        help="Stddev (LogNormal) of lognormal distribution for Gulf losses"
    )
    ### Options
    parser.add_argument(
        "-n", "--num_monte_carlo_samples",
        type=int,
        default=100,
        help="Number of Monte Carlo simulation samples (years) to run"
    )
    parser.add_argument(
        "-s", "--simulator",
        type=str,
        default="default",
        help=f"Which Monte Carlo simulator should be run from below:\n\
            {"\n".join([" - " + k + ": " + v[1] for k, v in SIMULATORS.items()])}\n"
    )
    parser.add_argument(
        "-t", "--timer",
        action="store_true",
        help="Output the execution time"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Increase Verbosity"
    )
    return vars(parser.parse_args())


def check_args(args: Dict) -> Tuple[bool, Optional[Dict]]:
    """
    Check Arguments for validity
    Parameters:
    - args: Arguments from parse_args as a Dict
    Returns:
    - isvalid: boolean for if arguments are valid
    - args: returns same args if valid
    """
    if args["verbose"]:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")

    argstocheck = [
        "florida_landfall_rate",
        "florida_mean",
        "florida_stddev",
        "gulf_landfall_rate",
        "gulf_mean",
        "gulf_stddev",
        "num_monte_carlo_samples"
    ]
    isvalid = True
    for argname in argstocheck:
        if args[argname] <= 0:
            logging.error(f"{argname} should be >= 0. {args[argname]} < 0")
            isvalid = False
    if not isvalid:
        return isvalid, None
    
    logging.info("===== Parameters =====")
    logging.info(f"Florida Rate: {args["florida_landfall_rate"]}")
    logging.info(f"Florida Mean: {args["florida_mean"]}")
    logging.info(f"Florida Standard Deviation: {args["florida_stddev"]}")
    logging.info(f"Gulf states Rate: {args["gulf_landfall_rate"]}")
    logging.info(f"Gulf states Mean: {args["gulf_mean"]}")
    logging.info(f"Gulf states Standard Deviation: {args["gulf_stddev"]}")
    logging.info(f"Number of Monte Carlo samples: {args["num_monte_carlo_samples"]}")
    logging.info("===== End Parameters =====")

    return isvalid, args


def get_hurricane_loss():
    # Command-line argument parsing
    args = parse_args()
    isvalid, args = check_args(args)

    if not isvalid:
        raise ValueError("Program stopped, Invalid arguments")

    # Run the simulation
    if args["timer"]:
        mean_loss, time = estimate_mean_loss(
            args["florida_landfall_rate"],
            args["florida_mean"],
            args["florida_stddev"],
            args["gulf_landfall_rate"],
            args["gulf_mean"],
            args["gulf_stddev"],
            args["num_monte_carlo_samples"],
            args["simulator"],
            True
        )
        print(f"Finished Simulation, execution time: {time:.4f} seconds")
    else:
        mean_loss = estimate_mean_loss(
            args["florida_landfall_rate"],
            args["florida_mean"],
            args["florida_stddev"],
            args["gulf_landfall_rate"],
            args["gulf_mean"],
            args["gulf_stddev"],
            args["num_monte_carlo_samples"],
            args["simulator"]
        )

    print(f"Estimated Average Annual Loss: ${mean_loss:.2f} Billion")

if __name__ == "__main__":
    get_hurricane_loss()