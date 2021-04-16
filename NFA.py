from DFA import DFA


class NFA():
    def __init__(self, allStates = None, alphabet = None, initialState = None, finalStates = None, Rules = None):
        self.allStates = allStates
        self.alphabet = alphabet
        self.initialState = initialState
        self.finalStates = finalStates
        self.Rules = Rules


    def printInfo(self):
        print(self.allStates)
        print(self.alphabet)
        print(self.initialState)
        print(self.finalStates)
        print(self.Rules)  

    def isAcceptByNFA(self, inputString):
        accept = True      
        currentState = self.initialState

        # insert landa between all chars of string
        inputString = " ".join(inputString)
        inputString = list(inputString)
        inputString.insert(0,' ')
        inputString.append(' ')


        for i in range(len(inputString)):
            currentStateList = [item for item in self.Rules if item[0] == currentState and item[2] == inputString[i]] #all rules from current state
            check = False
            for item in currentStateList:
                if item[2] == inputString[i]:
                    currentState = item[1]
                    check = True
                    break
            accept = check
            if not accept and inputString[i] != " ":
                return accept   

        if accept and (currentState in self.finalStates):
            return True
        else:
            return False    



    def createEquivalentDFA(self):     #ide az in site:      https://www.geeksforgeeks.org/conversion-from-nfa-to-dfa/ 
        alphabetDFA = self.alphabet
        initialStateDFA = self.initialState    
        allStatesDFA = [self.initialState]
        finalStatesDFA = []
        RulesDFA = []

        over = False
        i = 0
        while(not over):
            tempList2 = []
            for alphabet in self.alphabet:
                tempList = []
                for state in allStatesDFA[i]:
                    if type(allStatesDFA[i]) != list: state = allStatesDFA[i]
                    
                    tmp = [item for item in self.Rules if item[0] == state and item[2] == alphabet]
                    tempNewState = [item[1] for item in tmp]

                    if len(tempNewState) == 1: 
                        tempNewState = tempNewState[0]
                        if not tempNewState in tempList:
                            tempList.append(tempNewState)

                    elif len(tempNewState) == 0:
                        continue

                    elif not tempNewState in tempList and tempNewState != tempList:
                        for j in tempNewState:
                            tempList.append(j)
                        #tempList.append(tempNewState)
                    if len(allStatesDFA) == 1:
                        break 
                    # if type(allStatesDFA[i]) != list:
                    #     break    

                if len(tempList) == 1: tempList = tempList[0]

                RulesDFA.append([allStatesDFA[i], tempList, alphabet])
                
                if not tempList in allStatesDFA:
                        tempList2.append(tempList)
                        

            for j in tempList2:
                allStatesDFA.append(j)
            if len(tempList2) == 0 and i == len(allStatesDFA):
                over = True    
            if i < len(allStatesDFA)-1:
                i += 1
            else:
                break        

             

        if [] in allStatesDFA:
            for alphabet in alphabetDFA:
                if not [[], [], alphabet] in RulesDFA:
                    RulesDFA.append([[], [], alphabet])

        for finalState in self.finalStates:
            for state in allStatesDFA:
                if (finalState in state) and (state not in finalStatesDFA):
                    finalStatesDFA.append(state)

        

        return DFA(allStatesDFA, alphabetDFA, initialStateDFA, finalStatesDFA, RulesDFA)            

