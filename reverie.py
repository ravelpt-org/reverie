import subprocess
import os
import re
import sys

f_import = re.compile('from (.*?) import', re.MULTILINE)
i_import = re.compile('import (.*?$)', re.MULTILINE)

python_allowed = ['math', 'strings', 'collections', 'datetime', 'itertools', 'heapq']
# Using .* breaks this, also grabs ;
# Import static fails this
java_allowed = ['java.util', 'java.util.*;',  'java.lang.Math;', 'java.lang.Math.*;']

def is_clear(match_string, data, allowed):
    f = re.findall(match_string, data)
    if f is not None:
        for imported in f:
            if imported not in allowed:
                print(f'{imported} in not allowed')
                return False

    return True


def check_python(file):
    with open(file, 'r') as f:
        data = f.read()

    if is_clear(f_import, data, python_allowed):
        return is_clear(i_import, data, python_allowed)
    else:
        return False


def check_java(file):
    with open(file, 'r') as f:
        data = f.read()
    return is_clear(i_import, data, java_allowed)

prob_in = open("./sample_in.txt", "rb").read()
prob_out = open("./sample_out.txt", "r").read().splitlines()

def run(command):
    print(f"running {command}")
    return subprocess.Popen(command, stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def build(file):
    p = run(['javac', file])
    stdout, stderr = write_multiple(p)

    if stderr != "":
        return False, stderr
    else:
        return True, None

def write_multiple(process: subprocess.Popen, problem_in="", timeout=240):
    try:
        stdout, stderr = process.communicate(problem_in, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "", "Timelimit Exception"
    return stdout, stderr

def finish(status):
    with open("status.txt", 'w', encoding='utf-8') as f:
        f.write(status)
    sys.exit()


def check(process, problem_in):
    output, errors = write_multiple(process, problem_in)

    print("Looking for output:")

    if len(errors) > 0 and errors != "Timelimit Exception":
        print(f"Runtime error: {errors}")
        finish("Runtime Error")
    elif errors == "Timelimit Exception":
        finish("Timelimit Exception")

    if isinstance(output, list) and len(output) <= 0:
        finish("Timelimit Exception")
        return False
    else:
        output = output.decode('utf-8').replace("\r", "").splitlines()

    if output == prob_out:
        finish("Correct")
    else:
        print(output)
        print(prob_out)
        finish("Wrong")

        return False

def main(problem_in):
    if os.path.isfile("solution.java"):
        file_path = "solution.java"
        if check_java(file_path):
            built, error = True, ""

            if not built:
                print(error)
                finish("Compiler Error")
                return

            command = ["java", file_path]
        else:
            print("File imports illegal libraries")
            finish("Illegal Import")
            return
    elif os.path.isfile("solution.py"):
        file_path = "solution.py"
        if check_python(file_path):
            command = ["python", file_path]
        else:
            print("File imports illegal modules")
            finish("Illegal Import")
            return
    else:
        print("not a valid file")
        return
    status = check(run(command), problem_in)
    print(f"Solved: {status}")
    print("Running")    

main(prob_in)
