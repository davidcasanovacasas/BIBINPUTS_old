from pybtex.database import parse_string
from pybtex.errors import set_strict_mode
import re, os
import shutil

################################################################################

# This script reads all BIB files in the current directory and subdirectories
# and generates a output BIB file containing the citations found in the provided
# TEX file.
# It requires pybtex library that can be installed via PIP (pip install pybtex)

#################################   INPUT   #####################################

folder_input = '/Users/David/david/Group_Members/Carreras_Abel/TADF/Paper/Revision/Manuscript/'
file_input = 'main_revised.tex'
paper_file = folder_input + file_input
abbr_file = 'abbr.bib'
abbr_orig_file = '/Users/david/Dropbox/BIBINPUTS/' + abbr_file

#################################   OUTPUT   ####################################

bib_file = 'bibliography.bib'
output_bib_file = folder_input + bib_file
abbr_copy = folder_input + abbr_file

#################################################################################

# Copy abbr.bib to the folder
shutil.copyfile(abbr_orig_file,abbr_copy)

# Open TEX file
paper = open(paper_file).read().replace('\n', '')


# Search for citations in TEX file
cites_list = []
for a_string in ['\cite{', '\citenum{']:
    for m in re.finditer(re.escape(a_string), paper):
        # print(paper[m.end():m.end()+500].split('}')[0])
        cites_list += paper[m.end():m.end()+500].split('}')[0].split(',')


# get unique citations list of TEX file
unique_cites = []
for cite in cites_list:
    if cite not in unique_cites:
        unique_cites.append(cite)


print('Citations found')
for i, cite in enumerate(cites_list):
    print('{:5} {} '.format(i+1, cite))


# Read all bib files in directory and subdirectories
print('\nRead bibliography from:')
set_strict_mode(enable=False)
big_string = ''
for path, subdirs, files in os.walk('.'):
    for name in files:
        file_path = os.path.join(path, name)
        filename, extension = os.path.splitext(file_path)
        if extension.lower() == '.bib':
            print('  {}'.format(name))
            with open(file_path) as f:
                big_string += f.read()

bib_data = parse_string(big_string, 'bibtex')

bib_cite_list = []
for cite in unique_cites:
    if cite in bib_data.entries:
        if bib_data.entries[cite] not in bib_cite_list:
            bib_cite_list.append(bib_data.entries[cite])

if len(bib_cite_list) < len(unique_cites):
    print('Warning: some citations are missing')

# write output bib file
with open(output_bib_file, 'w') as f:
    for entry in bib_cite_list:
        # print(entry.to_string('bibtex'))
        f.write(entry.to_string('bibtex'))
