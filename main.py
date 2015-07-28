import re
import argparse

def start(filename):
    lines = open(filename).read().split('\n')
    for item in de_columnize(lines[1:]):
        print item

def de_columnize(lines):

    chunks = 0
    joined = ['']
    originals = lines

    prefix_data = handle_box(lines)

    paridx = 0
    for idx in xrange(0, len(lines)):
        lines[idx] = re.sub("[+|][^+|]*[+|]", "", lines[idx])
        lines[idx] = re.sub("(^ *| *$)", "", lines[idx]).strip()

        if lines[idx] == '':
            paridx = idx+1
            lines[idx] = '\n'
            continue

        temp_idx = idx
        for item in prefix_data:
            if item['line'] == idx:
                while idx > paridx:
                    idx = idx - 1
                lines[idx] = item['value'] + " " + lines[idx]
        idx = temp_idx

    for line in lines:
        if joined[chunks][-1:] == '-':
            joined[chunks] = joined[chunks][:-1] + line
        elif joined[chunks][-1:] == '\n':
            joined[chunks] = joined[chunks] + line
        else:
            joined[chunks] = joined[chunks] + ' ' + line

    for idx in xrange(len(joined)):
        joined[idx] = joined[idx].strip()

    return filter(lambda x: x.strip() != '', joined)

def handle_box(lines):

    capture = []
    count = 0
    start_capture = False
    stop_capture = False

    for idx in xrange(len(lines)):

        if re.match(".*\+-+\+.*", lines[idx]):

            if start_capture:
                capture[0]['value'] = filter(
                    lambda x: x.strip() != '',
                    capture[0]['value']
                )
                start_capture = False
            else:
                capture.insert(0, { 'line': 0, 'value': [] })
                capture[0]['line'] = idx
                start_capture = True
                continue

        if start_capture:
            clean = re.sub(".*\|([^|]*)\|.*", "\\1", lines[idx]).strip()
            capture[0]['value'].append(clean)

    for idx in xrange(len(capture)):
        capture[idx]['value'] = " ".join(capture[idx]['value'])
        capture[idx]['value'] = "(" + capture[idx]['value'] + ")"

    return capture

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f','--filename', help='Input file name', required=True)
    args = parser.parse_args()
    start(args.filename)
