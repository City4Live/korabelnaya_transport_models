import utils
import pandas as pd
import matplotlib.pyplot as plt

FLOW_COUNT = 6
FLOW_NAME = "flow_{}"

CAR_FLOWS = ["flow_0", "flow_1", "flow_2", "flow_3"]
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
}
COLOR_ALPHA = {
    "current": 0.15,
    "proposed": 0.40
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
    ax.set_ylabel('Время прохождения участка, c')
    ax.set_xlabel('Время (момент) отправления, секунд от начала моделирования')

def process_data(data):
    sorted_df = data.sort_values(by=['departTime'])

    return  {
            'x': sorted_df['departTime'].to_list(),
            'y': sorted_df['travelTime'].to_list()
        }

def plot_results(results):

    fig, ax = plt.subplots(2, 1)

    plots_data1 = []
    plots_data2 = []

    for model_type in results:
        result = results[model_type]

        for flow_name in CAR_FLOWS:
            processed = process_data(result[result['flow'] == flow_name])
            style = {
                'label': "{} {}".format(LABELS_MAPPING[flow_name], MODEL_TYPE_LABEL[model_type]),
                'c': COLORS[flow_name],
                'marker': MARKERSTYLE[model_type],
                'alpha': COLOR_ALPHA[model_type]
            }
            plots_data1.append(processed | style)

        for pt_flow in PT_FLOWS:
            data = result[result['flow'].isin(PT_FLOWS[pt_flow]["flows"])]
            plots_data2.append(
                process_data(data)
                | { "label": "{} {}".format(LABELS_MAPPING[pt_flow], MODEL_TYPE_LABEL[model_type]) }
                | PT_FLOWS[pt_flow]['style']
                | { "marker": MARKERSTYLE[model_type], "alpha": PT_ALPHA[model_type] })

    for plot_data in plots_data1:
        do_plot(ax[0], plot_data)

    for plot_data in plots_data2:
        do_plot(ax[1], plot_data)

    ax[0].set_title("Легковые ТС")
    ax[1].set_title("НГПТ")

    for plot in ax:
        plot.legend()

    plt.show()
