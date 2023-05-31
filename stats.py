from locale import DAY_1
import sys
import argparse
import json
import pandas as pd

from xml.sax import make_parser

# from more_itertools import split_into
from statisticsElements import Assign, T_Value, H_Value, VehInformationReader
from statisticsElements import getStatisticsOutput, getSignificanceTestOutput
# from norm import *
from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('/usr/share/sumo/tools/output')

IN_FILE_PATTERN = "{}/tripinfo-output.xml"
CONFIG_FILE_PATTERN = "sumo_{}/stats_analysis.json"
# FLOWS_COUNT = 15

def diff(a, b):
    return [a_i - b_i for a_i, b_i in zip(a, b)]

def split_into_chunks(data, step=10):
    x = []
    y = []
    for i in range(0, len(data), step):
        x.append(i + step / 2)
        y.append(data[i:i + step])
    return x, y

def plot_statistic(p, s_x, s_data, color, label):
    f_cubic = interp1d(s_x, s_data, kind='cubic')
    p.plot(s_x, s_data, '.', color=color, label=label)
    x_new = np.linspace(min(s_x), max(s_x), len(s_data) * 4)
    p.plot(x_new, f_cubic(x_new), color=color)
    return [min(s_data), max(s_data)]

def get_stats(file_inst):
    parser = make_parser()
    vehicles = []
    parser.setContentHandler(VehInformationReader(vehicles))
    parser.parse(IN_FILE_PATTERN.format(file_inst))

    flows = {}

    for v in vehicles:
        f = v.label.split('.')[0]
        flow_number = int(f.split('_')[1])

        if f not in flows:
            flows[f] = {
                'count': 0,
                'traveltime': [],
                'waittime': []
            }

        flows[f]['count'] += 1
        flows[f]['traveltime'].append(v.traveltime)
        flows[f]['waittime'].append(v.waittime)

    return flows


def main():

    parser = argparse.ArgumentParser(description='Analyse tripinfo output files')
    parser.add_argument('files', metavar="FILE", type=str, nargs='+', help='sumo tripinfo output files')

    args = parser.parse_args()

    print(get_stats(args.files))

    # x = np.arange(FLOWS_COUNT)  # the label locations
    # single_width = 0.24
    # width = single_width * len(flows)  # the width of the bars

    # pos = -single_width / 2
    # # fig, ax = plt.subplots()
    # ax = {}
    # ax[0] = plt.subplot2grid((2, 2), (0, 0), colspan=2)
    # ax[1] = plt.subplot2grid((2, 2), (1, 0))
    # ax[2] = plt.subplot2grid((2, 2), (1, 1))

    # norm_i = 1

    # ylim = [10000, 0]
    # lim = [10000, 0]

    # for inst, data in flows.items():
    #     # plot flows
    #     means = [0] * FLOWS_COUNT
    #     for f, c in data.items():
    #         flow_number = int(f.split('_')[1])
    #         means[flow_number] = c
    #     print(inst + ' total stats:')
    #     print('cars: ' + str(sum(means[i] for i in range(13))))
    #     print('busses: ' + str(sum(means[i] for i in range(13,15))))
    #     print('deviation: ' + format_norm([x for x in diff(norm(means), norm(ideal_flows))]))
    #     print('deviation metric: ' + str(sum([abs(x) for x in diff(norm(means), norm(ideal_flows))])))
    #     rects = ax[0].bar(x + pos, means, single_width, label=inst)
    #     ax[0].bar_label(rects, padding=3)

    #     # plot average times
    #     # time_means = [0] * FLOWS_COUNT
    #     # for f_n, d in avg_times[inst].items():
    #     #     time_means[f_n] = sum(d) / len(d)
    #     # t_rects = ax[4].bar(x + pos, time_means, single_width, label=inst)
    #     # ax[4].bar_label(t_rects, padding=3)

    #     # ax[norm_i].pie(norm(means), labels=[str(x + 1) for x in range(len(means))])
    #     # ax[norm_i].axis('equal')
    #     # ax[norm_i].set_title('Norm flows for scheme ' + inst)

    #     ax_pos = norm_i
    #     data = times[inst]
    #     df = pd.DataFrame(data)
    #     df = df[df < df.quantile(0.9)].dropna(how="any")
    #     data = df[0].tolist()
    #     c_x, chunks = split_into_chunks(data)
    #     ylim = [min(ylim[0], min(data)) , max(ylim[1], max(data))]
    #     plot_statistic(ax[ax_pos], c_x, [max(chunk) for chunk in chunks], color='red', label='макс.')
    #     plot_statistic(ax[ax_pos], c_x, [min(chunk) for chunk in chunks], color='green', label='мин.')
    #     plot_statistic(ax[ax_pos], c_x, [sum(chunk) / len(chunk) for chunk in chunks], color='darkgrey', label='средн.')
    #     ax[ax_pos].scatter(range(len(data)), data, s=7, color='silver')
    #     ax[ax_pos].set_title(configs[inst]['title'])
    #     ax[ax_pos].set_xlabel('Номер транспортного средства')
    #     ax[ax_pos].set_ylabel('Время прохождения участка, с')
    #     ax[ax_pos].legend(loc='best')

    #     # for f in range(FLOWS_COUNT):
    #     #     t = avg_times[inst][f]
    #     #     polynom = np.poly1d(np.polyfit(range(len(t)), t, deg=3))
    #     #     ax_pos = 6 + norm_i
    #     #     new_x = np.linspace(0, len(t))
    #     #     ax[ax_pos].plot(new_x, polynom(new_x), label='flow {}'.format(f + 1))
    #     #     current_lim = ax[ax_pos].get_ylim()
    #     #     lim = [min(lim[0], current_lim[0]), max(lim[1], current_lim[1])]
    #         # ax[ax_pos].scatter(range(len(t)), t, label='flow {}'.format(f + 1), s=7)

    #     pos += single_width
    #     norm_i += 1


    # ax[0].set_ylabel('Traffic flows')
    # ax[0].set_title('Traffic by flows and schemes')
    # ax[0].set_xticks(x, [str(x+1) for x in range(FLOWS_COUNT)])
    # ax[0].legend()

    # for i in range(len(flows)):
    #     ax[i + 1].set_ylim([max(0, ylim[0] - 10), ylim[1] + 15])

    # # for i in range(len(flows)):
    # #     ax[7 + i].set_ylim(lim)
    # #     ax[7 + i].legend()

    # # ax[4].set_xticks(x, [str(x+1) for x in range(FLOWS_COUNT)])
    # # ax[4].legend()

    # # ax[1].set_ylabel('Travel time')
    # # ax[1].set_title('Travel time by vehicle')
    # # ax[1].legend()
    # # # ax[1].set_xticks()
    # # ax[2].set_ylabel('Wait time')
    # # ax[2].set_title('Wait time by vehicle')
    # # ax[2].legend()

    # # ax[3].set_ylabel('Depart delay')
    # # ax[3].set_title('Depart delay by vehicle')
    # # ax[3].legend()

    # print('Ideal total flow: {}'.format(sum(ideal_flows)))

    # # fig.tight_layout()

    # plt.show()

    # print('Done')

    # # rects2 = ax.bar(x + width/2, women_means, width, label='Women')

    # # getStatisticsOutput(assignments, options.outputfile)
    # # print('The calculation of network statistics is done!')


    # # getSignificanceTestOutput(
    # #     assignments, options.ttest, tValueAvg, hValues, options.sgtoutputfile)
    # # print('The Significance test is done!')

if __name__ == "__main__":
    main()