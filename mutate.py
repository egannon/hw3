"""
This file demonstrates a basic workflow for creating mutants. First, 
we collect a list of nodes we want to mutate, then we modify
those nodes one at a time to create mutants. There are a couple things
you should change before using this for HW3: 

1) Add a command line interface
2) Add code for writing mutants back to python source code
3) Add code to turn add nodes into multiply nodes

See lines marked with TODO
"""

import sys
import ast
import astor
import random

import copy


def main():
    # We want "randomness", but we also want it to do the same thing
    # every time (determistic execution).
    random.seed(2873465893)

    # parse command line
    arg_list = sys.argv
    file_to_read = arg_list[1]
    num_mutants = int(arg_list[2])


    # collector_list = [[collector_func, mutator_func], []]
    collector_list = [[AddCollector, AddMutator], [negateCollector, negateMutator], [eqCollector, eqMutator], [ltCollector, ltMutator], [lteCollector, lteMutator], 
                    [LtTORtCollector, LtTORtMutator], [gtTORtCollector, gtTORtMutator], [isCollector, isMutator], [isnotCollector, isnotMutator], 
                    [addtosubCollector, addtosubMutator], [divideCollector, divideMutator], [assignCollector, assignMutator], [floorCollector, floorMutator]]
    
    # collector_List[0][1](node_id)
    # open file initially 
    with open(file_to_read, 'r') as f:
        program = ast.parse(f.read())
    
    how_many = 10 # how many mutations per file 
    for i in range(int(num_mutants)):

        collector = collector_list[(i %len(collector_list))] # which collector we use for this mutant
        collector[0]().visit(program)

        random.shuffle(collector[0]().binops_to_visit)
        to_mutate = collector[0]().binops_to_visit[:how_many] # get all operators for this mutant

        new_name = str(i) + ".py" # write to file function in python create file like 0.py etc
        f = open(new_name, "w")

        for (i, node_id) in enumerate(to_mutate): # loop through number of mutations you'll make in this file
            with open(file_to_read, 'r') as f:
                program = ast.parse(f.read())

            mutant = collector[1]()(node_id).visit(program) # mutate it!
            f.write(astor.to_source(mutant)) # convert ast to the source code and write it
        f.close()


# Find all the Add nodes in the program and record them.
class AddCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Add):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class AddMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)

            new_node = ast.BinOp(new_node.left, ast.Mult(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

# Find all the equal node comparators 
class negateCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Eq):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class negateMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.NotEq(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

# Find all the not eq operators
class eqCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.NotEq):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class eqMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.Eq(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

# Find all the not eq operators
class ltCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Lt):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class ltMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.LtE(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node
    
    # Find all the not eq operators
class lteCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.LtE):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class lteMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.Lt(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

    # Find all the not eq operators
class LtTORtCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Lt):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class LtTORtMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.Gt(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

    # Find all the not eq operators
class gtTORtCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Gt):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class gtTORtMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.GtE(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node
    
        # Find all the not eq operators
class isCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Is):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class isMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.IsNot(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

        # Find all the not eq operators
class isnotCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.IsNot):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class isnotMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.Is(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

        # Find all the not eq operators
class addtosubCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Add):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class addtosubMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.Sub(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

    
        # Find all the not eq operators
class divideCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Mult):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class divideMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.Div(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

class floorCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Div):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class floorMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.FloorDiv(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node    


class assignCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # check that we are indeed looking at an Add node since this
        # is what we care about
        if isinstance(node.op, ast.Assign):
            # record which node we're looking at by using the counter we
            # increment each time we visit a BinOp. This uniquely identifies
            # Add nodes since the AST is traversed deterministically using the
            # visitor pattern
            
            self.binops_to_visit.append(self.binop_count)


class assignMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1


        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            # TODO: You are responsible for figuring out how to modify this node
            # such that it turns into a multiply. Hint: it only took me one line.
            # There are other ways to do this as well (e.g. creating the
            # node directly from a constructor)
            new_node = ast.BinOp(new_node.left, ast.Delete(), new_node.right)
            
            #hidden.fixme_change_to_multiply_node(new_node)
            # run class and return the new node?
            # returning our new node will overwrite the node we were given on entry
            # to this class method
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node  


if __name__ == '__main__':
    main()