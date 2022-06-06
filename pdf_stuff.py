from pdfminer import high_level
import os
import re
import shutil

directory = 'C:/Users/sean.ruane/pdf_searchable/'  #py_tests/' #C:\Users\sean.ruane\pdf_searchable
directory2 = 'C:/Users/sean.ruane/pdf_output/'


for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        local_pdf_filename = f
        pages = [0]
        extracted_text = high_level.extract_text(local_pdf_filename, "", pages)
        lines = extracted_text.split("\n")
        ein_find = re.compile(r'^\w+\d?-\w+')

        for line in lines:
            if ein_find.search(line):
                if len(line.strip()) == 10:
                    ein = line.strip()
                    g = os.path.join(directory2, ein + '_' + filename)
                    end_file = ein + '_' + filename
                    shutil.copyfile(directory + filename, directory2 + end_file)

print("Files Done!")