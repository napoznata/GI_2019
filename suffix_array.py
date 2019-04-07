from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar


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

    def __compare_suffix(self, index1, index2):

        len_text = len(self.__text)

        if index1 != index2:

            while self.__text[index1] == self.__text[index2]:
                index1 += 1
                index2 += 1

                if index1 == len_text or index2 == len_text:
                    len_suffix1 = len_text - index1
                    len_suffix2 = len_text - index2

                    if len_suffix1 > len_suffix2:
                        return 1
                    else:
                        return -1

            if self.__text[index1] > self.__text[index2]:
                return 1
            else:
                return -1
        else:
            return 0

    def get_name(self):
        return "SuffixArray"

    def __init__(self):
        self.__suffix_array = []
        self.__text = ""

    def init_with_text(self, text):
        self.__text = text
        self.__suffix_array = []

        init_progress = ProgressBar(len(self.__text))
        ProgressBar.print_message("Adding suffixes...")

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
                result_list += list(self.__suffix_array[leftmost:rightmost])

        result_list.sort()
        return result_list
