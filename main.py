from index_hash import IndexHash
from index_sorted import IndexSorted
from suffix_array import SuffixArray
from suffix_tree import SuffixTree
from benchmark import benchmark_run
import os
import sys

from pathlib import Path

num_of_repeats = 1

def rstrip(line):
    return line.rstrip('\n')


#algorithms = [IndexHash(), IndexSorted(), SuffixArray(), SuffixTree()]
algorithms = [IndexHash()]

tests_dir = Path("Tests/Performance/")
tests_results_dir = Path("Tests/Results/")
test_files = []

for file in os.listdir(tests_dir):
    test_files.append(tests_dir / file)

for test_file_name in test_files:

    test_file = open(test_file_name, 'r')
    lines = test_file.readlines()

    genome = ''.join(map(rstrip, lines[2:]))
    patterns = [x for x in lines[1].rstrip('\n').split(',')]

    index = test_files.index(test_file_name)

    '''
    if len(sys.argv) > 1:
        algorithm_index = int(sys.argv[1])
        print("Selected algorithm index: " + str(algorithm_index))
        algorithms = [algorithms[algorithm_index]]
    else:
        print("Selected all algorithms")
    '''

    for algorithm in algorithms:
        test_results_file_path = tests_results_dir / (algorithm.get_name() + str(index) + ".txt")
        test_results_file = open(test_results_file_path, "w+")
        test_results_file.write(str(benchmark_run(algorithm, genome, patterns, algorithm.get_name(), num_of_repeats)))
