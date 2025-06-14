import streamlit as st


def get_question_data(chapter: int, question: int, difficulty: int):
    #confirm args are positive integers
    if not isinstance(chapter, int) or not isinstance(question, int) or not isinstance(difficulty, int):
        raise ValueError("chapter and question must be difficulty positive integers")
    
    difficulty = ['e', 'm', 'h'][difficulty] if difficulty in [0, 1, 2] else 'm'
    exec(f"q_{chapter}_{question}_{difficulty}()") #extremely unsafe, change later if possible


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


def q_1_1_m():
    st.subheader(f"1.1: {chapters[1]['questions'][1]}")
    st.write("The start of every programmer's journey is learning how to make a programm that outputs \"Hello World\".")
    st.write("In python, this is done using the `print()` command, like this:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("print(\"Hello World!\")")
    with col2: st.code("Hello World!", language=None)
    st.write("It's important to put your message inside quotes like \"this\" otherwise python wont know that you're talking about text. We'll expand on this more in the next page.")

    answer = "Hello Pylearn!"

    st.write(f"For now try it yourself! Write a program that outputs \"{answer}\" using the code editor on the left.")

    evaluate_answer(answer)


def q_1_2_m():
    st.subheader(f"1.2: {chapters[1]['questions'][2]}")
    st.write("A variable is like a container that stores information you want to use later. You can create a variable by choosing a name and using the `=` sign to assign it a value. For example:")
    st.code("greeting = \"Hello World!\"")
    st.write("Here, we created a variable called \"greeting\" and assigned it the value \"Hello World!\". You can then use this variable in your code, for example:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("greeting = \"Hello World!\"\nprint(greeting)")
    with col2: st.code("Hello World!\n", language=None)
    st.write("This will print the value of our variable, which is \"Hello World!\"."+\
            "You can name a variable anything you want, as long as it starts with a letter and doesn't contain spaces or special characters (except the underscore, which is allowed).\n"+\
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


def q_1_3_m():
    st.subheader(f"1.3: {chapters[1]['questions'][3]}")
    st.write("Comments are lines in your code that are ignored by Python. They are useful to explain what your code does, making it easier to understand. You can create a comment by starting a line with the `#` symbol.")
    st.write("Anything after the `#` symbol on that line **will** be ignored by Python. For example:")
    
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


def q_1_4_m():
    st.subheader(f"1.4: {chapters[1]['questions'][4]}")
    st.write("Python can perform basic arithmetic operations such as addition (+), subtraction (-), multiplication (*), and division (/).")
    st.write("The order of operations follows standard math rules. For example:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code(
                "print(8 + 2)\n"
                "print(8 - 2)\n"
                "print(8 * 2)\n"
                "print(8 / 2)\n"
                "print(8 + 2 * 3) # Multiplication happens before addition\n"
                "print((8 + 2) * 3) # Parentheses change the order of operations"
            )
    with col2:
        st.code(
                "10\n"
                "6\n"
                "16\n"
                "4.0\n"
                "14\n"
                "30",
                language=None
        )
    
    st.write("Notice that division returns a decimal (float) by default, this is because division can result in non-integer values. We'll explain floats more in future lessons")
    st.write("As a test, set the variables `a`, `b`, `c`, and `d` in the editor in way that the expression `a + (b * c - 1) / d` evaluates to `8.0`")
    st.session_state.editor_content ="a = 1\nb = 1\nc = 1\nd = 1\n"+\
                                     "print(a + (b * c - 1) / d)"

    answer = "8.0"
    evaluate_answer(answer)

def q_1_5_m():
    st.subheader(f"1.5: {chapters[1]['questions'][5]}")
    st.write("A **list** in Python is a way to store multiple values in a single variable. Lists are created using square brackets `[]`, and values are separated by commas.")
    st.write("Lists are **zero-indexed**, meaning the first element is at position 0. For example:")
    
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('animals = ["cat", "dog", "snake"]\nprint(animals[0])')
    with col2: st.code("cat\n", language=None)

    st.write("Try it yourself! Given the list below, print only the word \"dog\" using its position in the list.")
    st.session_state.editor_content = 'animals = ["cat", "dog", "snake"]\n# Your code here'

    answer = "dog"
    evaluate_answer(answer)

def q_2_1_m():
    st.subheader(f"2.1: {chapters[2]['questions'][1]}")
    st.write("**Integers** are whole numbers, which can be positive, negative, or zero. In Python, you can assign an integer to a variable directly:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code("a = 4  # positive integer\nb = -4 # negative integer\nc = 0  # zero is also an integer\nprint(a, b, c)")
    with col2:
        st.code("4 -4 0", language=None)
    st.write("You can also convert a decimal (float) to an integer using the `int()` function. This will **remove** the decimal part (it does not round):")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code("d = 4.9\nprint(int(d))")
    with col2:
        st.code("4", language=None)
    st.write("Try changing the code so that it prints the integer `5` (not `5.2`).")
    st.session_state.editor_content = "num = 5.2\nprint(num)"
    answer = "5"
    st.write(f"Hint: Use the `int()` function to convert `num` to an integer before printing.")
    evaluate_answer(answer)

def q_2_2_m():
    st.subheader(f"2.2: {chapters[2]['questions'][2]}")
    st.write("**Floats** are numbers with a decimal point. They can be positive or negative. You can assign a float to a variable like this:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code("a = 4.2  # positive float\nb = -4.7 # negative float\nprint(a, b)")
    with col2:
        st.code("4.2 -4.7", language=None)
    st.write("You can also convert an integer to a float using the `float()` function:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code("d = 4\nprint(float(d))")
    with col2:
        st.code("4.0", language=None)
    st.write("Try changing the code so that it prints the float `7.0` (not `7`).")
    st.session_state.editor_content = "num = 7\nprint(num)"
    answer = "7.0"
    evaluate_answer(answer)

def q_2_3_m():
    st.subheader(f"2.3: {chapters[2]['questions'][3]}")
    st.write("**Strings** are used to store text. In Python, you can create a string using double (`\"`) or single (`'`) quotes:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code("a = \"animal\"  # string\nb = 'human'  # also a string\nprint(a, b)")
    with col2:
        st.code("animal human", language=None)
    st.write("You can also convert numbers to strings using the `str()` function:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code("num = 4\nprint(str(num))")
    with col2:
        st.code("4", language=None)
    st.write("To continue, try assigning the string `dracula` to the variable `t` and print it.")
    st.session_state.editor_content = "t = \nprint(t)"
    answer = "dracula"
    st.write(f"Hint: Remember to use quotes.")
    evaluate_answer(answer)

def q_2_4_m():
    st.subheader(f"2.4: {chapters[2]['questions'][4]}")
    st.write("You can **concatenate** (join) strings in Python using the `+` operator. For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code("print(\"Hey \" + \"Friend\")")
    with col2:
        st.code("Hey Friend", language=None)
    st.write("Try combining the variables `part1` and `part2` to print `minecraft`.")
    st.session_state.editor_content = "part1 = \"mine\"\npart2 = \"craft\"\nprint()"
    answer = "minecraft"
    evaluate_answer(answer)

def q_2_5_m():
    st.subheader(f"2.5: {chapters[2]['questions'][5]}")
    st.write("**Booleans** are a data type that can only be `True` or `False`. For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        st.code("a = False\nprint(a)")
    with col2:
        st.code("False", language=None)
    st.write("This isn't too useful now, but we'll soon see how booleans can control the behaviour of an enitire program.")
    st.write("For now just print the variable with the value `True`.")
    st.session_state.editor_content = "a = True\nb = False\nprint()"
    answer = "True"
    evaluate_answer(answer)


def q_3_1_m():
    st.subheader(f"3.1: {chapters[3]['questions'][1]}")
    st.write("In Python, you can compare values using operators such as `==` (equal), `!=` (not equal), `>` (greater than), and `<` (less than).")
    st.write("The result of these comparisons is always either `True` or `False`.")
    st.write("For example, this is a true statement:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("print(5 > 3)")
    with col2: st.code("True", language=None)
    st.write("And this is a false statement:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("print(5 < 3)")
    with col2: st.code("False", language=None)
    answer = "False"
    st.session_state.editor_content = "print(7>4)"
    st.write(f"Try changing the code so that it prints `{answer}`.")
    evaluate_answer(answer)

def q_3_2_m():
    st.subheader(f"3.2: {chapters[3]['questions'][2]}")
    st.write("The `if` statement checks if a condition is true. If it is, the code inside the `if` block runs.")
    st.write("For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("num = 5\nif num > 0:\n    print(\"positive\")")
    with col2: st.code("positive", language=None)
    st.write("To continue, change the value of `celcius` so that the code prints `hot`.")
    st.session_state.editor_content = "celcius = 20\nif celcius > 30:\n    print(\"hot\")"
    answer = "hot"
    evaluate_answer(answer)

def q_3_3_m():
    st.subheader(f"3.3: {chapters[3]['questions'][3]}")
    st.write("The `else` statement works with `if`. If the `if` condition is false, the code inside `else` runs.")
    st.write("For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("num = -6\nif num > 0:\n    print(\"positive\")\nelse:\n    print(\"negative\")")
    with col2: st.code("negative", language=None)
    st.write("To continue, complete the code so that it prints `the name is leon`.")
    st.session_state.editor_content = (
        "name = \"leon\"\n"
        "if        :\n"
        "    print(\"the name is not leon\")\n"
        "else:\n"
        "    print()"
    )
    answer = "the name is leon"
    evaluate_answer(answer)

def q_3_4_m():
    st.subheader(f"3.4: {chapters[3]['questions'][4]}")
    st.write("The `elif` (else if) statement allows you to check multiple conditions in sequence.")
    st.write("For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code(
        "num = 0\n"
        "if num > 0:\n"
        "    print(\"positive\")\n"
        "elif num == 0:\n"
        "    print(\"zero\")\n"
        "else:\n"
        "    print(\"negative\")"
    )
    with col2: st.code("zero", language=None)
    st.write("As a test, complete the code so that it prints `Equal to ten`.")
    st.session_state.editor_content = (
        "num = 10\n"
        "if        :\n"
        "    print(\"Bigger than ten\")\n"
        "elif        :\n"
        "    print(\"Equal to ten\")\n"
        "else:\n"
        "    print(\"Bigger than ten\")"
    )
    answer = "Equal to ten"
    evaluate_answer(answer)

def q_3_5_m():
    st.subheader(f"3.5: {chapters[3]['questions'][5]}")
    st.write("Python has three important logical operators: `and`, `or`, and `not`.")
    st.write("- `and` returns `True` if **both** conditions are true.")
    st.write("- `or` returns `True` if **at least one** condition is true.")
    st.write("- `not` reverses the value of a condition.")
    st.write("Examples:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("a, b = True, False\nif a and b:\n    print(\"This will not be printed\")")
    with col2: st.code("")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("a, b = True, True\nif a and b:\n    print(\"This will be printed\")")
    with col2: st.code("This will be printed")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("a, b = False, False\nif a or b:\n    print(\"This will not be printed\")")
    with col2: st.code("")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("a, b = True, False\nif a or b:\n    print(\"This will be printed\")")
    with col2: st.code("This will be printed")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("a = True\nprint(not a)")
    with col2: st.code("False", language=None)
    st.write("To continue, complete the code to print all three lines as described.")
    st.session_state.editor_content = (
        "s1 = True\n"
        "s2 = False\n"
        "s3 = True\n"
        "if   and :\n"
        "    print(\"Both are true\")\n"
        "if   or :\n"
        "    print(\"One of them is true\")\n"
        "if not  ==  :\n"
        "    print(\"The not of one is equal to the normal state of the other\")\n"
    )
    answer = "Both are true\nOne of them is true\nThe not of one is equal to the normal state of the other"
    evaluate_answer(answer)

def q_3_6_m():
    st.subheader(f"3.6: {chapters[3]['questions'][6]}")
    st.write("You can use logical operators directly in `if` statements to check multiple conditions at once.")
    st.write("For example, using `and`:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("age = 14\nheight = 180\nif age == 14 and height == 180:\n    print(\"The person is 14 and has height 180 cm\")")
    with col2: st.code("The person is 14 and has height 180 cm", language=None)
    st.write("Or using `or`:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("age = 14\nheight = 180\nif age == 14 or height == 180:\n    print(\"The person is either 14 or has height 180 cm\")")
    with col2: st.code("The person is either 14 or has height 180 cm", language=None)
    st.write("Just like with numbers you can use parentheses to control the order of operations")
    st.write("To continue, complete the code so that it prints all three lines as described.")
    st.session_state.editor_content = (
        "s1 = True\n"
        "s2 = False\n"
        "s3 = True\n"
        "if   and :\n"
        "    print(\"Both are true\")\n"
        "if   or :\n"
        "    print(\"One of them is true\")\n"
        "if not  ==  :\n"
        "    print(\"The not of one is equal to the normal state of the other\")\n"
    )
    answer = "Both are true\nOne of them is true\nThe not of one is equal to the normal state of the other"
    evaluate_answer(answer)

def q_4_1_m():
    st.subheader(f"4.1: {chapters[4]['questions'][1]}")
    st.write("A `for` loop repeats code a certain number of times. The `range()` function is used to specify how many times to repeat.")
    st.write("For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("for i in range(5):\n    print(i)")
    with col2: st.code("0\n1\n2\n3\n4", language=None)
    st.write("Note that the output prints the 5 numbers from 0 and goes up to 4, not 5. This is another example of Python's zero-indexing.")
    st.write("To continue complete the loop to print the numbers 0, 1, 2, and 3.")
    st.session_state.editor_content = (
        "for i in range():\n"
        "    print()\n"
    )
    answer = "0\n1\n2\n3"
    evaluate_answer(answer)

def q_4_2_m():
    st.subheader(f"4.2: {chapters[4]['questions'][2]}")
    st.write("A `for` loop can also iterate over the elements of a list, one by one.")
    st.write("For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("fruits = [\"apple\", \"banana\", \"orange\"]\nfor fruit in fruits:\n    print(fruit)")
    with col2: st.code("apple\nbanana\norange", language=None)
    st.write("As a test, try to complete the code to print the animals `cat`, `dog`, and `turtle` in order.")
    st.session_state.editor_content = (
        "animals = []\n"
        "for animal in :\n"
        "    print()"
    )
    answer = "cat\ndog\nturtle"
    evaluate_answer(answer)

def q_4_3_m():
    st.subheader(f"4.3: {chapters[4]['questions'][3]}")
    st.write("A `while` loop repeats as long as a condition is true. You can use it to count or repeat actions.")
    st.write("For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("count = 1\nwhile count <= 3:\n    print(count)\n    count += 1")
    with col2: st.code("1\n2\n3", language=None)
    st.write("To continue, complete the code to print the numbers 0, 1, and 2.")
    st.session_state.editor_content = (
        "num = \n"
        "while num <= :\n"
        "    print()\n"
        "    num += "
    )
    answer = "0\n1\n2"
    evaluate_answer(answer)

def q_4_4_m():
    st.subheader(f"4.4: {chapters[4]['questions'][4]}")
    st.write("You can use `range(start, stop, step)` in a `for` loop to skip steps. For example, to print even numbers starting from 2:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("for i in range(2, 7, 2):\n    print(i)")
    with col2: st.code("2\n4\n6", language=None)
    st.write("You can also havea negative step to count downwards. For example, to print numbers from 9 to 3:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("for i in range(9, 2, -3):\n    print(i)")
    with col2: st.code("9\n6\n3", language=None)

    st.write("To continue, complete the loop to print the numbers 3, 6, and 9.")
    st.session_state.editor_content = (
        "for i in range(, , ):\n"
        "    print()"
    )
    answer = "3\n6\n9"
    evaluate_answer(answer)

def q_4_5_m():
    st.subheader(f"4.5: {chapters[4]['questions'][5]}")
    st.write("The `break` statement stops a loop early. It's usually placed inside an `if` statement.")
    st.write("For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("for i in range(5):\n    if i == 3:\n        break\n    print(i)")
    with col2: st.code("0\n1\n2", language=None)
    st.write("To continue, make the loop print the numbers from 0 to 4 (inclusive).")
    st.session_state.editor_content = (
        "for i in range(6):\n"
        "    if :\n"
        "        break\n"
        "    print()"
    )
    answer = "0\n1\n2\n3\n4"
    evaluate_answer(answer)

def q_4_6_m():
    st.subheader(f"4.6: {chapters[4]['questions'][6]}")
    st.write("The `continue` statement works like `break`, but instead of stopping the loop completely, it instead skips the current iteration and moves to the next one.")
    st.write("For example, this loop skips the number 2:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("for i in range(1, 5):\n    if i == 2:\n        continue\n    print(i)")
    with col2: st.code("1\n3\n4", language=None)
    st.write("Try it yourself! Complete the code to skip the number 3 and print the remaining numbers from 1 to 4.")
    st.session_state.editor_content = (
        "for i in range(1, 5):\n"
        "    if :\n"
        "        continue\n"
        "    print()"
    )
    answer = "1\n2\n4"
    evaluate_answer(answer)

# --- EASY QUESTIONS (explained as if the user may be a kid, minimal explanations) ---

def q_1_1_e():
    st.subheader(f"1.1: {chapters[1]['questions'][1]}")
    st.write("Let's make the computer say something! Type `print(\"Hello World!\")`the code to say Hello World!")
    st.write("In Python, we use the `print()` command to make the computer show something on the screen. We just need to put our message in quotes like `\"this\"`.")
    st.session_state.editor_content = ""
    answer = " Hello World!"
    evaluate_answer(answer)

def q_1_2_e():
    st.subheader(f"1.2: {chapters[1]['questions'][2]}")
    st.write("We can save a message inside a variable to use it later, think of it likep putting something in a box until you need it.")
    st.write("To create a variable, we choose a name and use the `=` sign to give it a value. For example: name = `\"Hi\"`")
    st.session_state.editor_content = ""
    answer = "Hello"
    st.write("try creating a variable named `greeting` and give it the value `Hello`, then print it out using `print(greeting)`.")
    evaluate_answer(answer)

def q_1_3_e():
    st.subheader(f"1.3: {chapters[1]['questions'][3]}")
    st.write("If you'd like to write notes in your code but don't want the computer to read them, you can use comments!")
    st.write("to do this, type the `#` character, and the computer will ignore everything after that for the rest of that line.")
    st.session_state.editor_content = "print(\"don't comment me out, comment out the next 2 lines\")\n"+\
                                        "print(\"comment me out by putting a # in front of the code\")\n"+\
                                        "print(\"comment me out as well\")"
    answer = "don't comment me out, comment out the next 2 lines"
    st.write("try commenting out the code so that it only the first line prints something.")
    evaluate_answer(answer)

def q_1_4_e():
    st.subheader(f"1.4: {chapters[1]['questions'][4]}")
    st.write("We can do math with Python! We can add, subtract, multiply, and divide numbers.")
    st.write("For example:")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("print(2 + 3)\nprint(5 - 2)\nprint(4 * 2)\nprint(8 / 2)")
    with col2: st.code("5\n3\n8\n4.0", language=None)
    st.session_state.editor_content = "x = 8 + 4 - \nprint(x)"
    answer = "10"
    st.write("Try completing the first line of code so that `x` is set to the value `10`.")
    evaluate_answer(answer)

def q_1_5_e():
    st.subheader(f"1.5: {chapters[1]['questions'][5]}")
    st.write("If a variable is a box, a list is like a big box with a lot of smaller boxes in a row inside, and each small box can hold a different item.")
    st.write("We can create a list by putting items inside square brackets `[]` and seperating them using commas `,` like this:")
    st.write("`animals = [\"cat\", \"dog\", \"fish\"]`")
    st.write("We can access items in a list by their position, starting from 0. For example, `animals[0]` gives us the first item, which is `cat`.")
    st.session_state.editor_content = "i = 0\nanimals = ['cat', 'dog', 'fish']\nprint(i)"
    answer = "dog"
    st.write("Currently the code prints the first animal in the list, which is `car` , try changing the value of `i` so that it prints the second animal, which is `dog`.")
    evaluate_answer(answer)

def q_2_1_e():
    st.subheader(f"2.1: {chapters[2]['questions'][1]}")
    st.write("Integers are whole numbers, like 1, 2, or -3. We can use them in Python just like we do in math.")
    st.session_state.editor_content = "number = 1\nprint(number)"
    answer = "100"
    st.write("Change the number to 100.")
    evaluate_answer(answer)

def q_2_2_e():
    st.subheader(f"2.2: {chapters[2]['questions'][2]}")
    st.write("Floats are numbers with a decimal point, like 3.14 or -2.5. You can change integers to floats and vice versa using the `int()` and `float()`.")
    st.session_state.editor_content = "float_number = 1\nprint(float_number)"
    answer = "3.14"
    st.write("Change the code to print 3.14")
    evaluate_answer(answer)

def q_2_3_e():
    st.subheader(f"2.3: {chapters[2]['questions'][3]}")
    st.write("You can turn anything in a message, better known as a string, by putting it in quotes. For example, `\"Hello\"` is a string.")
    st.write("If you forget to put quotes around a string, Python will think it is a variable, and give you an error")
    st.session_state.editor_content = "print()"
    answer = "Hello"
    st.write("Try printing `Hello`")
    evaluate_answer(answer)

def q_2_4_e():
    st.subheader(f"2.4: {chapters[2]['questions'][4]}")
    st.write("Quick note, you can join two strings together using the `+` operator, like this: `\"Hello\" + \"World\"` gives you `HelloWorld`.")
    st.session_state.editor_content = "a = \"Craft\"\nb = \"Mine\"\nprint()"
    answer = "MineCraft"
    st.write("Try adding together the `a` and `b` to print `MineCraft`.")
    evaluate_answer(answer)

def q_2_5_e():
    st.subheader(f"2.5: {chapters[2]['questions'][5]}")
    st.write("An extra really important value **type** to know is the boolean, which can only be `True` or `False`. You will see this a lot in the future so make sure you remember it!")
    st.session_state.editor_content = "print()"
    answer = "True"
    st.write("Try printing `True`")
    evaluate_answer(answer)

def q_3_1_e():
    st.subheader(f"3.1: {chapters[3]['questions'][1]}")
    st.write("We can compare numbers in Python! To check if a number is bigger than another use: `>` or if two numbers are the same use: `==`.")
    st.write("If the comparison is true, Python will say `True`. If not, it will say `False`.")
    st.session_state.editor_content = "print(3 > 5)"
    st.write("Try changing the code so that it prints `True`.")
    evaluate_answer("True")

def q_3_2_e():
    st.subheader(f"3.2: {chapters[3]['questions'][2]}")
    st.write("We can make Python do something when a condition is true by using `if` and following it with a colon `:`. For example:")
    colA, colB = st.columns([0.6, 0.4])
    with colA: st.code("if 5 > 3:\n    print(\"Yes!\")")
    with colB: st.code("Yes!", language=None)
    st.write("Try changing the code so that it prints `It's sunny!`.")
    st.session_state.editor_content = "weather = \"rainy\"\nif weather == \"sunny\":\n    print(\"It's sunny!\")"
    answer = "It's sunny!"
    evaluate_answer(answer)

def q_3_3_e():
    st.subheader(f"3.3: {chapters[3]['questions'][3]}")
    st.write("If we want to do something when a condition is NOT true, we can use `else:`.")
    colA, colB = st.columns([0.6, 0.4])
    with colA: st.code("if 2 > 3:\n    print(\"Yes!\")\nelse:\n    print(\"No!\")")
    with colB: st.code("No!", language=None)
    st.write("Try changing the code so that it prints `The condition is False!`.")
    st.session_state.editor_content = "x = 10\nif x > 5:\n    print(\"The condition is False!\")\nelse:\n    print(\"The condition is True!\")"
    answer = "The condition is True!"
    evaluate_answer(answer)

def q_3_4_e():
    st.subheader(f"3.4: {chapters[3]['questions'][4]}")
    st.write("If we want to check for more than one case, we can use `elif` (which means 'else if').")
    colA, colB = st.columns([0.6, 0.4])
    with colA: st.code("num = 5\nif num > 5:\n    print(\"Big\")\nelif num == 5:\n    print(\"Five!\")\nelse:\n    print(\"Small\")")
    with colB: st.code("Five!", language=None)
    st.write("Try completing the code so that it prints `Two!`.")
    st.session_state.editor_content = "size = 2\nif size > 5:\n    print(\"Big!\")\nelif size == 2:\n    print(\"Two!\")\nelse:\n    print(\"Small!\")"
    answer = "Medium!"
    evaluate_answer(answer)

def q_3_5_e(): #TODO: fix this and 3_6_e
    st.subheader(f"3.5: {chapters[3]['questions'][5]}")
    st.write("We can use `and`, `or`, and `not` to combine conditions.")
    st.write("- `and` means both things must be true.")
    st.write("- `or` means at least one thing must be true.")
    st.write("- `not` means the opposite.")
    st.session_state.editor_content = (
        "a = False\n"
        "b = True\n"
        "if a and b:\n"
        "    print(\"Both true!\")\n"
        "if a or b:\n"
        "    print(\"At least one is true!\")\n"
        "if not b:\n"
        "    print(\"b is not true!\")"
    )
    answer = "At least one is true!\nb is not true!"
    st.write("Try to make the code print the second and third lines by changing the values of `a` and `b`.")
    evaluate_answer(answer)

def q_3_6_e():
    st.subheader(f"3.6: {chapters[3]['questions'][6]}")
    st.write("We can use `and` and `or` inside `if` to check more than one thing at once!")
    st.session_state.editor_content = (
        "age = 9\n"
        "height = 140\n"
        "if age > 10 and height > 140:\n"
        "    print(\"You are tall and older than 10!\")\n"
        "if age < 10 or height > 140:\n"
        "    print(\"You are either young or tall!\")"
    )
    answer = "You are tall and older than 10!\nYou are either young or tall!"
    st.write("Try changing the values so that both lines print.")
    evaluate_answer(answer)

def q_4_1_e():
    st.subheader(f"4.1: {chapters[4]['questions'][1]}")
    st.write("A `for` loop lets us repeat something many times. For example, we can print numbers from 0 to 2 like this:")
    colA, colB = st.columns([0.6, 0.4])
    with colA: st.code("for i in range(3):\n    print(i)")
    with colB: st.code("0\n1\n2", language=None)
    st.session_state.editor_content = "for i in range(5):\n    print(i)"
    answer = "0\n1\n2"
    st.write("Try changing the code so that it prints only the numbers 0, 1, and 2.")
    evaluate_answer(answer)

def q_4_2_e():
    st.subheader(f"4.2: {chapters[4]['questions'][2]}")
    st.write("We can also use a `for` loop to go through each item in a list.")
    colA, colB = st.columns([0.6, 0.4])
    with colA: st.code("colors = [\"red\", \"blue\"]\nfor color in colors:\n    print(color)")
    with colB: st.code("red\nblue", language=None)
    st.session_state.editor_content = "animals = [\"cat\", \"dog\", \"turtle\"]\nfor animal in animals:\n    print()"
    answer = "cat\ndog\nturtle"
    st.write("Try completing the code to print all the animals.")
    evaluate_answer(answer)

def q_4_3_e():
    st.subheader(f"4.3: {chapters[4]['questions'][3]}")
    st.write("A `while` loop keeps going as long as something is true.")
    colA, colB = st.columns([0.6, 0.4])
    with colA: st.code("count = 0\nwhile count < 4:\n    print(count)\n    count = count + 1")
    with colB: st.code("0\n1\n2\n3", language=None)
    st.session_state.editor_content = "num = 0\nwhile num < 2:\n    print(num)\n    num += 1"
    answer = "0\n1\n2"
    st.write("Try changing the code so that it prints 0, 1, and 2.")
    evaluate_answer(answer)

def q_4_4_e():
    st.subheader(f"4.4: {chapters[4]['questions'][4]}")
    st.write("We can use `range(start, stop, step)` to count by steps. For example, `range(2, 10, 2)` gives 2, 4, 6, 8.")
    st.session_state.editor_content = "for i in range(1, 10, 3):\n    print(i)"
    answer = "2\n4\n6\n8\n10"
    st.write("Try changing the code so that it prints 2, 4, 6, 8, 10.")
    evaluate_answer(answer)

def q_4_5_e():
    st.subheader(f"4.5: {chapters[4]['questions'][5]}")
    st.write("The `break` command stops a loop early. For example:")
    colA, colB = st.columns([0.6, 0.4])
    with colA: st.code("for i in range(5):\n    if i == 2:\n        break\n    print(i)")
    with colB: st.code("0\n1", language=None)
    st.session_state.editor_content = "for i in range(5):\n    if i == 4:\n        break\n    print(i)"
    answer = "0\n1\n2"
    st.write("Try changing the code so that it prints 0, 1, 2")
    evaluate_answer(answer)

def q_4_6_e():
    st.subheader(f"4.6: {chapters[4]['questions'][6]}")
    st.write("The `continue` command skips the rest of the loop for that turn. For example, this skips 2:")
    colA, colB = st.columns([0.6, 0.4])
    with colA: st.code("for i in range(1, 5):\n    if i == 2:\n        continue\n    print(i)")
    with colB: st.code("1\n3\n4", language=None)
    st.session_state.editor_content = "for i in range(1, 5):\n    if i == 3:\n        continue\n    print(i)"
    answer = "1\n3\n4"
    st.write("Try changing the code so that it skips 2 and prints 1, 3, 4.")
    evaluate_answer(answer)

# --- HARD QUESTIONS (for programmers, more python spesific knowlendge than programming knowledge) ---

def q_1_1_h():
    st.subheader(f"1.1: {chapters[1]['questions'][1]}")
    st.write("In Python, printing is as simple as `print()`. No main function or semicolons required. Strings can use single or double quotes interchangeably.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('print("Hello World!")')
    with col2: st.code("Hello World!", language=None)
    st.write("Try printing `Hello, Pythonistas!`")
    answer = "Hello, Pythonistas!"
    evaluate_answer(answer)

def q_1_2_h():
    st.subheader(f"1.2: {chapters[1]['questions'][2]}")
    st.write("Python variables are dynamically typed—no type declaration needed. Underscores are idiomatic for multi-word names. Assignment is always by reference for objects.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('x = 42\nname = "Guido"\nprint(name)')
    with col2: st.code("Guido", language=None)
    st.write("Assign the string `dynamic typing` to a variable and print it.")
    answer = "dynamic typing"
    evaluate_answer(answer)

def q_1_3_h():
    st.subheader(f"1.3: {chapters[1]['questions'][3]}")
    st.write("Single-line comments use `#`. No block comment syntax, but multiline strings (`'''`) are sometimes abused for doc-comments, though not executed as comments.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('# This is a comment\nprint("Python ignores comments")')
    with col2: st.code("Python ignores comments", language=None)
    st.session_state.editor_content = "# This is a comment\nprint(\"Python ignores comments\")\nprint(\"This line will be executed\")"
    st.write("Run the given code to continue")
    answer = "Python ignores comments"
    evaluate_answer(answer)

def q_1_4_h():
    st.subheader(f"1.4: {chapters[1]['questions'][4]}")
    st.write("Python supports `+`, `-`, `*`, `/` (always float), `//` (floor division), and `**` (power). Beware: `/` always returns float, even for integer inputs.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code("print(5 / 2)\nprint(5 // 2)")
    with col2: st.code("2.5\n2", language=None)
    st.write("Evaluate `7 // 3` and print the result.")
    answer = "2"
    evaluate_answer(answer)

def q_1_5_h():
    st.subheader(f"1.5: {chapters[1]['questions'][5]}")
    st.write("Lists are mutable, heterogeneous, and zero-indexed. Slicing is powerful: `a[1:-1]`. Negative indices count from the end. List comprehensions are idiomatic.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('lst = [1, "two", 3.0]\nprint(lst[1])')
    with col2: st.code("two", language=None)
    st.write("Given `lst = [10, 20, 30]`, print the last element using negative indexing.")
    st.session_state.editor_content = "lst = [10, 20, 30]\n"
    answer = "30"
    evaluate_answer(answer)

def q_2_1_h():
    st.subheader(f"2.1: {chapters[2]['questions'][1]}")
    st.write("Python integers have arbitrary precision—no overflow. `int()` can parse strings or truncate floats. Underscores are allowed for readability: `1_000_000`.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('print(int("123"))\nprint(int(3.99))')
    with col2: st.code("123\n3", language=None)
    st.write("Convert the float `9.99` to int and print it.")
    answer = "9"
    evaluate_answer(answer)

def q_2_2_h():
    st.subheader(f"2.2: {chapters[2]['questions'][2]}")
    st.write("Floats are IEEE 754 doubles. Beware of floating-point precision issues. Use `float()` to convert. Scientific notation is supported: `1e-3`.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('print(0.1 + 0.2)\nprint(float(5))')
    with col2: st.code("0.30000000000000004\n5.0", language=None)
    st.write("Print the float representation of the integer `5`.")
    answer = "5.0"
    evaluate_answer(answer)

def q_2_3_h():
    st.subheader(f"2.3: {chapters[2]['questions'][3]}")
    st.write("Strings are immutable. Supports Unicode by default. Triple quotes for multiline. f-strings (since 3.6) are preferred for interpolation.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('s = f"Value: {42}"\nprint(s)')
    with col2: st.code("Value: 42", language=None)
    st.write("Assign `snake_case` to a variable and print it.")
    answer = "snake_case"
    evaluate_answer(answer)

def q_2_4_h():
    st.subheader(f"2.4: {chapters[2]['questions'][4]}")
    st.write("Use `+` for concatenation, but prefer f-strings for performance and clarity. Strings are immutable, so repeated concatenation is O(n²).")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('a, b = "foo", "bar"\nprint(a + b)\nprint(f"{a}{b}")')
    with col2: st.code("foobar\nfoobar", language=None)
    st.write("Concatenate `py` and `thon` and print the result.")
    answer = "python"
    evaluate_answer(answer)

def q_2_5_h():
    st.subheader(f"2.5: {chapters[2]['questions'][5]}")
    st.write("`True` and `False` are singletons, subclasses of `int` (`True == 1`). Any object can be tested for truthiness. Use `is` for identity, `==` for equality.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('print(True + True)\nprint(bool([]))')
    with col2: st.code("2\nFalse", language=None)
    st.write("Print  any `True` statement to continue.")
    answer = "True"
    evaluate_answer(answer)

def q_3_1_h():
    st.subheader(f"3.1: {chapters[3]['questions'][1]}")
    st.write("Comparisons: `==`, `!=`, `<`, `>`, `<=`, `>=`. Chained comparisons are supported: `1 < x < 10`. `is` checks identity, not equality.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('print(1 < 2 < 3)\nprint(2 is 2)')
    with col2: st.code("True\nTrue", language=None)
    st.write("Evaluate `1 is not 2` and `1 is (not 2)` and print the results to continue.")
    answer = "True\nFalse"
    evaluate_answer(answer)

def q_3_2_h():
    st.subheader(f"3.2: {chapters[3]['questions'][2]}")
    st.write("Python uses indentation for blocks—no braces. Any expression can be used as a condition; false values: `0`, `''`, `[]`, `None`, etc.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('if []:\n    print("Not printed")\nelse:\n    print("Empty list is false")')
    with col2: st.code("Empty list is false", language=None)
    st.write("Print `Empty dict is false` if `{}` is false.")
    answer = "Empty dict is false"
    evaluate_answer(answer)

def q_3_3_h():
    st.subheader(f"3.3: {chapters[3]['questions'][3]}")
    st.write("`else` is required to be aligned with `if`. No switch/case in Python. Use `elif` for multiple branches.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('x = 0\nif x:\n    print("Truthy")\nelse:\n    print("False")')
    with col2: st.code("False", language=None)
    st.write("Print `False` if `0` is false.")
    answer = "False"
    evaluate_answer(answer)

def q_3_4_h():
    st.subheader(f"3.4: {chapters[3]['questions'][4]}")
    st.write("`elif` avoids deep nesting. Only the first true branch runs. No fallthrough.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('x = 10\nif x < 0:\n    print("Negative")\nelif x == 0:\n    print("Zero")\nelif x > 0:\n    print("Positive")')
    with col2: st.code("Positive", language=None)
    st.write("Print `Zero` if `x` is zero.")
    answer = "Zero"
    evaluate_answer(answer)

def q_3_5_h():
    st.subheader(f"3.5: {chapters[3]['questions'][5]}")
    st.write("`and`, `or`, `not` are short-circuiting. Any object can be used; returns the last evaluated operand, not necessarily a boolean.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('print([] or 42)\nprint(0 and 1)\nprint(not 0)')
    with col2: st.code("42\n0\nTrue", language=None)
    st.write("Evaluate `not 0` and print the result.")
    answer = "True"
    evaluate_answer(answer)

def q_3_6_h():
    st.subheader(f"3.6: {chapters[3]['questions'][6]}")
    st.write("Combine logical operators in conditions. Parentheses clarify precedence. `not` has higher precedence than `and`, which is higher than `or`.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('print(True or False and False)')
    with col2: st.code("True", language=None)
    st.write("Evaluate `True or False and False` and print the result.")
    answer = "True"
    evaluate_answer(answer)

def q_4_1_h():
    st.subheader(f"4.1: {chapters[4]['questions'][1]}")
    st.write("`for` loops iterate over any iterable. `range(stop)` yields ints from 0 to stop-1. Prefer `enumerate()` for index+value.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('for i in range(1, 5):\n    print(i)')
    with col2: st.code("1\n2\n3\n4", language=None)
    st.write("Print the numbers 1 to 3 using `range`.")
    answer = "1\n2\n3"
    evaluate_answer(answer)

def q_4_2_h():
    st.subheader(f"4.2: {chapters[4]['questions'][2]}")
    st.write("Iterating over lists yields elements, not indices. Use `for x in lst:`. For index, use `enumerate(lst)`.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('lst = [3, 1, 4]\nfor x in lst:\n    print(x, end=" ")')
    with col2: st.code("3 1 4 ", language=None)
    st.write("Given `lst = [3, 1, 4]`, print all elements separated by spaces.")
    answer = "3 1 4"
    evaluate_answer(answer)

def q_4_3_h():
    st.subheader(f"4.3: {chapters[4]['questions'][3]}")
    st.write("`while` loops run until the condition is false. `else` after `while` runs if the loop wasn't broken.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('n = 0\nwhile n < 2:\n    n += 1\nelse:\n    print("Done")')
    with col2: st.code("Done", language=None)
    st.write("Print `Done` after a `while` loop that counts to 2.")
    answer = "Done"
    evaluate_answer(answer)

def q_4_4_h():
    st.subheader(f"4.4: {chapters[4]['questions'][4]}")
    st.write("`range(start, stop, step)` supports negative steps. Slicing also supports steps: `lst[::2]`.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('for i in range(2, 7, 2):\n    print(i)')
    with col2: st.code("2\n4\n6", language=None)
    st.write("Print the even numbers from 2 to 6 (inclusive) using a step.")
    answer = "2\n4\n6"
    evaluate_answer(answer)

def q_4_5_h():
    st.subheader(f"4.5: {chapters[4]['questions'][5]}")
    st.write("`break` exits the nearest enclosing loop. `else` after a loop runs only if not it wasn't broken.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('for i in range(5):\n    if i == 2:\n        break\nprint("Loop exited")')
    with col2: st.code("Loop exited", language=None)
    st.write("Print `Loop exited` after breaking a loop.")
    answer = "Loop exited"
    evaluate_answer(answer)

def q_4_6_h():
    st.subheader(f"4.6: {chapters[4]['questions'][6]}")
    st.write("`continue` skips to the next iteration. Useful for filtering. Avoids deeply nested `if` statements.")
    col1, col2 = st.columns([0.6, 0.4])
    with col1: st.code('for i in range(1, 6):\n    if i % 2 == 0:\n        continue\n    print(i)')
    with col2: st.code("1\n3\n5", language=None)
    st.write("Print only even numbers from 1 to 7 using `continue`.")
    answer = "1\n3\n5"
    evaluate_answer(answer)