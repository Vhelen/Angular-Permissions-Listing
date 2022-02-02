import os
import pathlib
import json


def add_perm(perms_dict, perm_to_add, file_perm, line_perm):
    if perm_to_add not in perms_dict:
        perms_dict[perm_to_add] = {}

    if file_perm not in perms_dict[perm_to_add]:
        perms_dict[perm_to_add][file_perm] = []

    perms_dict[perm_to_add][file_perm].append(line_perm)

    return perms_dict


html_files = []
for path, sub_dirs, files in os.walk('to_analyse'):
    for filename in files:
        file = os.path.join(path, filename)
        file_extension = pathlib.Path(file).suffix

        if file_extension == ".html":
            html_files.append(file)

perms = {}
for file in html_files:
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        x = 0

        for line in lines:
            x += 1

            if "*ngxPermissionsOnly" in line:
                line_perms = line[line.find('*ngxPermissionsOnly=') + len("*ngxPermissionsOnly=") + 1:]

                line_perms = line_perms.replace("'", "")

                if line_perms[0] == '[':
                    line_perms = line_perms[1:line_perms.find(']')]
                    for perm in line_perms.split(', '):
                        perms = add_perm(perms, perm, file, x)
                else:
                    line_perms = line_perms[:line_perms.find('"')]
                    perms = add_perm(perms, line_perms, file, x)

with open('perms.json', 'w') as fp:
    json.dump(perms, fp)



