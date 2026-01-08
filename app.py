import streamlit as st
from calculator import Calculator
import math
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def main():
    st.set_page_config(page_title="Catculator", page_icon="🐱")
    st.title("Catculator")
    
    # Load background image
    try:
        bin_str = get_base64_of_bin_file("cat_bg.png")
    except Exception:
        st.error("Could not load cat background.")
        bin_str = ""

    # Custom CSS for Catculator (Grid and Buttons)
    st.markdown("""
        <style>
        /* Lock everything to fixed dimensions */
        .stApp {
            background-color: #87CEEB !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            min-height: 100vh !important;
        }

        .block-container {
            position: relative !important;
            width: 450px !important;
            height: 800px !important;
            max-width: 450px !important;
            max-height: 800px !important;
            min-width: 450px !important;
            min-height: 800px !important;
            padding: 0 !important;
            margin: 20px auto !important;
            background-image: url("data:image/png;base64,__BG_IMAGE_B64__");
            background-size: 100% 100%;
            background-repeat: no-repeat;
            background-position: center;
            overflow: hidden !important;
        }

        /* Hide default Streamlit title and padding */
        h1, .stTitle { display: none !important; }
        .stMainBlockContainer { padding: 0 !important; }

        /* Catculator Title - Positioned at top */
        .catculator-title {
            position: absolute !important;
            top: 10px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            font-family: 'Comic Sans MS', cursive, sans-serif !important;
            font-size: 36px !important;
            font-weight: bold !important;
            color: #663300 !important;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.8) !important;
            z-index: 1001 !important;
            white-space: nowrap !important;
            display: inline-block !important;
        }

        /* Display Screen - Absolutely positioned on cat's forehead */
        .calc-display {
            position: absolute !important;
            top: 165px !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            width: 250px !important;
            height: 55px !important;

            background-color: rgba(255, 255, 255, 0.95) !important;
            color: #333 !important;
            padding: 8px 15px !important;
            border-radius: 15px !important;
            font-size: 28px !important;
            font-family: 'Comic Sans MS', sans-serif !important;
            font-weight: bold !important;
            text-align: right !important;
            border: 3px solid #663300 !important;
            box-shadow: 0 3px 8px rgba(0,0,0,0.3) !important;
            z-index: 1000 !important;

            display: flex !important;
            align-items: center !important;
            justify-content: flex-end !important;
            overflow: hidden !important;
        }

        /* Large invisible spacer to push buttons down to belly */
        .belly-spacer {
            height: 340px !important;
            min-height: 340px !important;
            max-height: 340px !important;
        }

        /* Force Grid Alignment */
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            white-space: nowrap !important;
            justify-content: center !important;
            gap: 6px !important;
            margin-bottom: 6px !important;
            padding-left: 20px !important;
            padding-right: 20px !important;
        }

        div[data-testid="stColumn"] {
            min-width: 64px !important;
            max-width: 64px !important;
            flex: 0 0 64px !important;
        }

        /* Button styling */
        div[data-testid="stColumn"] button {
            width: 60px !important;
            height: 60px !important;
            min-height: 60px !important;
            max-height: 60px !important;
            border-radius: 50% !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: 2px solid rgba(0,0,0,0.3) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.4) !important;
            font-size: 20px !important;
            font-weight: bold !important;
            margin: 0 auto !important;
            cursor: pointer !important;
        }

        /* Number buttons - Brown */
        button[kind="secondary"], div[data-testid="baseButton-secondary"] > button {
            background-color: #A0522D !important;
            color: white !important;
            border-color: #5D4037 !important;
        }

        /* Function buttons - Blue */
        button[kind="primary"], div[data-testid="baseButton-primary"] > button {
            background-color: #6495ED !important;
            color: white !important;
            border-color: #004085 !important;
        }

        /* Equals button - Darker blue */
        div[data-testid="stHorizontalBlock"]:nth-of-type(4) [data-testid="stColumn"]:nth-of-type(3) button {
            background-color: #4169E1 !important;
            border-color: #002a80 !important;
        }
        </style>
    """.replace("__BG_IMAGE_B64__", bin_str), unsafe_allow_html=True)


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

    # Title (Absolutely positioned at top)
    st.markdown('<div class="catculator-title">🐱 Catculator 🐱</div>', unsafe_allow_html=True)

    # Display Screen (Absolutely positioned on forehead)
    st.markdown(
        f"""
        <div class="calc-display">
            {st.session_state.display}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Spacer to push buttons down to cat's belly
    st.markdown('<div class="belly-spacer"></div>', unsafe_allow_html=True)

    # Grid Layout - 5 columns for Scientific Calculator
    # Row 1: 7, 8, 9, /, ^ (Power)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("7", on_click=input_number, args=('7',))
    c2.button("8", on_click=input_number, args=('8',))
    c3.button("9", on_click=input_number, args=('9',))
    c4.button("÷", on_click=set_operator, args=('/',), type="primary")
    c5.button("^", on_click=set_operator, args=('^',), type="primary")

    # Row 2: 4, 5, 6, *, √ (Sqrt)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("4", on_click=input_number, args=('4',))
    c2.button("5", on_click=input_number, args=('5',))
    c3.button("6", on_click=input_number, args=('6',))
    c4.button("×", on_click=set_operator, args=('*',), type="primary")
    c5.button("√", on_click=unary_operation, args=(calc.sqrt,), type="primary")

    # Row 3: 1, 2, 3, -, log
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("1", on_click=input_number, args=('1',))
    c2.button("2", on_click=input_number, args=('2',))
    c3.button("3", on_click=input_number, args=('3',))
    c4.button("−", on_click=set_operator, args=('-',), type="primary")
    c5.button("log", on_click=unary_operation, args=(calc.log,), type="primary")

    # Row 4: C, 0, =, +, sin
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("C", on_click=clear)
    c2.button("0", on_click=input_number, args=('0',))
    c3.button("=", on_click=calculate, type="primary")
    c4.button("＋", on_click=set_operator, args=('+',), type="primary")
    c5.button("sin", on_click=unary_operation, args=(calc.sin,), type="primary")

    # Row 5: Extra Scientific: cos, tan, pi, e
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.button("cos", on_click=unary_operation, args=(calc.cos,), type="primary")
    c2.button("tan", on_click=unary_operation, args=(calc.tan,), type="primary")
    c3.button("π", on_click=input_number, args=(math.pi,), type="primary")
    c4.button("e", on_click=input_number, args=(math.e,), type="primary")
    # Empty 5th button
    c5.empty()

if __name__ == "__main__":
    main()
