from algorithm import AlgorithmWithIndexStructure
from benchmark import ProgressBar
from operator import attrgetter

leafEnd = -1


class Node:
    """The Suffix-tree's node."""

    def __init__(self, leaf):
        self.children = {}
        # for leaf nodes, it stores the index of suffix for
        # the path  from root to leaf"""
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
        """Initiate the tree."""
        self._string = ""
        self.lastNewNode = None
        self.activeNode = None
        """activeEdge is represeted as input string character
          index (not the character itself)"""
        self.activeEdge = -1
        self.activeLength = 0
        # remainingSuffixCount tells how many suffixes yet to
        # be added in tree
        self.remainingSuffixCount = 0
        self.rootEnd = None
        self.splitEnd = None
        self.size = -1  # Length of input string
        self.root = None

        self.sub_string = ""
        self.latest_index = 0
        self.sub_length = 0

    @staticmethod
    def edge_length(node):
        return node.end - node.start + 1

    def walk_down(self, current_node):
        """Walk down from current node.
        activePoint change for walk down (APCFWD) using
        Skip/Count Trick  (Trick 1). If activeLength is greater
        than current edge length, set next  internal node as
        activeNode and adjust activeEdge and activeLength
        accordingly to represent same activePoint.
        """
        length = self.edge_length(current_node)
        if self.activeLength >= length:
            self.activeEdge += length
            self.activeLength -= length
            self.activeNode = current_node
            return True
        return False

    def new_node(self, start, end=None, leaf=False):
        """For root node, suffixLink will be set to NULL
        For internal nodes, suffixLink will be set to root
        by default in  current extension and may change in
        next extension"""
        node = Node(leaf)
        node.suffixLink = self.root
        node.start = start
        node.end = end
        return node

    def extend_suffix_tree(self, pos):
        global leafEnd
        """Extension Rule 1, this takes care of extending all
        leaves created so far in tree"""
        leafEnd = pos
        """Increment remainingSuffixCount indicating that a
        new suffix added to the list of suffixes yet to be
        added in tree"""
        self.remainingSuffixCount += 1
        """set lastNewNode to None while starting a new phase,
         indicating there is no internal node waiting for
         it's suffix link reset in current phase"""
        self.lastNewNode = None
        # Add all suffixes (yet to be added) one by one in tree
        while self.remainingSuffixCount > 0:
            if self.activeLength == 0:
                self.activeEdge = pos  # APCFALZ
            #  There is no outgoing edge starting with
            #  activeEdge from activeNode
            if self.activeNode.children.get(self._string[self.activeEdge]) is None:
                # Extension Rule 2 (A new leaf edge gets created)
                self.activeNode.children[self._string[self.activeEdge]] = self.new_node(pos, leaf=True)
                """A new leaf edge is created in above line starting
                 from  an existng node (the current activeNode), and
                 if there is any internal node waiting for it's suffix
                 link get reset, point the suffix link from that last
                 internal node to current activeNode. Then set lastNewNode
                 to None indicating no more node waiting for suffix link
                 reset."""
                if self.lastNewNode is not None:
                    self.lastNewNode.suffixLink = self.activeNode
                    self.lastNewNode = None
            #  There is an outgoing edge starting with activeEdge
            #  from activeNode
            else:
                #  Get the next node at the end of edge starting
                #  with activeEdge
                _next = self.activeNode.children.get(self._string[self.activeEdge])
                if self.walk_down(_next):  # Do walkdown
                    # Start from _next node (the new activeNode)
                    continue
                """Extension Rule 3 (current character being processed
                  is already on the edge)"""
                if self._string[_next.start + self.activeLength] == self._string[pos]:
                    # If a newly created node waiting for it's
                    # suffix link to be set, then set suffix link
                    # of that waiting node to curent. active node
                    if (self.lastNewNode is not None) and (self.activeNode != self.root):
                        self.lastNewNode.suffixLink = self.activeNode
                        self.lastNewNode = None
                    # APCFER3
                    self.activeLength += 1
                    """STOP all further processing in this phase
                    and move on to _next phase"""
                    break
                """We will be here when activePoint is in middle of
                  the edge being traversed and current character
                  being processed is not  on the edge (we fall off
                  the tree). In this case, we add a new internal node
                  and a new leaf edge going out of that new node. This
                  is Extension Rule 2, where a new leaf edge and a new
                internal node get created"""
                self.splitEnd = _next.start + self.activeLength - 1
                # New internal node
                split = self.new_node(_next.start, self.splitEnd)
                self.activeNode.children[self._string[self.activeEdge]] = split
                # New leaf coming out of new internal node
                split.children[self._string[pos]] = self.new_node(pos, leaf=True)
                _next.start += self.activeLength
                split.children[self._string[_next.start]] = _next
                """We got a new internal node here. If there is any
                  internal node created in last extensions of same
                  phase which is still waiting for it's suffix link
                  reset, do it now."""
                if self.lastNewNode is not None:
                    # suffixLink of lastNewNode points to current newly
                    # created internal node
                    self.lastNewNode.suffixLink = split
                """Make the current newly created internal node waiting
                  for it's suffix link reset (which is pointing to self.root
                  at present). If we come across any other internal node
                  (existing or newly created) in next extension of same
                  phase, when a new leaf edge gets added (i.e. when
                  Extension Rule 2 applies is any of the next extension
                  of same phase) at that point, suffixLink of this node
                  will point to that internal node."""
                self.lastNewNode = split
            """One suffix got added in tree, decrement the count of
               suffixes yet to be added."""
            self.remainingSuffixCount -= 1
            if (self.activeNode == self.root) and (self.activeLength > 0):  # APCFER2C1
                self.activeLength -= 1
                self.activeEdge = pos - self.remainingSuffixCount + 1
            elif self.activeNode != self.root:  # APCFER2C2
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

        """Root is a special node with start and end indices as -1,
        as it has no parent from where an edge comes to root"""
        self.rootEnd = -1
        self.root = self.new_node(-1, self.rootEnd)
        self.activeNode = self.root  # First activeNode will be root

        init_progress = ProgressBar(self.size, "Building suffix tree...")

        for i in (index for index in range(self.size)):
            init_progress.update_progress(i)
            self.extend_suffix_tree(i)

        init_progress.update_progress(self.size)

    def traverse(self, node, sub_string):
        if sub_string:
            # Since each child starts with a unique character we will pursue the process for the child that sub-string
            # Starts with the first character of this edge
            item = next(((char, child) for char, child in node.children.items() if sub_string[0] == char), None)

            if item:
                char, child = item
                start, end = child.start, child.end
                # If the edge is equal with sub-string returns the index
                if self._string[start: end + 1].startswith(sub_string):
                    return self.find_all_match(child, (end - start + 1) - len(sub_string) + self.sub_length)
                # sub-string starts with the frist character of our edge but is not equal with it
                # So call the travese for the rest of sub-string (from the lenght of previous edge)
                if child.leaf:
                    return []
                else:
                    return self.traverse(child, sub_string[end - start + 1:])
            else:
                # At this level there were no edge that sub-string starts with its leading character.
                return []
        return self.find_all_match(node, len(sub_string))

    def check(self):
        if self.root is None:
            return []
        if not isinstance(self.sub_string, str):
            return []
        if not self.sub_string:
            # Every string starts with an empty string
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
