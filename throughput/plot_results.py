import numpy as np
import matplotlib.pyplot as plt
import utils

def get_stats(filename):
    vehicles = []
    utils.read_tripinfo_file(filename, vehicles)

    flows = {}

    for v in vehicles:
        f = v.label.split('.')[0]
        if '-' in f:
            f = f.split('-')[0]

        if f not in flows:
            flows[f] = {
                'count': 0
            }

        flows[f]['count'] += 1
        flows[f]['trips'].append({
            'depart': v.depart,
            'arrival': v.arrival,
            'traveltime': v.traveltime,
            'waittime': v.waittime
        })

    return flows

def plot_results(results, experiments_count):
    FLOW_COUNT = 2
    FLOW_NAME = "flow_{}"
    COLORS = ["cornflowerblue", "wheat"]

    FLOW_NAMES = ['ул. Брестская', 'ул. Героев Севастополя']

    BAR_WIDTH = 0.6

    flows_legend = [{}] * FLOW_COUNT

    bars = [0, 1, 2, 3]

    variant_i = 1
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
        total_value = cumulative_bottom_pos[FLOW_COUNT - 1]
        plt.text(bars[variant_i] - 0.1, total_value - 80, str(int(total_value)))
        variant_i += 1

    x_labels = ['', 'Существующее\nположение', 'Предложение', '']
    plt.xticks(bars, x_labels)
    plt.ylabel('Пропускная способность перекрестка, авт./час')
    plt.legend(tuple(flows_legend), FLOW_NAMES)
    plt.show()
