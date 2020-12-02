from typing import Optional, Any, List, Dict, Tuple, Union
import itertools


class Node():
    """One Node of a Trie"""

    def __init__(self) -> None:
        self.children: Dict[str, Node] = {}
        self.value: Optional[Any] = None


class ATB():
    """Trie structure, with functions for insertion, retrieval, and deletion."""

    def __init__(self):
        self.root = Node()

    def search(self, key: str) -> Optional[Any]:
        """Alias for find() function.

        Find `key` in alphadict; return `key`'s value"""
        return self.find(key)

    def find(self, key: str) -> Optional[Any]:
        '''Find `key` in alphadict; return `key`'s value.'''
        node = self.root
        for char in key:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.value

    def insert(self, key: str, value: Any) -> None:
        """Insert key/value pair into trie, iteratively."""
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]

        node.value = value

    def delete(self, key: str) -> bool:
        '''delete `key` from the trie, recursively, if `key` exists in trie.'''

        def _delete(node: Node, key: str, d: int) -> bool:
            '''clear the node corresponding to key[d], and delete the child 
            key[d+1] if that subtrie is completely empty, and return whether 
            `node` has been cleared.'''
            if d == len(key):
                node.value = None
            else:
                c = key[d]
                if c in node.children and _delete(node.children[c], key, d+1):
                    del node.children[c]

            return node.value is None and len(node.children == 0)

        return _delete(self.root, key, 0)

    def keys_with_prefix(self, prefix: str) -> List[str]:
        '''Check to see if string `prefix` is a prefix for any existing words in the
        trie. If it is, return a list of all words in the trie that start with `prefix`.

        Beware using this function on single characters; the resulting list can be 
        massive and slow down the overall program significantly.'''

        def _collect(x: Optional[Node], prefix: List[str], results: List[str]) -> None:
            """append keys under node `x` matching the given prefix to `results`."""
            if x is None:
                return
            if x.value is not None:
                prefix_str = "".join(prefix)
                results.append(prefix_str)
            for c in x.children:
                prefix.append(c)
                _collect(x.children[c], prefix, results)
                del prefix[-1]

        def _get_node(node: Node, key: str) -> Optional[Node]:
            '''Find a node using `key`'''
            for char in key:
                if char in node.children:
                    node = node.children[char]

                else:
                    return None
            return node

        root = self.root
        results: List[str] = []
        x = _get_node(root, prefix)
        _collect(x, list(prefix), results)

        return results

    def get_matches(self, s: str) -> List[Any]:
        '''Search alphaDict dictionary tree for all possible word matches in string s.

        Returns a list composed of tuples of the matching term, and the index range in 
        `s` where that term was found, e.g. (term, range(start_index, stop_index))'''

        sets = []
        all_words = []

        for i in range(len(s)):
            for j in range(len(s)+1):
                proto = s[i:j]  # make a substring
                result = self.find(proto)  # check if it's in the trie
                prefix = self.keys_with_prefix(  # check if it's the prefix to something
                    proto) if len(proto) > 1 else [proto]  # if it's at least 2 chars long

                if result:  # if it's a word in the trie
                    # put the potential match in sets
                    sets.append([proto, range(i, j)])
                else:
                    if prefix:  # otherwise if it's part of a trie branch
                        continue
                    else:
                        # else append the sets to all words
                        all_words.append(sets)
                        sets = []  # and clear working sets
                        break
        # handle unappended sets
        if sets:
            all_words.append(sets)

        return all_words

    def greedy_segment(self, s: str) -> List[str]:
        """
        Segment string `s` into a list of individual words.
        """
        def _group_matches(matches):
            """
            group matches into chunks of overlapping indices
            """
            start, end = 0, 1
            chunks = []
            curr_chunk = []
            curr_chunk.append(matches[0][0])  # append the first word
            for group in matches:
                for tup in group:
                    word, ind = tup

                    # if the word starts the same but is longer than we're tracking
                    if ind[0] == start and ind[-1]+1 > end:
                        end = ind[-1]+1  # increment end
                        curr_chunk.append(tup)  # add to working chunk

                    # if the word ends the same place but starts further than we're tracking
                    elif ind[0] > start and ind[-1]+1 == end:
                        start = ind[0]  # increment start
                        curr_chunk.append(tup)  # add to working chunk

                    # if the word begins where our last word ended
                    elif ind[0] == end:
                        start = ind[0]  # increment start
                        end = ind[0]+1  # increment end
                        # add working chunk to finished chunks
                        chunks.append(curr_chunk)
                        curr_chunk = []  # clear working chunk
                        # put our current word into the new working chunk
                        curr_chunk.append(tup)
            if curr_chunk:  # if any is leftover
                # put the working chunk into finished chunks
                chunks.append(curr_chunk)

            return chunks  # return finished chunks

        return _group_matches(self.get_matches(s))

    def _flatten(self, s: str) -> List[Any]:
        """
        Return a flat list of `[match, range(start_index, stop_index)]` of all matches
        found in the string `s`.
        """
        return list(itertools.chain(*self.get_matches(s)))

    def dijkstra_segment(self, s:str) -> List[str]:
        '''Use Dijkstra's algorithm to traverse a weighted graph of the dictionary matches in string `s`.
        This method prefers word length, minimizing the number of single character words in a segmented sentence.'''
        pass