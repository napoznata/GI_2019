from index_hash import IndexHash
from index_sorted import IndexSorted
from suffix_array import SuffixArray
from suffix_tree import SuffixTree
from benchmark import benchmark_run
import os
from pathlib import Path
from config import *
from diagram import *
import ntpath
import gc

algorithms = [IndexHash(), IndexSorted(), SuffixArray(), SuffixTree()]

tests_dir = Path(performance_tests_dir_path)
tests_results_dir = Path(performance_tests_results_dir)
test_files = []


def rstrip(line):
    return line.rstrip('\n')


def print_separator():
    print('-' * 100)


for file in os.listdir(tests_dir):
    test_files.append(tests_dir / file)

for test_file_name in test_files:

    test_file_name_short = ntpath.basename(test_file_name)

    print("")
    print_separator()
    print("Test file: " + test_file_name_short)
    print_separator()

    test_file = open(test_file_name, 'r')
    lines = test_file.readlines()

    genome = ''.join(map(rstrip, lines[2:]))
    patterns = [x for x in lines[1].rstrip('\n').split(',')]

    index = test_files.index(test_file_name)

    all_results = []

    for algorithm in algorithms:
        test_results_file_path = tests_results_dir / (algorithm.get_name() + str(index) + ".txt")
        test_results_file = open(test_results_file_path, "w+")
        result = benchmark_run(algorithm, genome, patterns, algorithm.get_name(),num_of_test_iterations)
        all_results.append(result)
        test_results_file.write(str(result))
        gc.collect()

    print("")
    print_separator()
    plot_add_results(all_results, test_file_name_short)

print_separator()
plot_show()
