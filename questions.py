import streamlit as st


def get_question_data(chapter: int, question: int):
    #confirm args are positive integers
    if not isinstance(chapter, int) or not isinstance(question, int):
        raise ValueError("chapter and question must be positive integers")
    
    exec(f"q_{chapter}_{question}()") #extremely unsafe, change later if possible


def evaluate_answer(answer: str) -> bool:
    """
    Checks if the output saved in the session state is equal to the given answer.
    Saves the result as a boolen in the session state with key 'answer'.
    """
    if "stdout" not in st.session_state:
        st.session_state.stdout = ""
        st.session_state.stderr = ""

    st.session_state.answer = st.session_state.stdout.strip() == answer and st.session_state.stderr.strip() == ""


chapters ={1: {"title": "Basic Concepts",
               "description": "Learn the basic concepts of python, such as printing text, variables, comments and simple operations.",
               "questions": {
                    1: "Hello World!",
                    2: "Variables",
                    3: "Comments",
                    4: "Arithmetic operators",
                    5: "Lists"
                    }
                },
            2: {"title": "Basic Data Types",
                "description": "Learn the basic data types of python, such as strings, integers and floats.",
                "questions": { 
                    1: "Integers",
                    2: "Floats",
                    3: "Strings",
                    4: "String Concatenation",
                    5: "Booleans"
                }
                },
            3: {"title": "If-else statements",
                "description": "Learn how to use if-else statements to control the flow of your program.",
                "questions": {
                    1: "Basic Comparisons",
                    2: "If Statement",
                    3: "Else Statement",
                    4: "Elif Statement",
                    5: "Logical Operators",
                    6: "Logical Operations in Conditions"
                }
                },
            4:{"title": "Loops",
               "description": "Learn how to use loops in order to improve your code.",
               "questions": {
                    1: "For with Range",
                    2: "For with Lists",
                    3: "While loop",
                    4: "For loop with steps",
                    5: "Break",
                    6: "Continue"
               }
            }

           }


def q_1_1():
    st.subheader(f"1.1: {chapters[1]['questions'][1]}")
    st.write("The start of every programmer's journey is learning how to make a programm that outputs \"Hello World\".")
    st.write("In python, this is done using the print() command, like this:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("print(\"Hello World!\")")
    with col2: st.code("Hello World!", language=None)
    st.write("It's important to put your message inside quotes like \"this\" otherwise python wont know that you're talking about text. We'll expand on this more in the next page.")

    answer = "Hello Pylearn!"

    st.write(f"For now try it yourself! Write a program that outputs \"{answer}\" using the code editor on the left.")

    evaluate_answer(answer)


def q_1_2():
    st.subheader(f"1.2: {chapters[1]['questions'][2]}")
    st.write("A variable is like a container that stores information you want to use later. You can create a variable by choosing a name and using the = sign to assign it a value. For example:")
    st.code("greeting = \"Hello World!\"")
    st.write("Here, we created a variable called \"greeting\" and assigned it the value \"Hello World!\". You can then use this variable in your code, for example:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("greeting = \"Hello World!\"\nprint(greeting)")
    with col2: st.code("Hello World!\n", language=None)
    st.write("This will print the value of our variable, which is \"Hello World!\"."+\
            "You can name a variable anything you want, as long as it starts with a letter and doesn't contain spaces or special characters(except the underscore, which is allowed).\n"+\
            "a variable may be used to store anything for any length of time, and may also be changed at any time. For example:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("greeting = \"Hello World!\"\ngreeting = 42\nprint(greeting)")
    with col2: st.code("42\n", language=None)

    st.write("Notice that 42 isn't in quotes, that is because it is a number, not text. If you were to write text without quotes, python would try to use a variable that doesn't exist and throw an error. For example:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("print(\"greeting\")\nprint(greeting)")
    with col2: st.code("greeting\n"+\
                        "Traceback (most recent call last):\n"+\
                        "File \"Temp\\tmpo4og6s71.py\", line 1, in <module>\n"+\
                        "   print(greeting)\n"+\
                        "NameError: name 'greeting' is not defined\n", language=None)

    answer = "Python variable"
    st.write(f"To continue, try creating a variable with the text value \"{answer}\" and printing it out.")

    evaluate_answer(answer)


def q_1_3():
    st.subheader(f"1.3: {chapters[1]['questions'][3]}")
    st.write("Comments are lines in your code that are ignored by Python. They are useful to explain what your code does, making it easier to understand. You can create a comment by starting a line with the # symbol.")
    st.write("Anything after the # symbol on that line **will** be ignored by Python. For example:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("# This is a comment\nprint(\"Comments are useful\")")
    with col2: st.code("Comments are useful\n", language=None)

    st.write("even valid python code may be commented out, like this:")
    col1, col2 = st.columns([0.6, 0.4]) 
    with col1: st.code("#print(\"This will not run\")\nprint(\"This will run\")")
    with col2: st.code("This will run\n", language=None)

    st.markdown("remember you can also put comments **after** a valid command in the same line, like this:")
    col1, col2 = st.columns([0.6, 0.4]) 
    with col1: st.code("print(\"This will run\") # This is a comment")
    with col2: st.code("This will run\n", language=None)
    
    st.write("Overall, comments are a great way to make your code more readable and understandable. You can use them to explain what your code does, why you made certain choices, or to leave notes for yourself or others who might read your code later.\n"+\
            "You'd also be surprised how often people forget what their own code does, so leaving comments for your future self is never a bad idea.")
    st.markdown("To continue to the next page, uncomment the lines that will have the code print the words \"comments\", \"are\" and \"useful\" across 3 lines, and *comment out* any lines that interfere with this goal.")

    answer = "comments\nare\nuseful"
    st.session_state.editor_content = "#print(Do not uncomment this)\n"+\
                    "print(\"comments\")\n"+\
                    "print(42)\n"+\
                    "#print(are)\n"+\
                    "#print(\"are\")\n"+\
                    "#print(\"useful\")\n"+\
                    "print(\"comments are useful\")\n"
                                        
    evaluate_answer(answer)


def q_1_4():
        st.subheader(f"1.4: {chapters[1]['questions'][4]}")
        st.write("In python we can do addition, subtraction, multiplication and division. The symbols are +, -, * and /.")
        st.write("The priority of operations is the same as in mathematics. For example:")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("print(\"9+3-2\")")
        with col2: st.code("10", language=None)

        answer = "10\n6\n16\n4"
        st.write("To continue trye to use the command print in order to print the numbers \"10\", \"6\", \"16\" and \"4\", using only the numbers 8 and 2")

        evaluate_answer(answer)



def q_1_5():
        st.subheader(f"1.5: {chapters[1]['questions'][5]}")
        st.write("Lists in Python store multiple values. They are created with brackets [] and the values ​​are separated by commas.")
        st.write("They always start from element zero. For example:")
        st.write("The first element of the list is printed.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("fruits = [\"apple\",\"banana\",\"orange\"]\nprint(fruits[0])")
        with col2: st.code("apple", language=None)

        answer = "dog"
        st.session_state.editor_content = "animals = [\"cat\",\"dog\",\"snake\"]"
        st.write(f"Look at the list and print\"{answer}\"")
        evaluate_answer(answer)

def q_2_1():
        st.subheader(f"2.1: {chapters[2]['questions'][1]}")
        st.write("Integers are whole numbers. They can be positive, negative or even zero.")
        st.write("You can set a variable as int. For example:")
        st.write("These are some intergers.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("a=4 #positive interger\nb=-4 #negative interger\nc=0 #zero is an interger\nprint(a,b,c)")
        with col2: st.code("4 -4 0", language=None)

        st.write("You can also turn decimal numbers into integers through the int() function. For example:")
        st.write("This number will turn into an integer.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("d=4.5\nprint(int(d))")
        with col2: st.code("4", language=None)

        answer = "5"
        st.session_state.editor_content = "num = 5.2\n"+\
                                          "print(num)"
        st.write(f"Fix it in order to print\"{answer}\"")
        evaluate_answer(answer)

def q_2_2():
        st.subheader(f"2.2: {chapters[2]['questions'][2]}")
        st.write("Floats are numbers that are positive or negative, where they contain one or more decimals")
        st.write("You can set a variable as float. For example:")
        st.write("These are some floats.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("a=4.2 #positive float\nb=-4.7 negative float\nprint(a,b)")
        with col2: st.code("4.2 -4.7", language=None)

        st.write("You can also turn integer numbers into floats through the float() function. For example:")
        st.write("This number will turn into an float.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("d=4\nprint(float(d))")
        with col2: st.code("4.0", language=None)

        answer = "7.0"
        st.session_state.editor_content = "num = 7\n"+\
                                          "print(num)"
        st.write(f"Change what the line print contains in order to print\"{answer}\"")
        evaluate_answer(answer)


def q_2_3():
        st.subheader(f"2.3: {chapters[2]['questions'][3]}")
        st.write("Strings are ways to use textual data. You can save a string in python through (\"\") or ('')")
        st.write("You can set variables as string. For example:")
        st.write("These are some strings.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("a=\"animal\"#string\nb='human'#also string\nprint(a,b)")
        with col2: st.code("animal human", language=None)

        st.write("You can also turn integer numbers into string through the str() function. For example:")
        st.write("This number will turn into string.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("str(4)")
        with col2: st.code("'4'", language=None)

        answer = "dracula"
        st.session_state.editor_content = "t = \n"+\
                                          "print(t)"
        st.write(f"Put the right content in the first line of code in order to print \"{answer}\"")
        evaluate_answer(answer)

def q_2_4():
        st.subheader(f"2.4: {chapters[2]['questions'][4]}")
        st.write("In Python we can concatenate strings using the + operator. For example:")
        st.write("Two strings are joined to create a message.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("greeting = \"Hey\"\nname=\"Friend\"\nprint(greeting + name))")
        with col2: st.code("Hey Friend", language=None)

        answer = "minecraft"
        st.session_state.editor_content = "part1=\"mine\"\n"+\
                                           "part2=\"craft\"\n"+\
                                           "print()"
        st.write(f"Combine part1 and part2 in order to print\"{answer}\"")
        evaluate_answer(answer)

def q_2_5():
        st.subheader(f"2.5: {chapters[2]['questions'][5]}")
        st.write("Booleans can have only one of two values. They are either True or False. For example:")
        st.write("You can set one variable as False")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("a = False\nprint(a))")
        with col2: st.code("False", language=None)

        answer = "True"
        st.session_state.editor_content = "a=True\n"+\
                                          "b=False\n"+\
                                          "print()"

        st.write(f"Put the right variable into print in order to get a \"{answer}\" statement")
        evaluate_answer(answer)


def q_3_1():
        st.subheader(f"3.1: {chapters[3]['questions'][1]}")
        st.write("In Python we can compare values ​​using operators such as == (equal), != (not equal), > (greater than), < (less than).")
        st.write("The outcome is either True or False. For example:")
        st.write("This is a true statement:")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("print(5>3)")
        with col2: st.code("True", language=None)

        st.write("This is a false statement:")
        
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("print(5<3)")
        with col2: st.code("False", language=None)

        answer = "False"
        st.session_state.editor_content = "print(5>3)"
        st.write(f"Change it in order to be \"{answer}\" and printing it out.")
        evaluate_answer(answer)


def q_3_2():
        st.subheader(f"3.2: {chapters[3]['questions'][2]}")
        st.write("The if statement checks if it's true. If it's true it proceeds to execute the code. For example:")
        st.write("You can set one variable as False")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("num=5\nif num > 0:\n     print(\"postive\")")
        with col2: st.code("positive", language=None)

        answer = "hot"
        st.session_state.editor_content = "celcius=20\n"+\
                                          "if celcius > 30:\n"+\
                                          "     print(\"hot\")"

        st.write(f"Change the value in celcius in order to print the word \"{answer}\"")
        evaluate_answer(answer)

def q_3_3():
        st.subheader(f"3.3: {chapters[3]['questions'][3]}")
        st.write("The else statement goes with if statements. When an if statement is false then it will proceed to execute the else code. For example:")
        st.write("This is an else statement")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("num=-6\nif num > 0:\n     print(\"positive\")\nelse:\n     print(\"negative\")")
        with col2: st.code("negative", language=None)

        answer = "the name is leon"
        st.session_state.editor_content = "name = \"leon\"\n"+\
                                          "if        :\n"+\
                                          "     print(\"the name is not leon\")\n"+\
                                          "else:\n"+\
                                          "     print()"
        st.write(f"Make the if statement in order to print \"{answer}\"")
        evaluate_answer(answer)       

def q_3_4():
        st.subheader(f"3.4: {chapters[3]['questions'][4]}")
        st.write("The elif (else if) statement allows for testing multiple conditions. For example:")
        st.write("This is an elif statement.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("num = 0\nif num > 0:\n     print(\"positive\")\nelif num == 0:\n     print(\"zero\")\nelse:\n     print(\"negative\")")
        with col2: st.code("zero", language=None)

        answer = "Equal to ten"
        st.session_state.editor_content = "num = 10\n"+\
                                          "if        :\n"+\
                                          "     print(\"Bigger than ten\")\n"+\
                                          "elif        :\n"+\
                                          "     print(\"Equal to ten\")\n"+\
                                          "else:\n"+\
                                          "     print(\"Bigger than ten\")"
        st.write(f"Complete the code in order to print \"{answer}\"")
        evaluate_answer(answer)

def q_3_5():
        st.subheader(f"3.5: {chapters[3]['questions'][5]}")
        st.write("There three important logical operators. They are AND, OR and NOT.")
        st.write("The operator AND returns true if both parts are true.")
        st.write("When one is true and the other is false, it becomes false. For Example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("a, b = True, False\nif a and b:\n    print(\"This will not be printed\")#it will print nothing")
        with col2: st.code("               ", language=None)
        st.write("But when are both true, it becomes true. For Example:")
        with col1: st.code("a, b = True, True\nif a and b:\n    print(\"This will be printed\")#it will print")
        with col2: st.code("This will be printed", language=None)

        st.write("The operator OR returns true if either parts are true.")
        st.write("When both are False, it becomes false. For Example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("a, b = False, False\nif a or b:\n    print(\"This will not be printed\")#it will print nothing")
        with col2: st.code("               ", language=None)
        st.write("But when one of them is True, it becomes true. For Example:")
        with col1: st.code("a, b = True, False\nif a or b:\n    print(\"This will be printed\")#it will print")
        with col2: st.code("This will be printed", language=None)

        st.write("The operator NOT reserves the condition.")
        st.write("If the operant is true, when you put a not it will be false. For Example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("a = True\nprint(not a):\n")
        with col2: st.code("False", language=None)

        answer = "Both are true\nOne of them is true\nThe not of one is equal to the normal state of the other"
        st.session_state.editor_content = "s1 = True\n"+\
                                          "s2 = False\n"+\
                                          "s3 = True\n"+\
                                          "if   and :\n"+\
                                          "     print(\"Both are true\")\n"+\
                                          "if   or :\n"+\
                                          "     print(\"One of them is true\")\n"+\
                                          "if not  ==  :\n"+\
                                          "     print(\"The not of one is equal to the normal state of the other\")\n"
        st.write("Complete the if statement in order to print these")
        evaluate_answer(answer)

def q_3_6():
        st.subheader(f"3.6: {chapters[3]['questions'][6]}")
        st.write("You can use logical operations in order to check conditions.")
        st.write("They are many ways you can use and in if statements. For example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("age = 14\nheight = 180\nif age==14 and height==180:\n    print(\"The person is 14 and has height 180 cm\")")
        with col2: st.code("The person is 14 and has height 180 cm", language=None)
        st.write("The same is true about or. For Example:")
        with col1: st.code("age = 14\nheight = 180\nif age==14 or height==180:\n    print(\"The person is either 14 or has height 180 cm\")")
        with col2: st.code("The person is either 14 or has height 180 cm", language=None)

        answer = "Both are true\nOne of them is true\nThe not of one is equal to the normal state of the other"
        st.session_state.editor_content = "s1 = True\n"+\
                                          "s2 = False\n"+\
                                          "s3 = True\n"+\
                                          "if   and :\n"+\
                                          "     print(\"Both are true\")\n"+\
                                          "if   or :\n"+\
                                          "     print(\"One of them is true\")\n"+\
                                          "if not  ==  :\n"+\
                                          "     print(\"The not of one is equal to the normal state of the other\")\n"
        st.write("Complete the if statement in order to print these")
        evaluate_answer(answer)

def q_4_1():
        st.subheader(f"4.1: {chapters[4]['questions'][1]}")
        st.write("This loop repeats the code a certain number of times the user has chose.")
        st.write("The range() function is used to choose the number of times it will repeat. For example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("for i in range(5):\n    print(i)#it will print five times")
        with col2: st.code("0\n1\n2\n3\n4", language=None)

        answer = "0\n1\n2\n3"
        st.session_state.editor_content = "for i in range():\n"+\
                                          "    print()\n"
        st.write("Complete the loop in order to print the numbers 0,1,2,3 in order.")
        evaluate_answer(answer)

def q_4_2():
        st.subheader(f"4.2: {chapters[4]['questions'][2]}")
        st.write("The for loop can iterate over the elements of a list.")
        st.write("It is element per elements. For example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("fruits = [\"apple\", \"banana\", \"orange\"]\nfor fruit in fruits:\n    print(fruit)#it will print the fruits")
        with col2: st.code("apple\nbanana\norange", language=None)

        answer = "cat\ndog\nturtle"
        st.session_state.editor_content = "animals = []\n"+\
                                          "for animal in :\n"+\
                                          "    print()"
        st.write("Complete the loop in order to print the animals cat, dog and turtle in order.")
        evaluate_answer(answer)

def q_4_3():
        st.subheader(f"4.3: {chapters[4]['questions'][3]}")
        st.write("The while loop repeats as long as a condition is true.")
        st.write("You can count how many times it repeats. For example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("count = 1\nwhile count <= 3:\n    print(count)  # Prints 1,2,3\n    count += 1")
        with col2: st.code("1\n2\n3", language=None)

        answer = "0\n1\n2"
        st.session_state.editor_content = "num = \n"+\
                                          "while num <= :\n"+\
                                          "    print()\n"+\
                                          "    num += "
        st.write("Complete the loop in order to print the numbers 0, 1 and 2.")
        evaluate_answer(answer)

def q_4_4():
        st.subheader(f"4.4: {chapters[4]['questions'][4]}")
        st.write("Inside the range() you can skip steps. The range (x,y,z) the x is from when we start, y is for where it ends and z is the step it will go.")
        st.write("You can use it in order to print even numbers. For example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("for i in range(2, 7, 2):\n    print(i)")
        with col2: st.code("2\n4\n6", language=None)

        answer = "3\n6\n9"
        st.session_state.editor_content = "for i in range(, , ):\n"+\
                                          "    print()"
        st.write("Complete the loop in order to print the numbers 3, 6 and 9.")
        evaluate_answer(answer)

def q_4_5():
        st.subheader(f"4.5: {chapters[4]['questions'][5]}")
        st.write("The break statement terminates a loop before it completes.")
        st.write("You can combine it with an if statement. For example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("for i in range(5):\n    if i == 3:\n        break\n    print(i)")
        with col2: st.code("0\n1\n2", language=None)

        answer = "0\n1\n2\n3\n4"
        st.session_state.editor_content = "for i in range(6):\n"+\
                                          "    if :\n"+\
                                          "        break\n"+\
                                          "    print()"
        st.write("Make the loop to print until it is 4.")
        evaluate_answer(answer)

def q_4_6():
        st.subheader(f"4.6: {chapters[4]['questions'][6]}")
        st.write("The continue statement skips the current iteration and continues with the next one.")
        st.write("You can use it to skip a number. For example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("for i in range(1, 5):\n    if i == 2:\n        continue\n    print(i)")
        with col2: st.code("1\n3\n4", language=None)

        answer = "1\n2\n4"
        st.session_state.editor_content = "for i in range(1, 5):\n"+\
                                          "    if :\n"+\
                                          "        continue\n"+\
                                          "    print()"
        st.write("Complete the code to skip the number 3 and print the remaining numbers from 1 to 4.")
        evaluate_answer(answer)
