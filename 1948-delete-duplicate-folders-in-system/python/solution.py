from collections import defaultdict
from typing import List

class Node:
    __slots__ = ('children', 'sig', 'deleted', 'name')
    def __init__(self, name: str = ''):
        self.children: dict[str, Node] = {}
        self.sig: str = ''
        self.deleted: bool = False
        self.name = name

class Solution:
    def deleteDuplicateFolder(self, paths: List[List[str]]) -> List[List[str]]:
        root = Node()
        for p in paths:
            n = root
            for part in p:
                n = n.children.setdefault(part, Node(part))
        groups: dict[str, list[Node]] = defaultdict(list)
        def hash_node(n: Node) -> str:
            if not n.children:
                return ''
            parts = []
            for k in sorted(n.children):
                parts.append(k + '(' + hash_node(n.children[k]) + ')')
            n.sig = ''.join(parts)
            groups[n.sig].append(n)
            return n.sig
        hash_node(root)
        for sig, nodes in groups.items():
            if len(nodes) > 1 and sig:
                for n in nodes:
                    n.deleted = True
        out: list[list[str]] = []
        def emit(n: Node, path: list[str]) -> None:
            for k in sorted(n.children):
                child = n.children[k]
                if child.deleted:
                    continue
                path.append(k)
                out.append(path[:])
                emit(child, path)
                path.pop()
        emit(root, [])
        return out
