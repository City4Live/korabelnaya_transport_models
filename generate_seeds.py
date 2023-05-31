import random
import sys
import json

count = int(sys.argv[1])

seeds = [random.randint(1, 9999999) for i in range(count)]

with open('seeds.json', 'w') as output:
    output.write(json.dumps(seeds))
