import matplotlib.pyplot as plt
from hurricane_loss_model.meanloss import SIMULATORS

def benchmark():
    florida_landfall_rate = 1.5
    florida_mean = 2.0
    florida_stddev = 0.5
    gulf_landfall_rate = 1.2
    gulf_mean = 1.8
    gulf_stddev = 0.6
    
    results = {k: [] for k in SIMULATORS}

    for simulator, (func, desc) in SIMULATORS.items():
        print(f"Running simulator {simulator}")
        for n in range(1, 8):
            num_samples = 10 ** n
            print(f" - Sample size {num_samples}")
            res, time = func(
                florida_landfall_rate, florida_mean, florida_stddev,
                gulf_landfall_rate, gulf_mean, gulf_stddev, num_samples
            )
            results[simulator].append([num_samples, res, time * 1000])

    fig, axs = plt.subplots(2, 1, figsize=(10, 12))

    for simulator_name, data in results.items():
        num_samples = [item[0] for item in data]
        results = [item[1] for item in data]
        runtimes = [item[2] for item in data]
        axs[0].plot(num_samples, runtimes, marker="o", label=simulator_name)
        axs[1].plot(num_samples, results, marker="o", label=simulator_name)

    axs[0].set_xlabel("Number of Samples")
    axs[0].set_xlabel("Runtime (milliseconds)")
    axs[0].set_title("Runtime vs Number of Samples for Different Simulators")
    axs[0].set_xscale("log")
    axs[0].set_yscale("log")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].set_xlabel("Number of Samples")
    axs[1].set_xlabel("Loss in $Billions")
    axs[1].set_title("Loss in $Billions vs Number of Samples for Different Simulators")
    axs[1].set_xscale("log")
    axs[1].legend()
    axs[1].grid(True)

    plt.savefig("benchmark.png", format="png")
    

if __name__ == "__main__":
    benchmark()