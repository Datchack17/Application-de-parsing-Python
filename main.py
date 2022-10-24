
# encoding: utf-8
import string
import tempfile
import fileinput
import xml.sax
import xml.etree.cElementTree as ET
import os
import sys
import shutil

CSV_SEPARATOR = ";"
CATEGORY_TYPE = "CATEGORY"
TEST_TYPE = "TEST"
CONTENT_TYPE = "CONTENT"

def analyze_line(line):
    line_parsed = line.split(CSV_SEPARATOR)
    first = line_parsed[0]
    result = None

    if first.isdigit():
        line_type = TEST_TYPE
    elif first == "/":
        line_type = CATEGORY_TYPE
    else:
        line_type = CONTENT_TYPE

    if line_type == TEST_TYPE:
        test_name = line_parsed[1]
        test_description = line_parsed[2]
        result = [test_name, test_description]
    elif line_type == CATEGORY_TYPE:
        category_name = line_parsed[1]
        result = category_name
    else: # content
        test_content = line_parsed[0]
        result = test_content

    return line_type, result

def parse_csv(csv_file):
    fichier = open(csv_file, "r")
    lines = fichier.readlines()

    tests_suites = {}  # {"CATEGORY_1": [("test_1_name", "test_1_description"),], "CATEGORY_2": []}
    current_category = None
    for line in lines:
        type_of_line, line_content = analyze_line(line)

        if type_of_line == CATEGORY_TYPE:
            current_category = line_content
            tests_suites[current_category] = []
        elif type_of_line == TEST_TYPE:
            tests_suites[current_category].append(line_content)
        else:
            previous_description = tests_suites[current_category][-1][1]
            tests_suites[current_category][-1][1] = "{}/n{}".format(previous_description, line_content)

    return tests_suites

def ecriture_suite(suite_file):
    fichier = open(suite_file, "rt")
    data = fichier.read()
    data = data.replace("@DESCRIPTION_TESTSUITE@", category)
    fichier.close()
    fichier = open(suite_file, "wt")
    fichier.write(data)
    fichier.close()

def ecriture_file(file):
    # test_file.replace("@NAME@", test[0])
    fichier = open(file, "rt")
    data = fichier.read()
    data = data.replace("@NAME@", test[0])
    fichier.close()
    fichier = open(file, "wt")
    fichier.write(data)
    fichier.close()
    # test_file.replace("@DESCRIPTION@", test[1])
    fichier = open(file, "rt")
    data = fichier.read()
    data = data.replace("@DESCRIPTION@", test[1])
    fichier.close()
    fichier = open(file, "wt")
    fichier.write(data)
    fichier.close()

def copy_test(suite_file,file):
    # ajouter les test dans le fichier
    text_file = open(suite_file, "a")
    fichier = open(file)
    data = fichier.read()
    text_file.write(data + "\n")


if __name__ == '__main__':
    # ouverture du fichier
    tests_suites = parse_csv("jaguar.csv")
    i=0
    for tests_suite, tests in tests_suites.items():
        for test in tests:
            print("{} -> {} -> {}".format(tests_suite, test[0], test[1]))

        print("============================================================")

    test_suites_file = "suite_tests_template.xml"
    test_file = "simple_test_template.xml"
    for category, tests in tests_suites.items():

        #test_suites_file.replace("@DESCRIPTION_OF_TESTSUITE@", category)  # voir si replace() fonctionne
        ecriture_suite(test_suites_file)
        for test in tests:
            ecriture_file(test_file)
            copy_test(test_suites_file,test_file)
            shutil.copy("copie.xml",test_file)
        #ecriture d'un nouveau fichier
        new_file=open("fichier"+str(i)+".xml","w")
        new_file.close()
        text_file = open("fichier"+str(i)+".xml", "a")
        fichier = open(test_suites_file)
        data = fichier.read()
        text_file.write(data + "\n")
        text_file.write("</testsuite>")
        text_file.close()
        #copy du fichier
        shutil.copy("copie_suite.xml",test_suites_file)
        i=i+1

