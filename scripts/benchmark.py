import matplotlib.pyplot as plt
from hurricane_loss_model.meanloss import SIMULATORS
from hurricane_loss_model.simulators import _estimate_mean_loss_default, _estimate_mean_loss_loopless

def benchmark():
    florida_landfall_rate = 1.5
    florida_mean = 2.0
    florida_stddev = 0.5
    gulf_landfall_rate = 1.2
    gulf_mean = 1.8
    gulf_stddev = 0.6
    
    runtimes = {k: [] for k in SIMULATORS}

    for simulator, (func, desc) in SIMULATORS.items():
        print(f"Running simulator {simulator}")
        for n in range(1, 7):
            num_samples = 10 ** n
            print(f" - Sample size {num_samples}")
            res, time = func(
                florida_landfall_rate, florida_mean, florida_stddev,
                gulf_landfall_rate, gulf_mean, gulf_stddev, num_samples
            )
            runtimes[simulator].append([num_samples, time * 1000])

    plt.figure(figsize=(10, 6))

    for simulator_name, data in runtimes.items():
        num_samples = [item[0] for item in data]
        runtimes = [item[1] for item in data]
        plt.plot(num_samples, runtimes, marker="o", label=simulator_name)

    plt.xlabel("Number of Samples")
    plt.ylabel("Runtime (milliseconds)")
    plt.title("Runtime vs Number of Samples for Different Simulators")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.grid(True)

    plt.savefig("benchmark.png", format="png")
    

if __name__ == "__main__":
    benchmark()