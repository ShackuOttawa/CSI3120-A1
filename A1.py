import os
from typing import Union, List, Optional

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
all_valid_chars = var_chars + ["(", ")", ".", "\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]:
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """

    lines = list()

    with open (fp) as f:
        for line in f:
            lines.append(line.rstrip("\n "))

    return lines


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """

    if(s[0] in alphabet_chars and s.isalnum()):
        return True
    else:
        return False


class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
        self.children = []


    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)


class ParseTree:
    """
    A full parse tree, with nodes
    Attributes:
        root: the root of the tree
    """
    def __init__(self, root):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:

        dashes = "----" * level

        if level == 0:
            print(self.root.elem)
            level = 1
            dashes = "----" * level
        #else:
        #    print(f"{dashes}{self.root.elem}")

        i = 0
        while i < len(self.root.children):
            if isinstance(self.root.children[i], str):
                print(f"{dashes}{self.root.children[i]}")
            elif isinstance(self.root.children[i], Node):
                print(f"{dashes}{self.root.children[i].elem}")
                ParseTree(self.root.children[i]).print_tree(None, level+1)
            i += 1

        



def parse_tokens(s_: str) -> Union[List[str], bool]:
    """
    Gets the final tokens for valid strings as a list of strings, only for valid syntax,
    where tokens are (no whitespace included)
    \\ values for lambdas
    valid variable names
    opening and closing parenthesis
    Note that dots are replaced with corresponding parenthesis
    :param s_: the input string
    :return: A List of tokens (strings) if a valid input, otherwise False
    """

    s = s_[:]  #  Don't modify the original input string

    tokens = tokenizer(s)

    s = parserPreparer(s)
    
    s = "".join(s).replace(" ", "")
    s = parse(s)

    if s == "e":
        return tokens
    else:
        return False
    
def tokenizer(s:str) -> List[str]:
    i = 0
    result = []
    dotbrackets = 0

    while i < len(s):
        
        if s[i].isalpha():
            # Find the full variable, append it to the result
            last = findFullVar(s, i)
            # Add variable only if it is a valid var name
            # If the variable is only one character, add it
            if i == last:
                result.append(s[i])

            # If the variable is the last part of the string
            elif(last + 1 == len(s)):
                if(is_valid_var_name(s[i:])):
                    result.append(s[i:])
            # If the variable is not the last part of the string
            elif(last + 1 < len(s)):
                if(is_valid_var_name(s[i:last])):
                    result.append(s[i:last+1])

            i = last + 1  # Move i to the next character after the word
        else:
            # dots are converted to brackets
            if s[i] == ".":
                result.append("(")
                dotbrackets += 1
            elif s[i] != " ":
                result.append(s[i])
            i += 1
    
    # Add in final dot brackets
    while dotbrackets > 0:
        result.append(")")
        dotbrackets -= 1
            
    # return the result list
    return result


def parserPreparer(s: str) -> List[str]:
    i = 0
    result = []
    
    while i < len(s):
        if s[i].isalpha():
            # Find the full variable and replace with 'v'
            last = findFullVar(s, i)
            # Add variable only if it is a valid var name
            # If the variable is only one character, add it
            if i == last:
                result.append('v')
            # If the variable is the last part of the string
            elif(last + 1 == len(s)):
                if(is_valid_var_name(s[i:])):
                    result.append('v')
            # If the variable is not the last part of the string
            elif(last + 1 < len(s)):
                if(is_valid_var_name(s[i:last])):
                    result.append('v')

            i = last + 1  # Move i to the next character after the word
        else:
            # Non-alphabetic characters are kept as they are
            result.append(s[i])
            i += 1
            
    # return the result list
    return result


# Finds the full variable name after given the first letter
def findFullVar(s: str, start: int) -> int:
    while start + 1 < len(s) and s[start + 1].isalnum():
        start += 1
    return start

# Main parse function. Takes string s and should return "e" if a valid string
def parse(s: str) -> str:

    # Iterator variable slen is the initial string length
    slen = len(s) - 1
    acceptedValues = ["v", "e", "(", ")", ".", "\\"]

    # Go through the full length of string s
    while s != "e":

        # Reset iterator if negative
        if(slen <  0):
            slen = len(s) - 1

        # Invalid character error
        if s[slen] not in acceptedValues:
            print("Invalid character at index", slen, ":", s[slen])
            return "x"
        
        # If s has no variables or expressions, return error
        if("v" not in s and "e" not in s):
            print("String has no variables or expressions. Index:", slen, ":", s)
        
        # Bracket checker
        index = 0
        brackets = 0
        while index < len(s):
            if s[index] == "(":
                brackets += 1
            if s[index] == ")":
                brackets -= 1
            
            if brackets < 0:
                print("Invalid amount of closing brackets at index", slen, ":", s[slen])
                return("x")
            
            index += 1
        
        if brackets != 0:
            print("Invalid amount of total brackets at index", slen, "in :", s)
            return("x")
        
        # If a var is found
        elif s[slen] == "v":
            # If there is space to the right
            if(slen < len(s) - 1):
                # If the space to the right is an expr
                if(s[slen+1] == "e"):
                    # If there is space to the left
                    if(slen > 0):
                        # If there is a backslash to the left of the current var
                        if(s[slen-1] == "\\"):
                            # Remove the backslash and the var, replacing it with an e
                            s = s[:slen-1] + s[slen+1:]
                        # There is space to the left but not a backslash. Replace with e
                        else:
                            s = s[:slen] + s[slen+1:]
                    else:
                        # No space to the left. Remove the first value: expr expr rule
                        s = s[slen+1:]
                # If the space to the right is a right bracket, and if there is space to the left
                elif(s[slen+1] == ")"):
                    # If there is a space to the left
                    if(slen > 0):
                        # If the space to the left is a left bracket
                        if(s[slen-1] == "("):
                            # If the space to the right is the last character of the string
                            if(slen+2 == len(s)):
                                # Remove brackets
                                s = s[:slen-1] + "e"
                            else:
                                # The space to the right is not the last character of the string. Remove brackets
                                s = s[:slen-1] + "e" + s[slen+2:]
                        # The space to the left is not a left bracket. Turn this var into an expr
                        else:
                            s = s[:slen] + "e" + s[slen+1:]
            
            # If there is nothing to the right, turn this var into an expr
            else:
                s = s[:slen] + "e"
        
        # If an expr is found
        elif s[slen] == "e":
            # If there is space to the right
            if(slen < len(s) - 1):
                # If the space to the right is a right bracket, and if there is space to the left
                if(s[slen+1] == ")" and slen > 0):
                    # If the space to the left is a left bracket
                    if(s[slen-1] == "("):
                        # If the space to the right is the last character of the string
                        if(slen+2 == len(s)):
                            # Remove brackets
                            s = s[:slen-1] + "e"
                        else:
                            # The space to the right is not the last character of the string. Remove brackets
                            s = s[:slen-1] + "e" + s[slen+2:]

                # If there is an expr to the right of the current var
                elif(s[slen+1] == "e"):
                    s = s[:slen] + s[slen+1:]
                
        # If a right bracket is found
        elif s[slen] == ")":
            # If there is a left bracket directly to its left, throw an error
            if s[slen-1] == "(":
                print("Invalid input: Empty bracket expression at index", slen)
                return "x"
            # If the right bracket is the first character, throw an error
            if slen == 0:
                print("Invalid input, closing bracket with no opening bracket at index", slen, ":", s[:slen])
                return "x"


        # If a left bracket is found
        elif s[slen] == "(":
            # If the left bracket is the last character, throw an error
            if slen == len(s)-1:
                print("Invalid input at index", slen, ": can not end input with an open bracket", s[slen])
                return "x"

        # If a dot is found
        elif s[slen] == ".":
            # If there is 2 spaces behind and 1 space ahead
            if(slen >= 2 and slen != len(s)-1):
                # A dot must be preceded by \v and must have any character ahead except )
                if(s[slen-1] == "v" and s[slen-2] == "\\" and s[slen+1] != ")"):
                    s = s[:slen] + s[slen+1:]
            else:
                print("Invalid usage of", s[slen], "at index", slen)
                return "x"
        
        # If a backslash is found
        elif s[slen] == "\\":
            # If there is a space ahead
            if(slen < len(s)-2):
                # If the character ahead is not a var, return error
                if not (s[slen+1] == "v"):
                    print("Invalid usage of Lambda statement at index", slen, ":", s[slen])
                    return "x"
            else:
                print("Invalid usage of Lambda statement at index", slen, ":", s[slen])
                return "x"

        # Follow to next loop        
        slen -= 1

    return s

def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")



def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None:
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()




def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree
    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """

    # Node(elem); elem is the full contents of the Node
    thisNode = Node("_".join(tokens))
    
    i = 0

    while i < len(tokens):
        # when a backslash is not the beginning token, create child chain from the backslash onwards
        if tokens[i] == "\\" and i != 0:
            thisNode.add_child_node(build_parse_tree_rec(tokens[i:-1]))
            i = len(tokens)-2
        # when an opening bracket is not the beginning term, create child chain up to the associated closing bracket.
        elif tokens[i] == "(" and i != 0:
            bracketCounter = 1
            j = i+1
            while bracketCounter != 0:
                if tokens[j] == "(":
                    bracketCounter += 1
                elif tokens[j] == ")":
                    bracketCounter -= 1
                
                j += 1

            if j < len(tokens):
                thisNode.add_child_node(build_parse_tree_rec(tokens[i:j]))
            else:
                thisNode.add_child_node(build_parse_tree_rec(tokens[i:j]))
            
            i = j-1
        
        else:
            thisNode.add_child_node(tokens[i])
        
        i += 1

    return thisNode


def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":

    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)