#!/usr/bin/env python
import sys
import os

if len(sys.argv) != 2:
    print("Incorrect usage.")
    print("Correct usage: [input_file]")
    sys.exit()

inputFile = open(sys.argv[1], 'r')
outputFile = open((sys.argv[1][:-4] + ".tex"), 'w+')
cwd = os.getcwd()
course = cwd[cwd.rfind("/")+1:]
date = sys.argv[1][-8:-4]

headFile = open('res/head.tex', 'r')
midFile = open('res/mid.tex', 'r')

outputFile.write(headFile.read())
outputFile.write("\\newcommand{\\mydate}{" + date + "}\n")

course = course[:2] + "-" + course[2:]

outputFile.write("\\newcommand{\\mycourse}{" + course + "}\n")

outputFile.write(midFile.read())

indentCount = 0
for line in inputFile:
    line = line.replace("<", "\\textless")
    line = line.replace(">", "\\textgreater")
    newIndentCount = (len(line) - len(line.lstrip())) / 2
    if newIndentCount > indentCount:
        outputFile.write("  " * indentCount + "\\begin{itemize}\n")
    elif newIndentCount < indentCount:
        if indentCount - newIndentCount > 1:
            count = indentCount - newIndentCount
            count -= 1
            while count >= 1:
                outputFile.write("  " * count + "\\end{itemize}\n")
                count -= 1
        outputFile.write("  " * newIndentCount + "\\end{itemize}\n")
    if line.strip() == "":
        outputFile.write("\n")
        continue
    elif line.isupper():
        outputFile.write("\\textbf{" + line.strip() + "}\\\\\n")
    elif newIndentCount != 0:
        outputFile.write("  " * newIndentCount + "\\item " + line.strip() + "\n")
    else:
        outputFile.write("  " * newIndentCount + line.strip() + "\n")
    indentCount = newIndentCount

outputFile.write("\\end{document}")
