# Main parse function. Takes string s and should return "e" if a valid string
def parse(s: str) -> str:

    # Iterator variable slen is the initial string length
    slen = len(s) - 1
    acceptedValues = ["v", "e", "(", ")", ".", "\\"]

    # Go through the full length of string s
    while s != "e":

        # Reset iterator if negative
        '''if(slen <  0):
            slen = len(s) - 1'''
        
        # Testing purposes. delete when final
        print(slen, s, s[slen], len(s))

        # Invalid character error
        if s[slen] not in acceptedValues:
            print("Invalid character at index", slen, ":", s[slen])
        
        # If s has no variables or expressions, return error
        if("v" not in s and "e" not in s):
            return "x"
        
        # Bracket checker
        index = 0
        brackets = 0
        while index < len(s):
            if s[index] == "(":
                brackets += 1
            if s[index] == ")":
                brackets -= 1
            
            if brackets < 0:
                return "x"
            
            index += 1
        
        if brackets != 0:
            return "x"
        
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
                return "x"
            # If the right bracket is the first character, throw an error
            if slen == 0:
                return "x"


        # If a left bracket is found
        elif s[slen] == "(":
            # If the left bracket is the last character, throw an error
            if slen == len(s)-1:
                return "x"

        # If a dot is found
        elif s[slen] == ".":
            # If there is 2 spaces behind and 1 space ahead
            if(slen >= 2 and slen != len(s)-1):
                # A dot must be preceded by \v and must have any character ahead except )
                if(s[slen-1] == "v" and s[slen-2] == "\\" and s[slen+1] != ")"):
                    s = s[:slen] + s[slen+1:]
            else:
                return "x"
        
        # If a backslash is found
        elif s[slen] == "\\":
            # If there is a space ahead
            if(slen < len(s)-2):
                # If the character ahead is not a var, return error
                if not (s[slen+1] == "v"):
                    return "x"
            else:
                return "x"

        # Follow to next loop        
        slen -= 1

    return s

print(parse("e()"))