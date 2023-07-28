import numpy as np
import matplotlib.pyplot as plt
import sys
import json

def plot_results(results, experiments_count):
    FLOW_COUNT = 2
    FLOW_NAME = "flow_{}"
    COLORS = ["cornflowerblue", "wheat", "limegreen", "tomato", "violet", "khaki"]

    FLOW_NAMES = ['ул. Брестская', 'ул. Героев Севастополя']

    BAR_WIDTH = 0.3

    flows_legend = [{}] * FLOW_COUNT

    fig, ax = plt.subplots()

    bars = range(len(results))

    variant_i = 0
    for variant_name in results:
        data_by_flows = [[] for i in range(len(results))]
        flows_sum = {}
        for experiment in results[variant_name]:
            for flow in experiment:
                if flow == 'total':
                    continue
                if flow in flows_sum:
                    flows_sum[flow] += experiment[flow]['count']
                else:
                    flows_sum[flow] = experiment[flow]['count']
        for flow_number in range(FLOW_COUNT):
            data_by_flows[flow_number] = flows_sum[FLOW_NAME.format(flow_number)] / experiments_count

        cumulative_bottom_pos = [0] * FLOW_COUNT

        for flow_number in range(FLOW_COUNT):
            p = plt.bar(bars[variant_i], data_by_flows[flow_number], BAR_WIDTH, bottom=cumulative_bottom_pos, color=COLORS[flow_number], edgecolor="black")
            flows_legend[flow_number] = p
            for i in range(FLOW_COUNT):
                cumulative_bottom_pos[i] += data_by_flows[flow_number]
        variant_i += 1

    x_labels = ['Существующее положение', 'Предложение']
    plt.xticks(bars, x_labels)
    plt.legend(tuple(flows_legend), FLOW_NAMES)
    plt.show()


experiments_count = int(sys.argv[1])
variants = sys.argv[2:]

results = {}
for variant in variants:
    with open(variant + '.json', 'r') as variant_results:
        results[variant] = json.loads(variant_results.read())

plot_results(results, experiments_count)
