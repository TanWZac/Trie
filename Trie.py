
class Node:

    def __init__(self,item=None, count=0, prefix=0, counter=1, length=0):
        """
        :param item: allocate the alphabet
        :param count: count the string frequency
        :param prefix: count the prefix frequency
        :param counter: count the distinct string
        :param length: count the length of each string
        this class will create the node
        time complexity: O(1) where initialising the content
        """
        self.item = item
        self.count = count
        self.prefix = prefix
        self.next = [None] * 27
        self.counter = counter
        self.length = length


class Trie:

    def __init__(self, text):
        """
        :param text: the text given
        time complexity: O(text), where text is the given text
        """
        self.root = self.get_next()
        for i in range(len(text)):
            self.insert(text[i])

    def get_next(self):
        """
        create each node
        time complexity: O(1) calling the node class
        :return:
        """
        return Node()

    def insert(self, string):
        """
        :param string: every element in the text
        :return: None
        time complexity: O(string), where string is the length of string
        """
        node = self.root        # start node
        node.prefix += 1        # begin count the prefix
        for i in string:        # for each individual element in the string
            for j in i:
                index = ord(j) - ord('a') + 1       # allocate in the particular index
                if node.next[index] == None:        # if the current node is None:
                    node.next[index] = self.get_next()      # create the node
                node = node.next[index]             # go down the trie
                node.item = j                       # put the item in
                node.prefix += 1                    # increment the prefix
        node.count += 1                             # increment the count
        if len(string) == node.length:              # find is the word repeated
            node.counter += 1                       # if repeated then increment the counter
        node.length = len(string)                   # put the length of the string
        node.next[0] = self.get_next()              # this is to place the end node
        node = node.next[0]
        node.item = '$'

    def string_freq(self, query_str):
        """
        :param query_str: query string
        :return: number of elements of the text which are exactly query_string
        time complexity: O(q) where q is the length of query_str
        """
        node = self.root                    # start node
        counter = 0                         # initialize the counter
        for i in query_str:                 # loop in query string
            index = ord(i) - ord('a') + 1   # accessing using index
            if node.next[index] is not None:    # if the current index has the address
                counter += 1                # increment counter
                node = node.next[index]     # then go down the trie
        if len(query_str) == counter:       # compare the counter with the length of query string
            return node.count               # if all element are met then return count
        return 0                            # else return 0

    def prefix_freq(self, query_str):
        """
        :param query_str: query string
        :return: number of words in the text which have query_str as a prefix
        time complexity: O(q) where q is the length of query_str
        """
        node = self.root                    # start node
        counter = 0                         # initialize the counter
        for i in query_str:                 # loop in query string
            index = ord(i) - ord('a') + 1   # accessing using index
            if node.next[index]:            # if the current index has address in it
                counter += 1                # increment the counter
                node = node.next[index]     # then go down the trie
        if len(query_str) == counter:       # compare the counter with the length of query string
            return node.prefix              # if all element are met then return count
        return 0                            # eles return 0

    def wildcard_prefix_freq(self, query_str):
        """
        :param query_str: query string
        :return: a list containing all the strings which have a prex which matches query_str.
        time complexity: O(q+T) where q is the query string and T traversal the whole trie.
        """
        output = []                         # output array
        out = []                            # out array
        char = ""                           # character that has been reached
        node = self.root                    # start node
        counter = 0                         # counter

        def find(node, cur=""):
            """
            recursive function
            :param node: the start node
            :param cur: the string that has been taken
            :return: output of all prefix element from the start node
            time complexity: O(T) where T is the time taken to traverse the trie
            """
            cur = "".join([cur, node.item])     # add the element in the cur
            if node.next[0] != None:            # compare that if the node is the last node
                str = "".join([char, cur])      # concatenate the string
                for _ in range(node.counter):   # loop in constant time
                    output.append(str)          # append the str to the output
            for p in range(1, len(node.next)):  # continue to find the possible node
                if node.next[p] != None:        # if the current node has the address
                    current = node.next[p]      # then go down the trie
                    find(current, cur)          # call the recursive function

        for i in query_str:                     # loop in query string
            if i == '?':                        # if the current pointer is '?'
                counter += 1                    # increment counter
                if counter > 1:                 # if the counter is greater than 1
                    if len(char) != counter-1:  # compare if the len(character we got) and the counter - 1
                        return output           # return the output, as the string isn't in the trie
                for k in range(1, len(node.next)):      # find all possible node below the trie
                    if node.next[k] != None:            # when the accessing index is not None
                        find(node.next[k])              # call find function
            else:
                counter += 1                    # increment counter
                if len(output) != 0 and counter == 2:    # if the output isn't empty and the counter is exactly 2
                    for l in output:                     # loop in output
                        if l[1:len(query_str)] == query_str[1:]:    # except 1st string, if the string is the same
                            if len(l) >= len(query_str):            # compare if the length is greater or equal to query
                                out.append(l)                       # append the str to out
                    return out                  # return out
                elif len(output) != 0 and counter > 2:    # if the output isn't empty and the counter is greater than 2
                    for t in output:                      # loop in output
                        if t[counter-1:len(query_str)] == query_str[counter-1:]: # after '?', if output string equals to query
                            if len(t) >= len(query_str):            # compare if the length is greater or equal to query
                                out.append(t)                       # append the str to out
                    return out                  # return out
                else:
                    index = ord(i) - ord('a') + 1          # find the index
                    if node.next[index] is not None:       # if the index has the address of the node
                        node = node.next[index]            # go down the trie
                        char = "".join([char, node.item])  # concatenate the string
        return output                           # return the output


if __name__ == '__main__':
    text = ['aa', 'aab', 'aaab', 'abaa', 'aa', 'abba', 'aaba', 'aaa', 'aa', 'aaab','abbb', 'baaa', 'baa', 'bba', 'bbab']

