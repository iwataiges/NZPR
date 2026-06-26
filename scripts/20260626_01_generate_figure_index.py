# -*- coding: utf-8 -*-
import sys
import re

def main(input):
    f = open(input)
    fig_counter = 0

    for line in f:
        s = line.split()
        if len(s) > 0:
            m = s[0]

            if m == '##':
                chapter = s[1].replace('.','')
                section = ''
                subsection = ''
                fig_counter = 0
                print(line)
            elif m == '###':
                section = s[1].replace('.','')
                subsection = ''
#                print(line)
            elif m == '####':
                subsection = s[1].replace('.','')
#                print(line)

            if '*図[' in s[0]:
                match = re.search(r"\[(.*?)\]", line)
                t = match.group(1)
                fig_counter += 1
                print('%s %s %02d %s %s' % (chapter, t, fig_counter, section, subsection))

if __name__ == '__main__':
    input = sys.argv[1]
    main(input)
