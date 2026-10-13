import streamlit as st
import pandas as pd
from metrics_engine import MetricsAnalyzer

st.set_page_config(
    page_title="Static Code Health & Refactoring Advisor",
    page_icon="🎨",
    layout="wide"
)

# Custom Styling for vibrant headers and card styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #FF4B4B;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-text {
        color: #a3a8b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎨 Static Code Health & Refactoring Advisor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Interactive Software Metrics Assessment, Visual Complexity Breakdown, and Refactoring Advisor.</p>', unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.header("🎛️ Control Panel")
uploaded_file = st.sidebar.file_uploader("Upload Python (.py) File", type=["py"])

# Interactive filter option in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Display Preferences")
show_code = st.sidebar.checkbox("Show Source Code Viewer", value=True)
risk_filter = st.sidebar.selectbox("Filter Complexity Table by Risk", ["All Functions", "High Risk Only (>10)", "Safe Only (<=10)"])

if uploaded_file is not None:
    source_code = uploaded_file.read().decode("utf-8")
    
    if show_code:
        with st.expander("📄 View Uploaded Source Code", expanded=False):
            st.code(source_code, language="python")
        
    analyzer = MetricsAnalyzer(source_code)
    results = analyzer.analyze_all()
    
    # --- 1. SYNTAX ERROR BANNER ---
    if results.get("syntax_error") is not None:
        err = results["syntax_error"]
        st.error("🚨 **Syntax Error Compilation Blocked!**")
        st.markdown(f"""
        - **Error Message:** `{err['msg']}`
        - **Line Number:** `{err['line']}`
        - **Snippet:** `{err['text']}`
        """)
        st.warning("⚠️ Please fix the syntax error in your code file to view metrics.")
        
    else:
        raw = results.get("raw", {})
        halstead = results.get("halstead", {})
        mi_score = results.get("maintainability_index", 0.0)
        avg_complexity = results.get("avg_complexity", 0.0)
        complexity_details = results.get("complexity_details", [])

        # --- 2. PROJECT HEALTH OVERVIEW CARDS ---
        st.markdown("### 📌 Project Health Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("📊 Total / Effective LOC", f"{raw.get('loc', 0)} / {raw.get('sloc', 0)}", delta=f"Blanks: {raw.get('blank', 0)}")
        col2.metric("📝 Logical Lines (LLOC)", raw.get('lloc', 0))
        col3.metric("⚡ Avg Complexity", avg_complexity, delta="Target: < 10" if avg_complexity <= 10 else "High", delta_color="normal" if avg_complexity <= 10 else "inverse")
        
        mi_color = "normal" if mi_score >= 65 else "inverse"
        col4.metric("🛡️ Maintainability Index", f"{mi_score} / 100", delta="Healthy (>=65)" if mi_score >= 65 else "Action Required", delta_color=mi_color)

        # --- 3. HALSTEAD METRICS SECTION ---
        st.markdown("---")
        st.markdown("### 📐 Halstead Complexity & Code Density")
        
        h1, h2, h3, h4, h5 = st.columns(5)
        h1.metric("Volume (V)", halstead.get("volume", 0))
        h2.metric("Difficulty (D)", halstead.get("difficulty", 0))
        h3.metric("Effort (E)", halstead.get("effort", 0))
        h4.metric("Est. Bugs (B)", halstead.get("bugs", 0))
        h5.metric("Comment Density", f"{raw.get('comment_percent', 0.0)}%")

        # --- 4. INTERACTIVE FUNCTION COMPLEXITY TABLE & CHARTS ---
        st.markdown("---")
        st.markdown("### 🔍 Function-Level Complexity Analysis")
        
        if complexity_details and "error" not in complexity_details[0]:
            df_cc = pd.DataFrame(complexity_details)
            
            # Apply interactive filtering from sidebar
            if risk_filter == "High Risk Only (>10)":
                df_filtered = df_cc[df_cc["Complexity"] > 10]
            elif risk_filter == "Safe Only (<=10)":
                df_filtered = df_cc[df_cc["Complexity"] <= 10]
            else:
                df_filtered = df_cc

            # Layout columns for Table and Visual Bar Chart
            table_col, chart_col = st.columns([1.2, 1])
            
            with table_col:
                st.markdown("**Function Breakdown Table**")
                st.dataframe(df_filtered, use_container_width=True, hide_index=True)

            with chart_col:
                st.markdown("**Complexity Visualizer**")
                if not df_cc.empty:
                    chart_data = df_cc.set_index("Function Name")["Complexity"]
                    st.bar_chart(chart_data, color="#FF4B4B")
                else:
                    st.info("No data available for charting.")
            
            # --- 5. REFACTORING ADVISOR & TEMPLATES ---
            st.markdown("---")
            st.markdown("### 💡 Refactoring Advisor & Improvised Code Templates")
            risk_found = False
            
            for block in complexity_details:
                comp = block.get("Complexity", 0)
                name = block.get("Function Name", "Unknown")
                rank = block.get("Rank", "A")
                
                if comp > 10:
                    risk_found = True
                    st.error(f"🔴 **High Risk Function Detected ('{name}')**: Complexity score is **{comp}** (Rank: **{rank}**). Exceeds safe threshold (>10).")
                    
                    with st.expander(f"✨ Open Improvised Refactoring Template for '{name}'"):
                        st.markdown("**Diagnosis:** Excessive nested conditionals (`if/else` ladders) lead to high cognitive load and bug vulnerability.")
                        st.markdown("**Refactoring Strategy:** Apply **Guard Clauses** to return early or split logic into auxiliary helpers.")
                        st.code(f"""
# --- RECOMMENDED CLEAN ARCHITECTURE FOR {name} ---
def {name}_refactored(*args, **kwargs):
    # 1. Early exit guard clauses
    # if not precondition:
    #     return default_response
    
    # 2. Flattened execution flow
    cleaned_result = process_modular_steps(*args)
    return cleaned_result
                        """, language="python")
                elif comp > 5:
                    st.warning(f"🟡 **Moderate Risk Function ('{name}')**: Complexity score is **{comp}** (Rank: **{rank}**). Monitor during maintenance.")
                    
            if not risk_found:
                st.success("🟢 Excellent! All evaluated functions are within safe cyclomatic complexity limits.")
        else:
            st.info("ℹ️ No functions detected in this file.")

else:
    st.info("👈 Please upload a Python file using the sidebar control panel to initiate analysis.")