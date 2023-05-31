import build_config
import stats
import os
import json
import subprocess
import sys
import numpy as np
import matplotlib.pyplot as plt
import random

ROU_CONFIG_PATH = "{}/{}.rou.xml"
TEMPLATE_SUFFIX = ".jinja2"
CONFIG_PATH = "{}/config.sumocfg"

variant = sys.argv[1]
experiments_count = int(sys.argv[2])

def simulate_variant(model_type, simulation_seed):
    # config_name = ROU_CONFIG_PATH.format(model_type, model_type)
    # with open(config_name, 'w') as config_out:
    #     config_out.write(build_config.build_config(config_name + TEMPLATE_SUFFIX, [turn_rate, 0.25, 0.3]))

    process = subprocess.Popen(['sumo', '-c', CONFIG_PATH.format(model_type), "--seed", str(simulation_seed)],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return stats.get_stats(model_type)

with open('seeds.json', 'r') as seeds_input:
    seeds = json.loads(seeds_input.read())

results = []

# for turn_rate in range(10, 36, 5):
    # turn_rate_results = []
for i in range(experiments_count):
    results.append(simulate_variant(variant, seeds[i]))
# results[turn_rate] = turn_rate_results

with open(variant + '.json', 'w') as output:
    output.write(json.dumps(results))
