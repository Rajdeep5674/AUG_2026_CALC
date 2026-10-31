import streamlit as st
from datetime import datetime
from math import prod, isfinite
from html import escape

st.set_page_config(page_title="Smart Calculator", page_icon="🧮", layout="centered")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#0B1220,#172B4D); color:#fff;}
.block-container {max-width:850px; padding-top:2rem; padding-bottom:3rem;}
.main-title {text-align:center; font-size:42px; font-weight:800; color:#fff; margin-bottom:5px;}
.subtitle {text-align:center; font-size:15px; color:#A9B9D0; margin-bottom:30px;}
.section-title {font-size:20px; font-weight:700; color:#fff; margin:15px 0;}
.result-box {background:linear-gradient(120deg,#2563EB,#7C3AED); padding:25px; border-radius:16px; text-align:center; margin:15px 0;}
.result-label {font-size:14px; color:#E0E7FF; margin-bottom:10px; overflow-wrap:anywhere;}
.result-number {font-size:36px; font-weight:800; color:white; overflow-wrap:anywhere;}
.stButton > button[kind="primary"] {background:linear-gradient(90deg,#2563EB,#7C3AED); color:white; border:none; border-radius:10px; font-weight:700; height:48px;}
.stButton > button {border-radius:10px; font-weight:600; height:45px;}
div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input {border-radius:10px;}
div[data-testid="stForm"] {background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.12); border-radius:16px; padding:20px;}
#MainMenu {visibility:hidden;} footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None


def parse_values(text):
    parts = text.split(",")
    if not text.strip() or any(not part.strip() for part in parts):
        raise ValueError("Enter valid numbers separated by commas.")
    numbers = [float(part.strip()) for part in parts]
    if not all(isfinite(number) for number in numbers):
        raise ValueError("Please enter finite numbers only.")
    return numbers


def fmt(number):
    return f"{number:,.10g}"


st.markdown('<div class="main-title">🧮 Smart Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A modern and intuitive arithmetic calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Choose an Operation</div>', unsafe_allow_html=True)

operations = {"➕ Addition": "+", "➖ Subtraction": "-", "✖️ Multiplication": "*", "➗ Division": "/"}
selected_operation = st.selectbox("Arithmetic Operation", list(operations), label_visibility="collapsed")
operator = operations[selected_operation]

with st.form("calculator_form"):
    if operator in ("+", "*"):
        st.markdown("#### Enter Multiple Numbers")
        values = st.text_input("Numbers", placeholder="Example: 10, 20, 30, 40", help="Separate numbers using commas.")
        st.caption("Enter as many numbers as needed, separated by commas.")
    else:
        st.markdown("#### Enter Two Numbers")
        col1, col2 = st.columns(2)
        with col1:
            val1 = st.number_input("First Number", value=0.0, format="%.2f")
        with col2:
            val2 = st.number_input("Second Number", value=0.0, format="%.2f")
    calculate = st.form_submit_button("Calculate Result", type="primary", use_container_width=True)

if calculate:
    try:
        results = []
        if operator == "+":
            numbers = parse_values(values)
            results.append((" + ".join(fmt(x) for x in numbers), sum(numbers)))
        elif operator == "-":
            results.append((f"{fmt(val1)} - {fmt(val2)}", val1 - val2))
            results.append((f"{fmt(val2)} - {fmt(val1)}", val2 - val1))
        elif operator == "*":
            numbers = parse_values(values)
            results.append((" × ".join(fmt(x) for x in numbers), prod(numbers)))
        else:
            if val2 == 0:
                raise ZeroDivisionError("You cannot divide by zero.")
            results.append((f"{fmt(val1)} ÷ {fmt(val2)}", val1 / val2))

        if not all(isfinite(result) for _, result in results):
            raise ValueError("The result is too large to display.")

        st.session_state.last_result = results
        for expression, result in results:
            st.session_state.history.insert(0, {
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Operation": selected_operation,
                "Expression": expression,
                "Result": fmt(result),
            })
    except (ValueError, OverflowError, ZeroDivisionError) as exc:
        st.session_state.last_result = None
        st.error(str(exc))

if st.session_state.last_result is not None:
    st.markdown('<div class="section-title">Calculation Result</div>', unsafe_allow_html=True)
    for expression, result in st.session_state.last_result:
        st.markdown(f'<div class="result-box"><div class="result-label">{escape(expression)}</div><div class="result-number">{escape(fmt(result))}</div></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="section-title">🕘 Calculation History</div>', unsafe_allow_html=True)
if st.session_state.history:
    st.dataframe(st.session_state.history, use_container_width=True, hide_index=True)
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.session_state.last_result = None
        st.rerun()
else:
    st.info("No calculations yet. Start calculating!")

st.markdown("---")
st.markdown('<p style="text-align:center;color:#94A3B8;font-size:13px">Smart Calculator | Built with Python & Streamlit</p>', unsafe_allow_html=True)
