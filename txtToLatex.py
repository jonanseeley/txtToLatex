#!/usr/bin/env python
import sys
import os
import argparse
from subprocess import call

# Setting up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("file", help="Filename for .txt file", type=str)
parser.add_argument("name", help="Your name", type=str)
parser.add_argument("course", help="Name of course", type=str)
parser.add_argument("title", help="Title of notes", type=str)
args = parser.parse_args()

# Initialize output file
inputFile = open(args.file, 'r')
outputFilePath = args.file[:-4] + ".tex"
outputFile = open(outputFilePath, 'w+')

# Open reference files
headFile = open('res/head.tex', 'r')
midFile = open('res/mid.tex', 'r')

# Write commands to file to be used in header
outputFile.write(headFile.read())
outputFile.write("\\newcommand{\\myname}{" + args.name + "}\n")
outputFile.write("\\newcommand{\\mytitle}{" + args.title + "}\n")
outputFile.write("\\newcommand{\\mycourse}{" + args.course + "}\n")
outputFile.write(midFile.read())

# Loop to process tabs into indents in a itemized list
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
