import os
from pathlib import Path
from index_hash import IndexHash
from index_sorted import IndexSorted
from suffix_array import SuffixArray
from suffix_tree import SuffixTree
from config import *

unit_tests_dir = Path(unit_tests_dir_path)


class UnitTestResult(object):

    PASSED = 0
    FAILED = -1

    __result_str = dict()
    __result_str[PASSED] = "Passed"
    __result_str[FAILED] = "Failed"

    def __init__(self, result, name, message):
        self.__message = message
        self.__result = result
        self.__name = name

    def get_name(self):
        return self.__name

    def get_result(self):
        return self.__result

    def get_description(self):
        return self.__name + ": " + self.__result_str[self.__result] + self.__message


def run_algorithm_tests(algorithm):

    tests_dir = unit_tests_dir
    test_files = []
    results = []

    for file in os.listdir(tests_dir):
        test_files.append(tests_dir / file)

    for test_file_name in test_files:

        test_file = open(test_file_name, 'r')
        lines = test_file.readlines()

        name = lines[0].rstrip('\n')
        genome = lines[1].rstrip('\n')

        algorithm.init_with_text(genome)

        for pattern_line in lines[2:]:
            line_parts = pattern_line.rstrip('\n').split(':')

            pattern = line_parts[0]
            match_indexes = list(map(int, line_parts[1].split(','))) if len(line_parts[1]) > 0 else []

            algorithm_result = algorithm.query(pattern)

            message = ""

            if match_indexes != algorithm_result:
                result = UnitTestResult.FAILED
                message = ' (pattern: \"' + pattern + '\", missed indexes: ' \
                          + str(sorted(list(set(match_indexes).symmetric_difference(algorithm_result)))) + ")"
            else:
                result = UnitTestResult.PASSED

            results.append(UnitTestResult(result, name, message))

    return results


def print_test_results(results):
    for result in results:
        print(result.get_description())


algorithms = [IndexHash(), IndexSorted(), SuffixArray(), SuffixTree()]
for algorithm in algorithms:
    print(algorithm.get_name())
    test_results = run_algorithm_tests(algorithm)
    print_test_results(test_results)
