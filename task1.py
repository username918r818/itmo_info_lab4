# variant 8:
# from json to yaml
# Tuesday

# прямая конвертация, я бы такое на плюсах написал

def json_to_yaml(source):
    it_begin = source.find('{')
    it_end = source.rfind('}') 
    inner_type = ''
    status = 'SCAN'
    level = 0
    levels = []
    # KEY VALUE LIST_ELEMENT
    # SCAN READ
    level_down =  ['{', '[']
    level_up =  ['}', ']']
    word = ""
    result = ""
    banned = -1
    debug = 0
    for it in range(it_begin, it_end):
        
        if source[it] in level_down:
            level += 1
            if source[it] == '{':
                levels.append("DICT")
                inner_type = "KEY_FIRST"
            else:
                levels.append("LIST")
                inner_type = "LIST_ELEMENT"
            continue
        elif source[it] in level_up:
            level -= 1
            levels.pop()
            continue
        elif it <= banned:
            continue
        elif source[it] == '"':
            debug = 0
            it += 1
            it_new = source.find('"', it)
            word = source[it:it_new]
            banned = it_new
            if inner_type == "KEY_FIRST" or inner_type == "KEY":
                result += '\n'
                for i in levels:
                    if i == "LIST":
                        result += '  '
                if debug:
                    print("--!!!------")
                    print(levels)
                    print(inner_type)
                    print(it)
                    print("-----------")

                if len(levels) > 1:
                    if levels[-2] == "LIST" and inner_type == "KEY_FIRST":
                        result = result[0:len(result)-2]
                        result += "- "
                result += word + ': '
                inner_type = "VALUE"
            else:
                if inner_type == "LIST_ELEMENT":
                    result += '\n'
                    for i in levels:
                        if i == "LIST":
                            result += '  '
                    result = result[0:len(result)-2]
                    result += "- "
                else:
                    inner_type = "KEY"
                result += word
    return result[1:]


for i in range(330):
    for number in range(0, 3):
        f = open(f"schedules/schedule{number}.json")
        str = f.read()
        result = json_to_yaml(str)

        w = open(f"output/task1_{number}.txt", 'w')
        w.write(result)
            

            



