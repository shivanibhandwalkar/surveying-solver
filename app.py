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

        # -------- CALCULATION (FIXED) --------
        if mode == "Custom Input":
            deg = decl_deg_input
            minute = decl_min_input
            direction = direction_input
        else:
            total_mag = mag_deg + mag_min / 60

            # ✅ Correct formula
            decl = 180 - total_mag

            # Direction
            if decl >= 0:
                direction = "E"
            else:
                direction = "W"

            # Convert to DMS
            decl = abs(decl)
            deg = int(decl)
            minute = int((decl - deg) * 60)

        # -------- OUTPUT --------
        st.subheader("📋 Step-by-Step Solution")

        if mode == "Custom Input":
            st.write(f"Declination = {deg}° {minute}′ {direction}")
        else:
            st.write(f"Magnetic Bearing = {mag_deg}° {mag_min}′")

        st.success(f"Final Answer: {deg}° {minute}′ {direction}")

        total_minutes = deg * 60 + minute
        st.info(f"Declination in Minutes: {total_minutes:.2f}′")

        # ---------------- BETTER COMPASS GRAPH ----------------
        angle = deg + minute / 60
        rad = math.radians(angle)

        fig, ax = plt.subplots(figsize=(7,7), subplot_kw={'projection': 'polar'})

        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')

        # Set 0° at North and clockwise direction
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)

        # Hide radial labels
        ax.set_yticklabels([])

        # Compass directions
        ax.set_xticks(np.radians([0, 90, 180, 270]))
        ax.set_xticklabels(['N', 'E', 'S', 'W'], color='white')

        # TRUE NORTH
        ax.plot([0, 0], [0, 1], linewidth=2)
        ax.text(0, 1.1, "True North", color='white', ha='center', fontsize=8)

        # MAGNETIC NORTH
        if direction == "E":
            mag_angle = rad
        else:
            mag_angle = -rad

        ax.plot([mag_angle, mag_angle], [0, 1], linewidth=2)
        ax.text(mag_angle, 1.1, "Magnetic North", color='white', ha='center', fontsize=8)

        # DECLINATION ARC
        theta = np.linspace(0, mag_angle, 200)
        r = np.ones_like(theta) * 0.5
        ax.plot(theta, r, linewidth=2)

        # LABEL
        ax.text(
            mag_angle/2 if mag_angle != 0 else 0,
            0.6,
            f"{deg}°{minute}′\n{direction}",
            color='yellow',
            ha='center',
            fontsize=9
        )

        # STATION
        ax.scatter(0, 0, s=50)
        ax.text(0, 0.1, "Station", color='white', ha='center', fontsize=7)

        # STYLE
        ax.set_title("Compass Declination Diagram", color='white', fontsize=10)

        plt.tight_layout()
        st.pyplot(fig)