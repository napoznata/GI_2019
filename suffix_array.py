from algorithm import AlgorithmWithIndexStructure


class SuffixArray(AlgorithmWithIndexStructure):

    def get_name(self):
        return "SuffixArray"

    def __init__(self):
        self.__suffix_array = []
        self.__text = ""

    def init_with_text(self, text):
        self.__text = text

        # Suffix array is a list of tuples
        self.__suffix_array = []

        for i in reversed(range(len(self.__text))):
            # Add a tuple (suffix,index)
            self.__suffix_array.append((self.__text[i:], i))

        # Sort by suffix
        self.__suffix_array.sort(key=lambda t: t[0])

    def query(self, pattern):
        result_list = []

        if pattern != "":

            found_at = -1
            low = 0
            high = len(self.__suffix_array) - 1

            while low <= high:

                mid = low + (high - low) // 2  # Integer division

                if self.__suffix_array[mid][0].startswith(pattern):
                    found_at = mid
                    break
                elif pattern > self.__suffix_array[mid][0]:
                    low = mid + 1
                else:
                    high = mid - 1

            if found_at != -1:
                # Append item found in binary search
                result_list.append(self.__suffix_array[found_at][1])

                # Linear search down for the rest
                index_down = found_at -1
                while index_down > 0 and self.__suffix_array[index_down][0].startswith(pattern):
                    result_list.append(self.__suffix_array[index_down][1])
                    index_down -= 1

                # Linear search up for the rest
                index_up = found_at + 1
                while index_up < len(self.__suffix_array) and self.__suffix_array[index_up][0].startswith(pattern):
                    result_list.append(self.__suffix_array[index_up][1])
                    index_up += 1

        return sorted(result_list)
