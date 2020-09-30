from typing import Optional, Any, List, Dict

class Node():
    def __init__(self) -> None:
        self.children: Dict[str, Node] = {}
        self.value: Optional[Any] = None



class ATB():
    
    def __init__(self):
        self.root = Node()

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


    def getMatches(self, s: str) -> List[Any]:
        '''Search alphaDict dictionary tree for all possible word matches in string s.
        
        Returns a list composed of tuples of the matching term, and the index range in 
        `s` where that term was found, e.g. (term, range(start_index, stop_index))'''

        sets = []
        all_words = []

        for i in range(len(s)):
            for j in range(len(s)+1):
                proto = s[i:j]
                result = self.find(proto)
                prefix = self.keys_with_prefix(proto) if len(proto) > 1 else [proto]

                if result:
                    sets.append((proto, range(i, j)))
                else:
                    if prefix:
                        continue
                    else:
                        all_words.append(tuple(sets))
                        sets.clear()
                        break
        if sets:
            all_words.append(tuple(sets))

        return(all_words)
