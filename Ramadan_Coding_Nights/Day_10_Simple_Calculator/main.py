import streamlit as st

def main():
    st.title("Simple Calculator")
    st.write("Enter two numbers and choose an operation")
    col1, col2 = st.columns(2)

    with col1:
        num1 = st.number_input("Enter first number", value=0.0)

    with col2:
        num2 = st.number_input("Enter second number", value=0.0)

    operation = st.selectbox(
        "Choose an operation",
        ["Addition (+)", "Subtraction (-)", "Multiplication (*)", "Division (/)"]
        )
    
    if st.button("Calculate"):
        try:
            if operation == "Addition (+)":
                result = num1 + num2
                symbol = "+"
            elif operation == "Subtraction (-)":
                result = num1 - num2
                symbol = "-"
            elif operation == "Multiplication (*)":
                result = num1 * num2
                symbol = "x"
            else:
                if num2 == 0:
                    st.error("Cannot divide by zero")
                    return
                result = num1 / num2
                symbol = "/"

            st.success(f"{num1} {symbol} {num2} = {result}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
if __name__ == "__main__":
    main()
