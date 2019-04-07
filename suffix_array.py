from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar
import bisect


class SuffixArray(AlgorithmWithIndexStructure):

    def __bisect_left(self, x, lo=0, hi=None):
        a = self.__suffix_array

        if lo < 0:
            raise ValueError('lo must be non-negative')
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if self.__text[a[mid]:][:len(x)] < x:
                lo = mid + 1
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
            if self.__text[a[mid]:][:len(x)] > x:
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
        self.__suffix_array = []

        init_progress = ProgressBar(len(self.__text), "Adding suffixes...")

        for x in list(reversed(range(len(self.__text)))):
            index = self.__bisect_left(text[x:])
            self.__suffix_array.insert(index, x)
            init_progress.update_progress(len(self.__text) - x)

    def query(self, pattern):
        result_list = []

        if pattern != "":
            leftmost = self.__bisect_left(pattern)
            rightmost = self.__bisect_right(pattern)

            if leftmost < rightmost:
                for offset in self.__suffix_array[leftmost:rightmost]:
                    bisect.insort(result_list, offset)

        return result_list
