from algorithm import AlgorithmWithIndexStructure
import bisect


class SuffixArray(AlgorithmWithIndexStructure):

    def __bisect_left(self, x, lo=0, hi=None):
        a = self.__suffix_array

        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo+hi)//2
            if self.__text[a[mid]:] < x:
                lo = mid+1
            else:
                hi = mid
        return lo

    def __bisect_right(self, x, lo=0, hi=None):
        a = self.__suffix_array

        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.__text[a[mid]:] > x:
                hi = mid
            else:
                lo = mid + 1
        return lo

    def get_name(self):
        return "SuffixArray"

    def __init__(self):
        self.__suffix_array = []
        self.__text = ""

    def init_with_text(self, text):
        self.__text = text
        self.__suffix_array = list(reversed(range(len(self.__text))))

        # Sort by suffix
        self.__suffix_array.sort(key=lambda index: self.__text[index:])

        self.__test_array = []
        for index in self.__suffix_array:
            self.__test_array.append((self.__text[index:], index))

    def query(self, pattern):
        result_list = []

        if pattern != "":

                leftmost = self.__bisect_left(pattern)
                rightmost = self.__bisect_right(pattern)

                if leftmost <= rightmost:
                    result_list += list(x[1] for x in self.__suffix_array[leftmost:rightmost])

        return sorted(result_list)
