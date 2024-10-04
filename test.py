# Main parse function. Takes string s and should return "e" if a valid string
def parse(s: str) -> str:

    # Iterator variable
    slen = len(s) - 1
    acceptedValues = ["v", "(", ")", ".", "\\"]
    result = ""
    bracketHolder = ""

    # Go through the full length of string s
    while slen != -1:


        # Invalid character error
        if s[slen] not in acceptedValues:
            print("Invalid character at index", slen, ":", s[slen])
        
        # If a var is found
        elif s[slen] == "v":

            # If there is space to the right of the v and it is 'e'
            if slen < len(s)-1:
                if s[slen + 1] == "e":

                    # If there is *not* space to the right and the character to the right is not \, do nothing
                    if not (slen > -1 and s[slen - 1] == "\\"):
                        result = result
                    else:
                        # If a backslash to the right does exist, make slen skip over the backslash
                        slen -= 1
            
            # Else, this e is the first. append e to the start of result
            else:
                result = "e" + result

        # If an opening bracket is found, return recursively
        elif s[slen] == "(":
            result = "(" + result
        
        # If a closing bracket is found, recursively parse the inside of the bracket.
        elif s[slen] == ")":
            if(slen == 0):
                print("Error: Unclosed Bracket")
            else:
                result = ")" + result
                result = parse(s[:-1]) + result

                stack = []
                stack.append(")")
                tempslen = slen

                while stack != [] and tempslen > 0:
                    if s[tempslen] == ")":
                        stack.append(")")
                    if s[tempslen] == "(":
                        stack.pop()
                    
                    tempslen -= 1

            # Subtract from slen the distance from this bracket to the associated opener

            slen -= slen - tempslen

            
            if not (result[0:2] == "(e)"):
                ("Error at index", slen, ": no expr in the brackets or no closing brackets")

        # Follow to next loop        
        slen -= 1

    return result


print(parse(""))