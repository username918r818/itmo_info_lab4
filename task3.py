# variant 8:
# from json to yaml
# Tuesday

# использование регулярок уродливо, но все же они есть
# как в явном виде, так и через различные методы вроде find

import re

def get_json(source):
    return get_dict(source)

def get_dict(source):
    a = str(re.search(r"{((?:.*[\n]*)*)}", str(source)).group(0))
    it = 0
    result = {}
    banished = 0
    for it in range(0, len(a)):
        if it < banished:
            continue
        it_begin = a.find('"', it + 1) + 1
        if it_begin == 0:
            return result
        it_end = a.find('"', it_begin)
        tag = a[it_begin:it_end]
        it = it_end + 1
        new_it = it
        elements = [source.find('{', it), source.find('[', it), source.find('"', it)]
        for i in range(0, len(elements)):
            if elements[i] == -1:
                elements[i] = 100000000000000000 #inf
        if min(elements) == 100000000000000000:
            return result
        if elements[0] == min(elements):
            diff_open_closed_brackets = 0
            it = source.find('{', it)
            for i in range(it, len(a)):
                if a[i] == '}':
                    diff_open_closed_brackets += 1
                elif a[i] == '{':
                    diff_open_closed_brackets -= 1
                if diff_open_closed_brackets == 0:
                    new_it = i
                    break
            new_it += 1
            b = a[it:new_it]
            result.update({tag: get_dict(b)})
        elif elements[1] == min(elements):
            diff_open_closed_brackets = 0
            it = source.find('[', it)
            for i in range(it, len(a)):
                if a[i] == ']':
                    diff_open_closed_brackets += 1
                elif a[i] == '[':
                    diff_open_closed_brackets -= 1
                if diff_open_closed_brackets == 0:
                    new_it = i
                    break
            new_it += 1
            b = a[it:new_it]
            result.update({tag: get_array(b)})
        elif elements[2] == min(elements):
            it_begin = a.find('"', it + 1) + 1
            it_end = a.find('"',it_begin)
            word = a[it_begin:it_end]
            result.update({tag: word})
            new_it = it_end + 1
        it = new_it
        banished = it
    return result
        

def get_array(source):
    a = str(re.search(r"\[((?:.*[\n]*)*)\]", str(source)).group(0))
    a = a[1:len(a)-2]
    it = 0
    result = []
    while it != len(a) - 1:
        elements = [a.find('{', it), a.find('[', it), a.find('"', it)]
        for i in range(0, len(elements)):
            if elements[i] == -1:
                elements[i] = 100000000000000000 #inf
        if min(elements) == 100000000000000000:
            return result
        new_it = 0
        if elements[0] == min(elements):
            diff_open_closed_brackets = 0
            it = a.find('{', it)
            for i in range(it, len(a)):
                if a[i] == '}':
                    diff_open_closed_brackets += 1
                elif a[i] == '{':
                    diff_open_closed_brackets -= 1
                if diff_open_closed_brackets == 0:
                    new_it = i
                    break
            new_it += 1
            b = a[it:new_it]
            result.append(get_dict(b))
        elif elements[1] == min(elements):
            diff_open_closed_brackets = 0
            it = source.find('[', it)
            for i in range(it, len(a)):
                if a[i] == ']':
                    diff_open_closed_brackets += 1
                elif a[i] == '[':
                    diff_open_closed_brackets -= 1
                if diff_open_closed_brackets == 0:
                    new_it = i
                    break
            new_it += 1
            b = a[it:new_it]
            result.append(get_array(b))
        elif elements[2] == min(elements):
            it_begin = a.find('"', it + 1) + 1
            it_end = a.find('"',it_begin)
            word = a[it_begin:it_end]
            result.append(word)
            new_it = it_end + 1
        it = new_it
    return result

    
        


def to_yaml(source, result="", level=0, is_in_list=0, is_a_value=0):
    # print(type({}))
    # print(type([]))
    # print(type(""))
    if isinstance(source, dict):
        for x in source.keys():
            for i in range(1, level):
                result += "  "
            if level >= 1:
                if is_in_list:
                    result += "- "
                    is_in_list = False
                else:
                    result += "  "
            result += x + ':\n'
            result = to_yaml(source[x], result, level, 0, 1)
    elif isinstance(source, list):
        for x in source:
            result = to_yaml(x, result, level+1, 1)
    else:
        if is_a_value:
            result = result[0:len(result)-1] + f" {source}\n"
            return result
        for i in range(1, level):
            result += "  "
        if level >= 1:
            if is_in_list:
                result += "- "
            else:
                result += "  "
        result += source + '\n'
    # print(source)
    return result
            



for i in range(330):
    for number in range(0, 3):
        f = open(f"schedules/schedule{number}.json")
        source = f.read()
        result = get_json(source)
        result = to_yaml(result)
        w = open(f"output/task3_{number}.txt", 'w')
        w.write(result)
            

            



