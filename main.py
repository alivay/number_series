import copy

DEBUG = 0
SEARCH_DEBT = 10

OPERATION_PLACE_HOLDER = 0
OPERATION_VALUE_1 = 1
OPERATION_VALUE_N = 2
OPERATION_ADD = 3
OPERATION_SUB = 4
OPERATION_MUL = 5
OPERATION_DIV = 6
OPERATION_POWER = 7

LEFT_OPERAND = 0
RIGHT_OPERAND = 1


class Function:
    def __init__(self):
        self.left = None
        self.right = None
        self.operand = None

    def __str__(self):
        if self.operand is None:
            return "PH"
        elif self.operand == OPERATION_VALUE_1:
            return "1"
        elif self.operand == OPERATION_VALUE_N:
            return "n"
        elif self.operand == OPERATION_ADD:
            return "(" + str(self.left) + "+" + str(self.right) + ")"
        elif self.operand == OPERATION_SUB:
            return "(" + str(self.left) + "-" + str(self.right) + ")"
        elif self.operand == OPERATION_MUL:
            return "(" + str(self.left) + "*" + str(self.right) + ")"
        elif self.operand == OPERATION_DIV:
            return "(" + str(self.left) + "/" + str(self.right) + ")"
        elif self.operand == OPERATION_POWER:
            return "(" + str(self.left) + "^" + str(self.right) + ")"
        else:
            print("ERROR: {}: unknown operation = {}".format(__name__, self.operand))


def legitimate(root):
    if root.operand is None:
        return False
    if root.operand == OPERATION_VALUE_1:
        return True
    if root.operand == OPERATION_VALUE_N:
        return True
    return legitimate(root.left) and legitimate(root.right)

def calc(root, n):
    if root.operand == OPERATION_VALUE_1:
        return 1
    if root.operand == OPERATION_VALUE_N:
        return n
    if root.operand == OPERATION_ADD:
        return calc(root.left, n) + calc(root.right, n)
    if root.operand == OPERATION_SUB:
        return calc(root.left, n) - calc(root.right, n)
    if root.operand == OPERATION_MUL:
        return calc(root.left, n) * calc(root.right, n)
    if root.operand == OPERATION_DIV:
        try:
            return calc(root.left, n) / calc(root.right, n)
        except:
            return 0
    if root.operand == OPERATION_POWER:
        try:
            return calc(root.left, n) ** calc(root.right, n)
        except:
            return 0

def set_leaf(sub_tree, path, operand):
    if len(path) == 0:
        sub_tree.operand = operand
    elif path[0] == LEFT_OPERAND:
        set_leaf(sub_tree.left, path[1:], operand)
    elif path[0] == RIGHT_OPERAND:
        set_leaf(sub_tree.right, path[1:], operand)
    else:
        print("ERROR: unknown operand = {}".format(operand))


def add_leaf(sub_tree, path):
    if len(path) == 1:
        if path[0] == LEFT_OPERAND:
            if sub_tree.left is not None:
                print("ERROR: Trying to add a left leaf when it already exists")
                exit(1)
            sub_tree.left = Function()
        if path[0] == RIGHT_OPERAND:
            if sub_tree.right is not None:
                print("ERROR: Trying to add a right leaf when it already exists")
                exit(1)
            sub_tree.right = Function()
        return sub_tree
    else:
        if path[0] == LEFT_OPERAND:
            if sub_tree.left is None:
                print("ERROR: Trying to go down a left leaf that doesn't exist")
                exit(1)
            return add_leaf(sub_tree.left, path[1:])
        if path[0] == RIGHT_OPERAND:
            if sub_tree.right is None:
                print("ERROR: Trying to go down a right leaf that doesn't exist")
                exit(1)
            return add_leaf(sub_tree.right, path[1:])


def expand_tree_int(root, sub_tree, path_so_far, list_of_trees):
    if sub_tree.operand is None:
        for operand in [OPERATION_VALUE_1, OPERATION_VALUE_N]:
            new_tree = copy.deepcopy(root)
            set_leaf(new_tree, path_so_far, operand)
            list_of_trees.append(new_tree)
        for operand in [OPERATION_ADD, OPERATION_SUB, OPERATION_MUL, OPERATION_POWER, OPERATION_DIV]:
            new_tree = copy.deepcopy(root)
            set_leaf(new_tree, path_so_far, operand)
            add_leaf(new_tree, path_so_far + [LEFT_OPERAND])
            add_leaf(new_tree, path_so_far + [RIGHT_OPERAND])
            list_of_trees.append(new_tree)
        return
    elif sub_tree.operand == OPERATION_VALUE_1:
        return
    elif sub_tree.operand == OPERATION_VALUE_N:
        return
    else:
        if sub_tree.left is None:
            print("{}: ERROR: sub_tree.left is None")
            exit(1)
        expand_tree_int(root, sub_tree.left, path_so_far + [LEFT_OPERAND], list_of_trees)
        if sub_tree.right is None:
            print("{}: ERROR: sub_tree.right is None")
            exit(1)
        expand_tree_int(root, sub_tree.right, path_so_far + [RIGHT_OPERAND], list_of_trees)


def expand_tree(tree):
    list_of_trees = []
    expand_tree_int(tree, tree, [], list_of_trees)
    return list_of_trees

def expand(node):
    list_of_trees = expand_tree(node.state)
    new_nodes=[]
    for tree in list_of_trees:
        new_node = make_node(tree, node.depth+1)
        new_nodes.append(new_node)
    return new_nodes


class Node:
    def __init__(self, state, depth, cost):
        self.state = state
        self.parent = None
        self.operator = None
        self.depth = depth
        self.cost = cost
    def __str__(self):
        return str(self.state)


class Queue:
    def __init__(self, first_element):
        self.queue_list = []
        self.queue_list.append(first_element)

    def empty(self):
        return len(self.queue_list) == 0

    def front(self):
        return self.queue_list[0]

    def pop(self):
        self.queue_list = self.queue_list[1:]

    def push_back(self, item):
        self.queue_list.append(item)

    def sort_according_to_cost(self):
        self.queue_list.sort(key=lambda x: x.cost)

    def __str__(self):
        my_str = ""
        for element in self.queue_list:
            my_str = my_str + str(element) + ", "
        return my_str


def make_queue(element):
    q = Queue(element)
    return q


def enqueue_at_end(nodes, new_nodes):
    for new_node in new_nodes:
        nodes.push_back(new_node)
    nodes.sort_according_to_cost()
    return nodes


def initial_state(problem):
    initial_one_node_no_operation_function_tree = Function()
    return initial_one_node_no_operation_function_tree

def calc_cost(function_tree):
    if function_tree.operand == None:
        return 1
    if function_tree.operand == OPERATION_VALUE_1:
        return 0
    if function_tree.operand == OPERATION_VALUE_N:
        return 0
    return calc_cost(function_tree.left)+calc_cost(function_tree.right)

def make_node(function_tree, depth):
    cost = calc_cost(function_tree)
    node = Node(function_tree, depth, cost)
    return node


def remove_front(nodes):
    if nodes.empty():
        print("{}: ERROR: trying to remove an element from an empty queue")
        exit(1)
    front_node = nodes.front()
    nodes.pop()
    return front_node


def state(node):
    return node.state


def goal_test(problem, function):
    if not legitimate(function):
        return False
    for n, value in enumerate(problem):
        if calc(function, n) != value:
            return False
    return True


def general_search(problem, queuing_fn):
    nodes = make_queue(make_node(initial_state(problem),0))
    while True:
        if nodes.empty():
            return "Failure"
        node = remove_front(nodes)
        if DEBUG:
            print("node = {}".format(node))
        if node.depth==SEARCH_DEBT:
            print("ERROR: maximum depth reached without solution")
            exit(1)
        if goal_test(problem, state(node)):
            return str(node)
        nodes = queuing_fn(nodes, expand(node))
        if DEBUG:
            print("nodes = {}".format(nodes))


def breadth_first_search(problem):
    return general_search(problem, enqueue_at_end)

print(breadth_first_search([1, 2, 3, 4, 5]))
print(breadth_first_search([1, 2, 4, 8, 16]))
print(breadth_first_search([0, 1, 4, 9]))
print(breadth_first_search([-1, 0, 3, 8]))
print(breadth_first_search([1, 0, -3, -8]))
print(breadth_first_search([2, 1, -2, -7]))
print(breadth_first_search([0, 2, 8, 18]))
print(breadth_first_search([1, 3, 9, 27]))