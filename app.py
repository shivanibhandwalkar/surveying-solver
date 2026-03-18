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

            # ✅ FIX: correct conversion
            total_decl_min = abs(decl) * 60
            deg = int(total_decl_min // 60)
            minute = int(total_decl_min % 60)

        # ---------------- STEPS ----------------
        st.subheader("📋 Step-by-Step Solution")

        if mode == "Custom Input":
            st.write("**STEP 1:** User Provided Declination")
            st.write(f"Declination = {deg}° {minute}′ {direction}")
        else:
            st.write("**STEP 1:** Given Data")
            st.write(f"Magnetic Bearing = {mag_deg}° {mag_min}′")

            st.write("**STEP 2:** Formula")
            st.write("Magnetic Declination = 180° − Magnetic Bearing (if towards south)")
            st.write("OR Magnetic Declination = Magnetic Bearing (if towards north)")

        # FINAL RESULT
        st.success(f"Final Answer: {deg}° {minute}′ {direction}")

        # ✅ TOTAL MINUTES (correct)
        total_minutes = (deg * 60) + minute
        st.info(f"Declination in Minutes: {total_minutes:.2f}′")

        # ---------------- GRAPH ----------------
        angle = deg + minute/60

       # ✅ Correct reference: from True North
        if direction == "E":
          magnetic_angle = 90 - angle   
        else:
          magnetic_angle = 90 + angle   

        fig, ax = plt.subplots(figsize=(9,7)) 
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')

        # TRUE NORTH
        ax.plot([0, 0], [0, 5], linewidth=2)
        ax.text(0, 5.2, "True North", color='white', ha='center', fontsize=8)

        # MAGNETIC NORTH
        # Correct orientation (angle from North)
        rad = math.radians(angle)

        if direction == "E":
           x = 5 * math.sin(rad)
           y = 5 * math.cos(rad)
        else:
           x = -5 * math.sin(rad)
           y = 5 * math.cos(rad)

        ax.plot([0, x], [0, y], linewidth=2)
        ax.text(x, y, "Magnetic North", color='white', fontsize=8)

        # ARC
        theta = np.linspace(0, math.radians(abs(angle)), 100)

        if direction == "E":
            arc_x = 1.5 * np.sin(theta)
            arc_y = 1.5 * np.cos(theta)
        else:
            arc_x = -1.5 * np.sin(theta)
            arc_y = 1.5 * np.cos(theta)

        ax.plot(arc_x, arc_y)

        # ✅ LABEL WITH MINUTES ALSO
        ax.text(
            arc_x[len(arc_x)//2],
            arc_y[len(arc_y)//2],
            f"{deg}°{minute}′\n({total_minutes:.1f}′)",
            color='yellow',
            fontsize=4,
            ha='center'
        )

        # STATION
        ax.scatter(0, 0, s=60)
        ax.text(0, -0.5, "Station", color='white', ha='center', fontsize=4)

        # COMPASS
        ax.text(0, 5.6, "N", color='white', ha='center', fontsize=4)
        ax.text(0, -5.6, "S", color='white', ha='center', fontsize=4)
        ax.text(5.6, 0, "E", color='white', fontsize=8)
        ax.text(-5.6, 0, "W", color='white', fontsize=8)

        # STYLE
        ax.set_title("Magnetic Declination Diagram", color='white', fontsize=10)

        ax.tick_params(colors='white', labelsize=4)
        for spine in ax.spines.values():
            spine.set_color('white')

        ax.grid(True, linestyle='--', linewidth=0.4, color='gray')
        ax.set_aspect('equal')

        plt.tight_layout()

        st.pyplot(fig)