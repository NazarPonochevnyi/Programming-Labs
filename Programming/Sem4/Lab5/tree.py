# Tree implementation in Python

from graphviz import Digraph


class BinaryTree:
    def __init__(self, value=None):
        self.data = value
        self.left = None
        self.right = None

    def to_dict(self, result):
        if self.data is None:
            return {}
        result[self.data] = [None, None]
        if self.left:
            result[self.data][0] = self.left.data
            self.left.to_dict(result)
        if self.right:
            result[self.data][1] = self.right.data
            self.right.to_dict(result)
        return result

    def __str__(self):
        return str(self.to_dict({}))

    def display(self):
        tree = self.to_dict({})
        fig = Digraph(format="png",
                      graph_attr={'ordering': 'out',
                                  'nodesep': '0.4',
                                  'ranksep': '0.5',
                                  'margin': '0.1'},
                      edge_attr={'arrowsize': '0.8'})
        temp_nodes = {n: 0 for n in tree}
        for parent in tree:
            for child in tree[parent]:
                if child:
                    fig.edge(str(parent), str(child))
                else:
                    temp_nodes[parent] += 1
                    temp_node = f"{parent}t{temp_nodes[parent]}"
                    fig.node(temp_node, style='invis')
                    fig.edge(str(parent), temp_node, style='invis')
        fig.view()
        return tree

    def insert(self, value):
        if self.data:
            if value < self.data:
                if self.left is None:
                    self.left = BinaryTree(value)
                else:
                    self.left.insert(value)
            else:
                if self.right is None:
                    self.right = BinaryTree(value)
                else:
                    self.right.insert(value)
        else:
            self.data = value

    def remove(self, value):
        if self.data:
            if value < self.data:
                if self.left is None:
                    raise Exception("element not found")
                if self.left.data == value:
                    temp = self.left
                    if temp.left is None and temp.right is None:
                        self.left = None
                        return temp
                return self.left.remove(value)
            elif value > self.data:
                if self.right is None:
                    raise Exception("element not found")
                if self.right.data == value:
                    temp = self.right
                    if temp.left is None and temp.right is None:
                        self.right = None
                        return temp
                return self.right.remove(value)
            else:
                temp = self.data
                if self.left is None:
                    self.data = self.right.data
                    self.right = None
                    return temp
                elif self.right is None:
                    self.data = self.left.data
                    self.left = None
                    return temp
                min_value = self.right.min()
                self.data = min_value
                if self.right.data == min_value:
                    self.right = None
                    return temp
                self.right.remove(min_value)
                return temp
        else:
            raise Exception("binary tree is empty")

    def search(self, value):
        if self.data:
            if value < self.data:
                if self.left is None:
                    return False
                return self.left.search(value)
            elif value > self.data:
                if self.right is None:
                    return False
                return self.right.search(value)
            return True
        else:
            raise Exception("binary tree is empty")

    def min(self):
        if self.data:
            if self.left is None:
                return self.data
            return self.left.min()
        else:
            raise Exception("binary tree is empty")

    def max(self):
        if self.data:
            if self.right is None:
                return self.data
            return self.right.max()
        else:
            raise Exception("binary tree is empty")


def is_float(str):
    try:
        float(str)
    except ValueError:
        return False
    return True


def main():
    tree = BinaryTree()
    gr = "\n[t]ree, [i]nsert, [r]emove, " \
        + "[s]earch, [min], [max], [d]isplay, [q]uit: "
    while True:
        command = input(gr).strip().split()
        if len(command) == 0 or \
                (len(command) == 2 and not is_float(command[1])):
            print("Wrong command")
            continue
        if command[0] in ('t', 'tree'):
            print(tree)
        elif command[0] in ('i', 'insert'):
            tree.insert(float(command[1]))
        elif command[0] in ('r', 'remove'):
            print(tree.remove(float(command[1])))
        elif command[0] in ('s', 'search'):
            print(tree.search(float(command[1])))
        elif command[0] == 'min':
            print(tree.min())
        elif command[0] == 'max':
            print(tree.max())
        elif command[0] in ('d', 'display'):
            print(tree.display())
        elif command[0] in ('q', 'quit', 'exit'):
            break
        else:
            print("Command not found!")


if __name__ == "__main__":
    main()
