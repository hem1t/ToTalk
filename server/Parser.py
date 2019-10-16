run = False
if __name__ == "__main__":
    run = True


def packet_parser(data):
    """
    parser functions takes the utf-8 encoded data and will
    return a dictionary of headers and it's values.
    """
    i = data.index("{")
    new_data = {}
    methods, data = data[:i], data[i:]
    key = ""
    value = ""
    complete = 0
    escape = False  # / will be escape for " ' , : /
    string = ""
    escape_toggle = False
    print(data) if run else ""
    for char in data:
        if char == "/" and not escape:
            escape = True

        if not escape and char == ":":
            key = string
            string = ""
            complete += 1
            print("c1") if run else ""
        elif not escape and char == ",":
            value = string
            string = ""
            complete += 1
            print("c2") if run else ""
        elif char == "{" or char == "}":
            pass
        elif escape_toggle:
            escape = False
            escape_toggle = False
            string += char
        else:
            if not escape:
                string += char
            else:
                escape_toggle = True

        if complete == 2:
            print("complete") if run else ""
            new_data[key] = value
            complete = 0
    print("done") if run else ""
    if run:
        return new_data
    else:
        return new_data, [method for method in methods.split("\n")]


if run:
    a = packet_parser("{name: m/'s jd/'s,}")
    print(a["name"])
    print(packet_parser("{/\"key/\":value,}"))
    print(packet_parser("{key:value, key1:value1,}"))
    print(packet_parser("lksdf: ks, {key:value,"
                        "key1:value1,}"))
    print(packet_parser("lksd f: k s, {k e y:v a/,lue, key 1#:v/:alu}e 1,}"))
