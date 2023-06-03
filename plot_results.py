import numpy as np
import matplotlib.pyplot as plt
import sys
import json

FLOW_COUNT = 6
FLOW_NAME = "flow_{}"

CAR_FLOWS = ["flow_0", "flow_1", "flow_2", "flow_3"]  #, "flow_4", "flow_5"
PT_FLOWS = {
    "pt_1": {
        "flows": ["flow_01"],
        "style": {
            "label": "pt_1",
            "c": "y",
        }
    },
    "pt_2": {
        "flows": ["flow_02"],
        "style": {
            "label": "pt_2",
            "c": "y",
        }
    },
    "pt_3": {
        "flows": ["flow_11", "flow_12", "flow_13"],
        "style": {
            "label": "pt_3",
            "c": "blue",
        }
    },
    "pt_4":{
        "flows": ["flow_31", "flow_32", "flow_33"],
        "style": {
            "label": "pt_4",
            "c": "green",
        }
    }
}

COLORS = {
    "flow_1": "blue",
    "flow_2": "orange",
    "flow_3": "green",
    "flow_4": "red",
    "flow_5": "purple",
    "flow_0": "y",
}
COLOR_ALPHA = {
    "current": 0.35,
    "proposed": 0.5
}
LINESTYLES = {
    "current": "dashed",
    #   {
    #     "flow_1": ["blue", "dashed"],
    #     "flow_2": ["orange", "dashed"],
    #     "flow_3": ["green", "dashed"],
    #     "flow_4": ["red", "dashed"],
    #     "flow_5": ["purple", "dashed"],
    #     "flow_0": ["y", "dashed"]
    # },
    "proposed": "solid"
}

MARKERSTYLE = {
    "current": "o",
    "proposed": "x"
}

def do_plot(ax, data):
    ax.scatter(
        data['x'],
        data['y'],
        label=data['label'],
        c=data['c'],
        marker=data['marker'],
        alpha=data['alpha'])

def process_data(data):
    x = []
    y = []
    data.sort(key=lambda x: x['arrival'])
    for d in data:
        x.append(d['arrival'])
        y.append(d['traveltime'])
    
    return  {
            'x': x,
            'y': y
        }

def plot_results(results, experiments_count):

    flows_legend = [{}] * FLOW_COUNT

    fig, ax = plt.subplots(2, 1)

    metric = 'traveltime'

    plots_data1 = []
    plots_data2 = []

    for model_type in results:
        result = results[model_type][0]

        # for flow_name in result:
        for flow_name in CAR_FLOWS:
            processed = process_data(result[flow_name]['trips'])
            style = {
                'label': "{}_{}".format(model_type, flow_name),
                'c': COLORS[flow_name],
                'marker': MARKERSTYLE[model_type],
                'alpha': COLOR_ALPHA[model_type]
            }
            plots_data1.append(processed | style)

        for pt_flow in PT_FLOWS:
            data = []
            for flow_name in PT_FLOWS[pt_flow]["flows"]:
                data += result[flow_name]['trips']
            plots_data2.append(
                process_data(data) 
                | PT_FLOWS[pt_flow]['style'] 
                | { "marker": MARKERSTYLE[model_type], "alpha": COLOR_ALPHA[model_type]})


        # polynom = np.poly1d(np.polyfit(range(len(data)), data, deg=10))
        # new_x = np.linspace(0, len(data))
        # plt.plot(new_x, polynom(new_x), label=flow_name, linewidth=2, color=COLORS[flow_name], linestyle=LINESTYLES[model_type])

    for plot_data in plots_data1:
        do_plot(ax[0], plot_data)
    
    for plot_data in plots_data2:
        do_plot(ax[1], plot_data)

    plt.legend()
    plt.show()


experiments_count = int(sys.argv[1])
variants = sys.argv[2:]

results = {}
for variant in variants:
    with open(variant + '.json', 'r') as variant_results:
        results[variant] = json.loads(variant_results.read())

plot_results(results, experiments_count)
