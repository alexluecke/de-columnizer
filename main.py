import re
import argparse

def start(filename):
    lines = open(filename).read().split('\n')
    print de_columnize(lines[1:])

def find_par_idxs(lines):
    par_idxs = [0]
    # Don't include very last line of file as new paragraph
    for idx in xrange(0, len(lines)-1):
        if re.sub("[|\-+]", "", lines[idx]).strip() == '':
            par_idxs.append(idx)
    return par_idxs

def de_columnize(lines):

    start_capture = False
    fixed = ''
    box_text = ''
    captured_boxes = {}

    par_idxs = find_par_idxs(lines)

    print par_idxs
    for idx in par_idxs:
        captured_boxes[idx] = []

    next_par_idx = par_idxs.pop()

    for idx in reversed(range(len(lines))):
        if start_capture:
            if re.match("[|]?.*\+-+\+.*[|]?", lines[idx]):
                box_text = "(" + box_text.strip() + ")"
                if idx < next_par_idx:
                    next_par_idx = par_idxs.pop()
                captured_boxes[next_par_idx].insert(0, box_text)
                start_capture = False
            else:
                box_text = capture_box_line(lines[idx]) + ' ' + box_text
        else:
            if re.match(".*\+-+\+.*", lines[idx]):
                box_text = ''
                start_capture = True

        lines[idx] = re.sub("[|][^|]*[|]", "", lines[idx])
        lines[idx] = re.sub("(\| *)?\+-+\+( *\|)?", "", lines[idx]).strip()

        prefix = ''
        if next_par_idx == idx and not start_capture:
            prefix = " ".join(captured_boxes[next_par_idx]) + " "

        if lines[idx][-1:] == '-':
            fixed = prefix + lines[idx][:-1] + fixed
        else:
            fixed = prefix + lines[idx] + ' ' + fixed

        if next_par_idx == idx and idx != 0:
            fixed = "\n" + fixed

    return re.sub(' +', ' ', fixed).strip()

def capture_box_line(line):
    return re.sub(".*\|([^|]*)\|.*", "\\1", line).strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f','--filename', help='Input file name', required=True)
    args = parser.parse_args()
    start(args.filename)
