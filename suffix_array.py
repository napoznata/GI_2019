from unit_test import *
from main import AlgorithmWithIndexStructure


class SuffixArray(AlgorithmWithIndexStructure):

    def __init__(self):
        self.__suffix_array = []
        self.__text = ""

    def initWithText(self):
        # Suffix array is a list of tuples
        self.__suffix_array = []

        for i in reversed(range(len(self.__text))):
            # Add a tuple (suffix,index)
            self.__suffix_array.append((self.__text[i:], i))


        # Sort by suffix
        self.__suffix_array.sort(key=lambda t: t[0])

    def query(self, text, pattern):
        self.__text = text
        self.initWithText()

        low = 0
        high = len(self.__suffix_array) - 1

        while low <= high:

            mid = low + (high - low) // 2  # Integer division

            if self.__suffix_array[mid][0].startswith(pattern):
                return self.__suffix_array[mid][1]
            elif pattern > self.__suffix_array[mid][0]:
                low = mid + 1
            else:
                high = mid - 1

        return -1




obj = SuffixArray()
print(obj.query("banana","nan"))

# Run tests
#test_results = run_algorithm_tests(SuffixArray())
#print_test_results(test_results)