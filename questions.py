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
                "questions": { #TODO: innacurate, update later
                    1: "integers",
                    2: "floats",
                    3: "strings",
                    4: "boolean"
                }
                },
            3: {"title": "If-else statements",
                "description": "Learn how to use if-else statements to control the flow of your program.",
                "questions": { #TODO: innacurate, update later
                    1: "if statements",
                    2: "if-else statements",
                    3: "if-elif-else statements",
                    4: "Nested if statements",
                    5: "Logical operators",
                    6: "Boolean operators"
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


def q_2_5():
        st.subheader("2.5: String Concatenation")
        st.write("In Python we can concatenate strings using the + operator. For example:")
        st.write("Two strings are joined to create a message.")

        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("greeting = \"Hey\"\nname=\"Friend\"\nprint(greeting + name))")
        with col2: st.code("Hey Friend", language=None)

        answer = "minecraft"
        st.session_state.editor_content = "animals = [\"cat\",\"dog\",\"snake\"]"
        st.session_state.editor_content = "part1=\"mine\"\n"+\
                    "part2=\"craft\"\n"
        st.write(f"Combine part1 and part2 in order to print\"{answer}\"")
        evaluate_answer(answer)


def q_3_1():
        st.subheader("3.1: Basic Comparisons")
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
        st.subheader("3.1: Logical Operators")
        st.write("There three important logical operators. They are AND, OR and NOT.")
        st.write("The operator AND is for when both conditions must be true. For Example:")
        st.write("When one is true and the other is false, it becomes false. For Example:")
        col1, col2 = st.columns([0.6, 0.4])
        with col1: st.code("greeting = \"Hey\"\nname=\"Friend\"\nprint(greeting + name))")
        with col2: st.code("Hey Friend", language=None)

        answer = "minecraft"
        st.session_state.editor_content = "animals = [\"cat\",\"dog\",\"snake\"]"
        st.session_state.editor_content = "part1=\"mine\"\n"+\
                    "part2=\"craft\"\n"
        st.write(f"Combine part1 and part2 in order to print\"{answer}\"")
        evaluate_answer(answer)
