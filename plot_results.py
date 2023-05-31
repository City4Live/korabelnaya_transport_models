import numpy as np
import matplotlib.pyplot as plt
import sys
import json

def plot_results(results, experiments_count):
    FLOW_COUNT = 6
    FLOW_NAME = "flow_{}"
    COLORS = {
        "flow_1": "blue",
        "flow_2": "orange",
        "flow_3": "green",
        "flow_4": "red",
        "flow_5": "purple",
        "flow_0": "y"
    }
    LINESTYLES = {
        "current": "dashed",
        "proposed": "solid"
    }

    FLOW_NAMES = ['ФШ прав.', 'Вакуленчука', 'Вакуленчука лев.', 'ПОР прав.', 'ФШ лев.', 'ПОР']

    BAR_WIDTH = 0.25

    flows_legend = [{}] * FLOW_COUNT

    fig, ax = plt.subplots()

    metric = 'traveltime'

    for model_type in results:
        result = results[model_type][0]

        for flow_name in result:
            data = result[flow_name][metric]

            polynom = np.poly1d(np.polyfit(range(len(data)), data, deg=3))
            # ax_pos = 6 + norm_i
            new_x = np.linspace(0, len(data))
            plt.plot(new_x, polynom(new_x), label=flow_name, linewidth=2, color=COLORS[flow_name], linestyle=LINESTYLES[model_type])

    plt.legend()
    plt.show()


experiments_count = int(sys.argv[1])
variants = sys.argv[2:]

results = {}
for variant in variants:
    with open(variant + '.json', 'r') as variant_results:
        results[variant] = json.loads(variant_results.read())

plot_results(results, experiments_count)
