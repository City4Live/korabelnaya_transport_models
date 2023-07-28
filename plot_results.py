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
            "c": "y",
        }
    },
    "pt_2": {
        "flows": ["flow_02"],
        "style": {
            "c": "y",
        }
    },
    "pt_3": {
        "flows": ["flow_11", "flow_12", "flow_13"],
        "style": {
            "c": "blue",
        }
    },
    "pt_4":{
        "flows": ["flow_31", "flow_32", "flow_33"],
        "style": {
            "c": "green",
        }
    }
}

COLORS = {
    "flow_0": "y",
    "flow_1": "blue",
    "flow_2": "orange",
    "flow_3": "green",
    # "flow_4": "red",
    # "flow_5": "purple",
}
COLOR_ALPHA = {
    "current": 0.2,
    "proposed": 0.35
}
PT_ALPHA = {
    "current": 0.35,
    "proposed": 0.5
}
LINESTYLES = {
    "current": "dashed",
    "proposed": "solid"
}

MARKERSTYLE = {
    "current": "o",
    "proposed": "x"
}

LABELS_MAPPING = {
    "flow_0": "ул. Жидилова",
    "flow_1": "ул. Горпищенко",
    "flow_2": "пл. Ластовая",
    "flow_3": "просп. Победы",
    "pt_1": "112",
    "pt_2": "T 1",
    "pt_3": "T 7,17,4",
    "pt_4": "T 9,19,20"
}

MODEL_TYPE_LABEL = {
    "current": "(сущ.)",
    "proposed": "(предл.)"
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
                'label': "{} {}".format(LABELS_MAPPING[flow_name], MODEL_TYPE_LABEL[model_type]),
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
                | { "label": "{} {}".format(LABELS_MAPPING[pt_flow], MODEL_TYPE_LABEL[model_type]) }
                | PT_FLOWS[pt_flow]['style']
                | { "marker": MARKERSTYLE[model_type], "alpha": PT_ALPHA[model_type] })


        # polynom = np.poly1d(np.polyfit(range(len(data)), data, deg=10))
        # new_x = np.linspace(0, len(data))
        # plt.plot(new_x, polynom(new_x), label=flow_name, linewidth=2, color=COLORS[flow_name], linestyle=LINESTYLES[model_type])

    for plot_data in plots_data1:
        do_plot(ax[0], plot_data)
    
    for plot_data in plots_data2:
        do_plot(ax[1], plot_data)

    for plot in ax:
        plot.legend()

    plt.show()


experiments_count = int(sys.argv[1])
variants = sys.argv[2:]

results = {}
for variant in variants:
    with open(variant + '.json', 'r') as variant_results:
        results[variant] = json.loads(variant_results.read())

plot_results(results, experiments_count)
