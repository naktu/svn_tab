#!/usr/bin/env python3

from sys import argv
import pytablewriter

row = []
rows = []
comment = False
first_column = {
      ' ': 'no modifications',
      'A': 'Added',
      'C': 'Conflicted',
      'D': 'Deleted',
      'I': 'Ignored',
      'M': 'Modified',
      'R': 'Replaced',
      'X': 'an unversioned directory created by an externals definition',
      '?': 'item is not under version control',
      '!': 'item is missing (removed by non-svn command) or incomplete',
      '~': 'versioned item obstructed by some item of a different kind',
}
third_column = {
      ' ': 'normal',
      'C': 'tree-Conflicted',

}
with open(argv[1]) as svndoutput:
    for line in svndoutput:
        row = []
        if comment == False:
            row = [first_column[line[0]], line[3], third_column[line[6]]]
            for data in line[7:].split(' '):  
                if data != '':
                    if data[-1] == '\n':                # delete last '\n'
                        row.append(data[:-1])
                    else:
                        row.append(data)
            if row[2] == 'tree-Conflicted':                           # if have 'C' we need write next streen in new last column
                comment = True
            elif row[0] != 'item is not under version control':
                row.append('')
            else:
                row = [row[0], ' ', ' ', ' ', ' ', ' ', row[-1][:-1], '']       # need 8 columns, but string with '?' have less
            rows.append(row)
        else:
            s = ''
            for i in line.split(' '):
                if i not in ['', '>']:
                    if i[-1] == '\n':
                        s = s + i[:-1] + ' '
                    else:
                        s = s + i + ' '
            rows[-1].append(s[:-1])             # -2 using for deliting last whitespace and \n
            comment = False
for i in rows:
    print(i)
writer = pytablewriter.RstGridTableWriter()
writer.table_name = 'SVN Status'
writer.header_list = ['Item Status', 'Second', 'Tree conflict', 'Numb1', 'Nubm2', 'User', 'Path', 'Comment']
writer.value_matrix = rows

writer.write_table()