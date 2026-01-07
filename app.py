import streamlit as st
from calculator import Calculator
import math

def main():
    st.set_page_config(page_title="Calculator", page_icon="🧮")
    st.title("Nate's Simple Python Calculator")

    # Custom CSS for modern, premium look
    st.markdown("""
        <style>
        /* Main background */
        .stApp {
            background-color: #1e1e1e;
        }

        /* Title styling */
        h1, .stTitle {
            color: #ffffff !important;
        }
        
        /* Base Button styling (Numbers - Dark Grey) */
        div.stButton > button {
            background-color: #2d2d2d;
            color: #ffffff;
            border-radius: 15px;
            border: 1px solid #3d3d3d;
            height: 60px;
            font-size: 20px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        div.stButton > button:hover {
            background-color: #3d3d3d;
            border-color: #555;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        
        div.stButton > button:active {
            transform: translateY(1px);
        }

        /* ----- Function Buttons (Light Blue) ----- */
        /* ----- Function Buttons (Light Blue) ----- */
        /* Row 1 (Index 4): Cols 4, 5 (/, ^) */
        div[data-testid="stVerticalBlock"] > div:nth-of-type(4) [data-testid="stColumn"]:nth-of-type(4) button,
        div[data-testid="stVerticalBlock"] > div:nth-of-type(4) [data-testid="stColumn"]:nth-of-type(5) button {
            background-color: #4facfe !important;
            border-color: #4facfe !important;
        }

        /* Row 2 (Index 5): Cols 4, 5 (*, sqrt) */
        div[data-testid="stVerticalBlock"] > div:nth-of-type(5) [data-testid="stColumn"]:nth-of-type(4) button,
        div[data-testid="stVerticalBlock"] > div:nth-of-type(5) [data-testid="stColumn"]:nth-of-type(5) button {
            background-color: #4facfe !important;
            border-color: #4facfe !important;
        }

        /* Row 3 (Index 6): Cols 4, 5 (-, log) */
        div[data-testid="stVerticalBlock"] > div:nth-of-type(6) [data-testid="stColumn"]:nth-of-type(4) button,
        div[data-testid="stVerticalBlock"] > div:nth-of-type(6) [data-testid="stColumn"]:nth-of-type(5) button {
            background-color: #4facfe !important;
            border-color: #4facfe !important;
        }

        /* Row 4 (Index 7): Cols 1 (C), 4 (+), 5 (sin) */
        div[data-testid="stVerticalBlock"] > div:nth-of-type(7) [data-testid="stColumn"]:nth-of-type(1) button,
        div[data-testid="stVerticalBlock"] > div:nth-of-type(7) [data-testid="stColumn"]:nth-of-type(4) button,
        div[data-testid="stVerticalBlock"] > div:nth-of-type(7) [data-testid="stColumn"]:nth-of-type(5) button {
            background-color: #4facfe !important;
            border-color: #4facfe !important;
        }

        /* Row 5 (Index 8): All Cols (cos, tan, pi, e) */
        div[data-testid="stVerticalBlock"] > div:nth-of-type(8) button {
             background-color: #4facfe !important;
             border-color: #4facfe !important;
        }

        /* ----- Equals Button (Bright Blue) ----- */
        /* Row 4 (Index 7): Col 3 (=) */
        div[data-testid="stVerticalBlock"] > div:nth-of-type(7) [data-testid="stColumn"]:nth-of-type(3) button {
            background-color: #007AFF !important;
            border-color: #007AFF !important;
            font-weight: bold;
        }

        /* Hover effects for Blue buttons */
        div[data-testid="column"] button[style*="background-color: #4facfe"]:hover { 
            background-color: #63b2ff !important; 
        }
        
        /* Display Screen styling */
        .calc-display {
            background-color: #000000;
            color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            font-size: 42px;
            font-family: 'Roboto', sans-serif;
            text-align: right;
            margin-bottom: 25px;
            border: 1px solid #333;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize calculator logic
    calc = Calculator()

    # Session State Initialization
    if 'display' not in st.session_state:
        st.session_state.display = '0'
    if 'stored_value' not in st.session_state:
        st.session_state.stored_value = None
    if 'pending_operator' not in st.session_state:
        st.session_state.pending_operator = None
    if 'reset_next' not in st.session_state:
        st.session_state.reset_next = False

    # Logic functions (Callbacks)
    def input_number(digit):
        if st.session_state.reset_next:
            st.session_state.display = str(digit)
            st.session_state.reset_next = False
        else:
            if st.session_state.display == '0':
                st.session_state.display = str(digit)
            else:
                st.session_state.display += str(digit)

    def set_operator(op):
        if st.session_state.pending_operator is not None and not st.session_state.reset_next:
             calculate()
        
        st.session_state.stored_value = float(st.session_state.display)
        st.session_state.pending_operator = op
        st.session_state.reset_next = True

    def calculate():
        if st.session_state.pending_operator and st.session_state.stored_value is not None:
            try:
                current_val = float(st.session_state.display)
                result = 0
                op = st.session_state.pending_operator
                
                if op == '+':
                    result = calc.add(st.session_state.stored_value, current_val)
                elif op == '-':
                    result = calc.subtract(st.session_state.stored_value, current_val)
                elif op == '*':
                    result = calc.multiply(st.session_state.stored_value, current_val)
                elif op == '/':
                    result = calc.divide(st.session_state.stored_value, current_val)
                elif op == '^':
                    result = calc.power(st.session_state.stored_value, current_val)
                
                # Format result
                if result.is_integer():
                    st.session_state.display = str(int(result))
                else:
                    st.session_state.display = str(result)
                
                st.session_state.stored_value = None
                st.session_state.pending_operator = None
                st.session_state.reset_next = True
                
            except Exception as e:
                st.session_state.display = "Error"
                st.session_state.stored_value = None
                st.session_state.pending_operator = None
                st.session_state.reset_next = True

    def clear():
        st.session_state.display = '0'
        st.session_state.stored_value = None
        st.session_state.pending_operator = None
        st.session_state.reset_next = False

    # Unary Operations (Immediate execution)
    def unary_operation(op_func):
        try:
            current_val = float(st.session_state.display)
            result = op_func(current_val)
             # Format result
            if result.is_integer():
                st.session_state.display = str(int(result))
            else:
                st.session_state.display = str(result)
            st.session_state.reset_next = True
        except Exception as e:
             st.session_state.display = "Error"
             st.session_state.reset_next = True

    # UI Layout
    
    # Display Screen
    st.markdown(
        f"""
        <div class="calc-display">
            {st.session_state.display}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Grid Layout - 5 columns for Scientific Calculator
    # Row 1: 7, 8, 9, /, ^ (Power)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("7", on_click=input_number, args=('7',), use_container_width=True)
    c2.button("8", on_click=input_number, args=('8',), use_container_width=True)
    c3.button("9", on_click=input_number, args=('9',), use_container_width=True)
    c4.button("÷", on_click=set_operator, args=('/',), use_container_width=True)
    c5.button("^", on_click=set_operator, args=('^',), use_container_width=True)

    # Row 2: 4, 5, 6, *, √ (Sqrt)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("4", on_click=input_number, args=('4',), use_container_width=True)
    c2.button("5", on_click=input_number, args=('5',), use_container_width=True)
    c3.button("6", on_click=input_number, args=('6',), use_container_width=True)
    c4.button("×", on_click=set_operator, args=('*',), use_container_width=True)
    c5.button("√", on_click=unary_operation, args=(calc.sqrt,), use_container_width=True)

    # Row 3: 1, 2, 3, -, log
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("1", on_click=input_number, args=('1',), use_container_width=True)
    c2.button("2", on_click=input_number, args=('2',), use_container_width=True)
    c3.button("3", on_click=input_number, args=('3',), use_container_width=True)
    c4.button("−", on_click=set_operator, args=('-',), use_container_width=True)
    c5.button("log", on_click=unary_operation, args=(calc.log,), use_container_width=True)

    # Row 4: C, 0, =, +, Const (pi, e - simplified to just constants inputs for now or maybe trig)
    # Let's do Trig: sin, cos, tan
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("C", on_click=clear, use_container_width=True)
    c2.button("0", on_click=input_number, args=('0',), use_container_width=True)
    c3.button("=", on_click=calculate, use_container_width=True)
    c4.button("＋", on_click=set_operator, args=('+',), use_container_width=True)
    c5.button("sin", on_click=unary_operation, args=(calc.sin,), use_container_width=True)

    # Row 5: Extra Scientific: cos, tan, pi, e
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("cos", on_click=unary_operation, args=(calc.cos,), use_container_width=True)
    c2.button("tan", on_click=unary_operation, args=(calc.tan,), use_container_width=True)
    c3.button("π", on_click=input_number, args=(math.pi,), use_container_width=True)
    c4.button("e", on_click=input_number, args=(math.e,), use_container_width=True)
    # Empty 5th button or could be something else
    c5.empty()

if __name__ == "__main__":
    main()
