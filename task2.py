# variant 8:
# from json to yaml
# Tuesday

# использование библиотек

import json
import yaml


for i in range(330):
    for number in range(0, 3):
        data = json.load(open(f"schedules/schedule{number}.json"))
        result = yaml.dump(data)

        w = open(f"output/task2_{number}.txt", 'w')
        w.write(result)
            

            



