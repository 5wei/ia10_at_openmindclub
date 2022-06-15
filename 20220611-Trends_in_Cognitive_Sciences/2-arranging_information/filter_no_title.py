# -*- coding: UTF-8 -*-

in_file = open("..\\1\\TiCS_meta.bib", mode='r', encoding='utf8')
out_file = open("TiCS_meta.bib", mode='w', encoding='utf8')

count = 0

while True:
    count += 1
    line = in_file.readline()
    if not line:
        break
    filtered_line = line.replace("{[}No title captured]", "{[}No title captured " + str(count) +  "]").replace("{[}Anonymous]", "{[}Anonymous " + str(count) + "]")
    out_file.write(filtered_line)

in_file.close()
out_file.close()