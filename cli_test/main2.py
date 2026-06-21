from flare import *

node = storage.fs.walk.input
stack = storage.args.input


class Node:
    def __init__(self, name, type, parent=storage.fs.root):
        parent.child.append({})
        parent.child[-1].name = name
        parent.child[-1].type = type

        self._name = name
        self.parent = parent
        self.type = type

        if type == "dir":
            self.node().child = []
            self.child = self.node().child

    def node(self):
        return self.parent.child[{"name": self._name}]

    def remove(self):
        self.node.remove()

    def rename(self, new_name, type=None):
        if type is None:
            type = self.type
        self.parent.child[{"name": self._name}].name = new_name
        self._name = new_name

    def walk(self):
        walk(self.child)


@export("fs/walk")
def walk(children: nbt):
    for item in children:
        print(item.name, item.type)

        if item.child:
            walk(item.child)


root = Node("root", "dir")
pack = Node("pack.mcmeta", "txt", root)
pack = Node("pack.ajmeta", "txt", root)
pack_md = Node("README.md", "md", root)
data = Node("data", "dir", root)
minecraft = Node("minecraft", "dir", data)
tags = Node("tags", "dir", minecraft)
function_tag = Node("function", "dir", tags)
tick_function_tag = Node("tick.json", "json", function_tag)
load_function_tag = Node("load.json", "json", function_tag)
dpi_namespace = Node("dpi", "dir", data)
functions = Node("function", "dir", dpi_namespace)
tick = Node("tick.mcfunction", "mcf", functions)
load = Node("load.mcfunction", "mcf", functions)

root.walk()
