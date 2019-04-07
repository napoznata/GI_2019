from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar


class SuffixTree(AlgorithmWithIndexStructure):

    def get_name(self):
        return "SuffixTree"

    class Node(object):
        def __init__(self, lab, offset=-1):
            self.lab = lab  # label on path leading to this node
            self.offset = offset  # suffix offset in text
            self.out = {}  # outgoing edges; maps characters to nodes

        def get_leaves_offsets(self):
            if self.offset != -1:
                # node is a leaf, returns suffix offset
                return [self.offset]
            else:
                # node is internal, propagates function call further down the tree
                offsets = [el for c in self.out for el in self.out[c].get_leaves_offsets()]
                offsets.sort()
                return offsets

    def __init__(self):
        self.__root = self.Node(None)
        self.__text = ""

    def init_with_text(self, text):
        self.__text = text + '$'

        init_progress = ProgressBar(len(self.__text), "Adding suffixes to tree...")

        self.__root = self.Node(None)
        self.__root.out[self.__text[0]] = self.Node(self.__text, 0)  # trie for just longest suf
        # add the rest of the suffixes, from longest to shortest
        for i in range(1, len(self.__text)):
            # start at root; we’ll walk down as far as we can go
            cur = self.__root
            j = i
            while j < len(self.__text):
                if self.__text[j] in cur.out:
                    child = cur.out[self.__text[j]]
                    lab = child.lab
                    # Walk along edge until we exhaust edge label or
                    # until we mismatch
                    k = j + 1
                    while k - j < len(lab) and self.__text[k] == lab[k - j]:
                        k += 1
                    if k - j == len(lab):
                        cur = child  # we exhausted the edge
                        j = k
                    else:
                        # we fell off in middle of edge
                        c_exist, c_new = lab[k - j], self.__text[k]
                        # create “mid”: new node bisecting edge
                        mid = self.Node(lab[:k - j])
                        mid.out[c_new] = self.Node(self.__text[k:], i)
                        # original child becomes mid’s child
                        mid.out[c_exist] = child
                        # original child’s label is curtailed
                        child.lab = lab[k - j:]
                        # mid becomes new child of original parent
                        cur.out[self.__text[j]] = mid
                else:
                    # Fell off tree at a node: make new edge hanging off it
                    cur.out[self.__text[j]] = self.Node(self.__text[j:], i)
                init_progress.update_progress(i)

        init_progress.update_progress(len(self.__text))

    def follow_path(self, pattern):
        cur = self.__root
        i = 0
        path_progress = ProgressBar(len(pattern), "Traversing suffix tree...")
        while i < len(pattern):
            path_progress.update_progress(i)
            c = pattern[i]
            if c not in cur.out:
                path_progress.update_progress(len(pattern))
                return None  # fell off at a node
            child = cur.out[pattern[i]]
            lab = child.lab
            j = i + 1
            while j - i < len(lab) and j < len(pattern) and pattern[j] == lab[j - i]:
                j += 1
            if j - i == len(lab):
                cur = child  # exhausted edge
                i = j
                path_progress.update_progress(i)
            elif j == len(pattern):
                path_progress.update_progress(len(pattern))
                return child  # exhausted query string in middle of edge
            else:
                path_progress.update_progress(len(pattern))
                return None  # fell off in the middle of the edge
        path_progress.update_progress(len(pattern))
        return cur  # exhausted query string at internal node

    def query(self, pattern):
        if len(pattern) == 0:
            return []

        node = self.follow_path(pattern)
        result = node.get_leaves_offsets() if node is not None else []
        return result
