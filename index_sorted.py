from algorithm import AlgorithmWithIndexStructure


class IndexSorted(AlgorithmWithIndexStructure):
    def get_name(self):
        return "IndexSorted"

    __pattern_len = 5

    def __init__(self):
        self.__text = ""
        self.__index = []

    def init_with_text(self, text):
        self.__text = text
        self.__index = []

        for i in range(len(self.__text) + 1):
            self.__index.append((self.__text[i:i + IndexSorted.__pattern_len], i))  # add <substr, offset> pair
        self.__index.sort()  # sort pairs

    def query(self, pattern):
        if len(pattern) == 0:
            return []

        # include all offsets initially
        results = [x for x in range(0, len(self.__text))]

        for i in range(0, len(pattern), IndexSorted.__pattern_len):
            substring = pattern[i:i + IndexSorted.__pattern_len]

            result_list = []
            found_at = -1
            low = 0
            high = len(self.__index) - 1

            while low <= high:

                mid = low + (high - low) // 2  # Integer division

                if self.__index[mid][0].startswith(substring):
                    found_at = mid + self.__index[mid][0].index(substring)
                    break
                elif substring > self.__index[mid][0]:
                    low = mid + 1
                else:
                    high = mid - 1

            if found_at != -1:
                # Append item found in binary search
                result_list.append(self.__index[found_at][1])

                # Linear search down for the rest
                index_down = found_at - 1
                while index_down > 0 and self.__index[index_down][0].startswith(substring):
                    result_list.append(self.__index[index_down][1])
                    index_down -= 1

                # Linear search up for the rest
                index_up = found_at + 1
                while index_up < len(self.__index) and self.__index[index_up][0].startswith(substring):
                    result_list.append(self.__index[index_up][1])
                    index_up += 1

            results = list(filter(lambda x: (x + i) in result_list, results))
            # return if there are no results
            if len(results) == 0:
                break

        return sorted(results)
