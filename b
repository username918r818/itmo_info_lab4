def get_dict(source):
    a = str(re.search(r"{((?:.*[\n]*)*)}", str(source)).group(0))
    it = 0
    result = {}
    while it != len(source) - 1:
        it_begin = a.find('"', it + 1) + 1
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
            new_it = source.rfind('}') + 1
            pattern = r"{((?:.*?[\n]*?)*)}"
            b = a[it:new_it]
            b = re.search(pattern, b).group(0)
            result.update({tag: get_dict(b)})
        elif elements[1] == min(elements):
            new_it = source.rfind(']') + 1
            pattern = r"[((?:.*?[\n]*?)*)]"
            b = a[it:new_it]
            b = re.search(pattern, b).group(0)
            result.update({tag: get_array(b)})
        elif elements[2] == min(elements):
            it_begin = a.find('"', it + 1) + 1
            it_end = a.find('"',it_begin)
            word = a[it_begin:it_end]
            result.update({tag: word})
            new_it = it_end + 1
        it = new_it
    return result