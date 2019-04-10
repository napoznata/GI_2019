from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar
from operator import attrgetter

leafEnd = -1


class Node:
    """The Suffix-tree's node."""

    def __init__(self, leaf):
        self.children = {}
        self.leaf = leaf
        self.start = None
        self.end = None
        self.suffixLink = None

    def __eq__(self, node):
        atg = attrgetter('start', 'end')
        return atg(self) == atg(node)

    def __ne__(self, node):
        atg = attrgetter('start', 'end')
        return atg(self) != atg(node)

    def __getattribute__(self, name):
        if name == 'end':
            if self.leaf:
                return leafEnd
        return super(Node, self).__getattribute__(name)


class SuffixTree(AlgorithmWithIndexStructure):

    def init_with_text(self, text):
        self.lastNewNode = None
        self.activeNode = None
        self.activeEdge = -1
        self.activeLength = 0
        self.remainingSuffixCount = 0
        self.rootEnd = None
        self.splitEnd = None
        self.size = -1
        self.root = None
        self._string = text + "$"
        self.build_suffix_tree()

    def query(self, pattern):
        if len(pattern) == 0:
            return []

        self.sub_string = pattern
        self.latest_index = 0
        self.sub_length = len(pattern)

        return self.check()

    def get_name(self):
        return "SuffixTree"

    def __init__(self):
        self._string = ""
        self.lastNewNode = None
        self.activeNode = None
        self.activeEdge = -1
        self.activeLength = 0
        self.remainingSuffixCount = 0
        self.rootEnd = None
        self.splitEnd = None
        self.size = -1
        self.root = None

        self.sub_string = ""
        self.latest_index = 0
        self.sub_length = 0

    @staticmethod
    def edge_length(node):
        return node.end - node.start + 1

    def walk_down(self, current_node):
        length = self.edge_length(current_node)
        if self.activeLength >= length:
            self.activeEdge += length
            self.activeLength -= length
            self.activeNode = current_node
            return True
        return False

    def new_node(self, start, end=None, leaf=False):
        node = Node(leaf)
        node.suffixLink = self.root
        node.start = start
        node.end = end
        return node

    def extend_suffix_tree(self, pos):
        global leafEnd
        leafEnd = pos
        self.remainingSuffixCount += 1
        self.lastNewNode = None
        while self.remainingSuffixCount > 0:
            if self.activeLength == 0:
                self.activeEdge = pos
            if self.activeNode.children.get(self._string[self.activeEdge]) is None:
                self.activeNode.children[self._string[self.activeEdge]] = self.new_node(pos, leaf=True)
                if self.lastNewNode is not None:
                    self.lastNewNode.suffixLink = self.activeNode
                    self.lastNewNode = None
            else:
                _next = self.activeNode.children.get(self._string[self.activeEdge])
                if self.walk_down(_next):
                    continue
                if self._string[_next.start + self.activeLength] == self._string[pos]:
                    if (self.lastNewNode is not None) and (self.activeNode != self.root):
                        self.lastNewNode.suffixLink = self.activeNode
                        self.lastNewNode = None
                    self.activeLength += 1
                    break
                self.splitEnd = _next.start + self.activeLength - 1
                split = self.new_node(_next.start, self.splitEnd)
                self.activeNode.children[self._string[self.activeEdge]] = split
                split.children[self._string[pos]] = self.new_node(pos, leaf=True)
                _next.start += self.activeLength
                split.children[self._string[_next.start]] = _next
                if self.lastNewNode is not None:
                    self.lastNewNode.suffixLink = split
                self.lastNewNode = split
            self.remainingSuffixCount -= 1
            if (self.activeNode == self.root) and (self.activeLength > 0):
                self.activeLength -= 1
                self.activeEdge = pos - self.remainingSuffixCount + 1
            elif self.activeNode != self.root:
                self.activeNode = self.activeNode.suffixLink

    def walk_dfs(self, current, chars_traversed):
        def first_char(el):
            return self._string[el.start]

        start, end = current.start, current.end
        chars_traversed = end - start + 1 + chars_traversed
        yield (self._string[start: end + 1], chars_traversed, current.leaf)

        for node in sorted(current.children.values(), key=first_char):
            if node:
                yield from self.walk_dfs(node, chars_traversed)

    def build_suffix_tree(self):
        self.size = len(self._string)

        self.rootEnd = -1
        self.root = self.new_node(-1, self.rootEnd)
        self.activeNode = self.root

        init_progress = ProgressBar(self.size, "Building suffix tree...")

        for i in (index for index in range(self.size)):
            init_progress.update_progress(i)
            self.extend_suffix_tree(i)

        init_progress.update_progress(self.size)

    def traverse(self, node, sub_string):
        if sub_string:

            item = next(((char, child) for char, child in node.children.items() if sub_string[0] == char), None)

            if item:
                char, child = item
                start, end = child.start, child.end
                if self._string[start: end + 1].startswith(sub_string):
                    return self.find_all_match(child, (end - start + 1) - len(sub_string) + self.sub_length)
                if child.leaf:
                    return []
                else:
                    return self.traverse(child, sub_string[end - start + 1:])
            else:
                return []
        return self.find_all_match(node, len(sub_string))

    def check(self):
        if self.root is None:
            return []
        if not isinstance(self.sub_string, str):
            return []
        if not self.sub_string:
            return []

        return self.traverse(self.root, self.sub_string)

    def find_all_match(self, node, sub_length):

        def inner(sel_node, traversed_edges):
            for char, child in sorted(sel_node.children.items()):
                if child.leaf:
                    yield child.start - traversed_edges
                else:
                    start, end = child.start, child.end
                    sub_length = end - start + 1
                    yield from inner(child, traversed_edges + sub_length)

        if node.leaf:
            first = node.start - (self.sub_length - sub_length)
            result = [first, *inner(node, self.sub_length)]
            result.sort()
            return result
        else:
            result = list(inner(node, sub_length))
            result.sort()
            return result

    def print_dfs(self):
        for sub in self.walk_dfs(self.root, 0):
            print(sub)

    def gen_suffix_array(self):
        array = []
        init_progress = ProgressBar(self.size + 1, "Adding substring indexes...")
        for sub in self.walk_dfs(self.root, 0):
            if sub[2]:
                array.append(self.size - sub[1] + 1)
                init_progress.update_progress(len(array))

        return array
