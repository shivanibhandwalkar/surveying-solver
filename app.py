import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# PAGE CONFIG
st.set_page_config(page_title="Surveying Solver", layout="wide")

# DARK STYLE
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 Surveying Problem 4 Solver")

# LAYOUT
col1, col2 = st.columns([1,2])

# ---------------- LEFT SIDE INPUT ----------------
with col1:
    st.header("⚙️ Input Parameters")

    mode = st.radio("Select Mode", ["Default", "Custom Input"])

    mag_deg = st.number_input("Degree", 0, 360, 175)
    mag_min = st.number_input("Minutes", 0, 59, 30)

    if mode == "Custom Input":
        st.subheader("Enter Declination Directly")
        decl_deg_input = st.number_input("Declination Degree", 0, 180, 5)
        decl_min_input = st.number_input("Declination Minutes", 0, 59, 30)
        direction_input = st.selectbox("Direction", ["E", "W"])

    solve_btn = st.button("Solve")

# ---------------- RIGHT SIDE OUTPUT ----------------
with col2:
    st.header("📊 Output & Diagram")

    if solve_btn:

        # -------- CALCULATION --------
        if mode == "Custom Input":
            deg = decl_deg_input
            minute = decl_min_input
            direction = direction_input
        else:
            total_mag = mag_deg + mag_min/60

            if total_mag > 180:
                decl = 180 - total_mag
                direction = "E"
            else:
                decl = total_mag
                direction = "W"

            total_decl_min = abs(decl) * 60
            deg = int(total_decl_min // 60)
            minute = int(total_decl_min % 60)

        # -------- OUTPUT --------
        st.subheader("📋 Step-by-Step Solution")

        if mode == "Custom Input":
            st.write(f"Declination = {deg}° {minute}′ {direction}")
        else:
            st.write(f"Magnetic Bearing = {mag_deg}° {mag_min}′")

        st.success(f"Final Answer: {deg}° {minute}′ {direction}")

        total_minutes = deg * 60 + minute
        st.info(f"Declination in Minutes: {total_minutes:.2f}′")

        # ---------------- GRAPH ----------------
        angle = deg + minute/60
        rad = math.radians(angle)

        fig, ax = plt.subplots(figsize=(9,7))

        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')

        # TRUE NORTH
        ax.plot([0, 0], [0, 6], linewidth=2)
        ax.text(0, 6.3, "True North", color='white', ha='center', fontsize=8)

        # MAGNETIC NORTH
        if direction == "E":
            x = 6 * math.sin(rad)
            y = 6 * math.cos(rad)
        else:
            x = -6 * math.sin(rad)
            y = 6 * math.cos(rad)

        ax.plot([0, x], [0, y], linewidth=2)
        ax.text(x, y, "Magnetic North", color='white', fontsize=8)

        # ARC
        theta = np.linspace(0, rad, 100)

        if direction == "E":
            arc_x = 2 * np.sin(theta)
            arc_y = 2 * np.cos(theta)
        else:
            arc_x = -2 * np.sin(theta)
            arc_y = 2 * np.cos(theta)

        ax.plot(arc_x, arc_y, linewidth=1.2)

        # LABEL
        mid = len(arc_x)//2
        ax.text(
            arc_x[mid]*1.1,
            arc_y[mid]*1.1,
            f"{deg}°{minute}′\n({total_minutes:.1f}′)",
            color='yellow',
            fontsize=7,
            ha='center'
        )

        # STATION
        ax.scatter(0, 0, s=70)
        ax.text(0, -0.7, "Station", color='white', ha='center', fontsize=7)

        # COMPASS
        ax.text(0, 7.2, "N", color='white', ha='center', fontsize=7)
        ax.text(0, -7.2, "S", color='white', ha='center', fontsize=7)
        ax.text(7.2, 0, "E", color='white', fontsize=7)
        ax.text(-7.2, 0, "W", color='white', fontsize=7)

        # STYLE
        ax.set_title("Magnetic Declination Diagram", color='white', fontsize=9)

        ax.tick_params(colors='white', labelsize=5)

        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_linewidth(0.8)

        ax.grid(True, linestyle='--', linewidth=0.3, color='gray', alpha=0.6)
        ax.set_aspect('equal')

        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)

        plt.tight_layout()

        st.pyplot(fig)