# -*- coding: utf-8 -*-
import sys
import re

def main(input, index, output):
    f = open(index)
    fig_index = []
    for line in f:
        s = line.split()
        if len(s) > 0:
            chapter = s[0]
            label = s[1]
            figno = int(s[2])
            dict = {
                'chapter': chapter,
                'label': label,
                'figno': figno
            }
            fig_index.append(dict)

    fout = open(output, 'w')

    f = open(input)
    for line in f:
        for item in fig_index:
            t = '['+item['label']+']'
            if t in line:
                string = '%s-%d' % (item['chapter'], item['figno'])
                rep = line.replace(t, string)
                line = rep

        fout.write(line)


if __name__ == '__main__':
    input = sys.argv[1]
    index = sys.argv[2]
    output = sys.argv[3]
    main(input, index, output)
