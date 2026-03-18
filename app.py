import streamlit as st # pyright: ignore[reportMissingImports]
import numpy as np # pyright: ignore[reportMissingImports]
import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]
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

    # 🔹 MODE SELECTION
    mode = st.radio("Select Mode", ["Default", "Custom Input"])

    # 🔹 DEFAULT INPUTS (existing)
    mag_deg = st.number_input("Degree", 0, 360, 175)
    mag_min = st.number_input("Minutes", 0, 59, 30)

    # 🔹 CUSTOM INPUTS (new)
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

        # 🔹 CUSTOM MODE LOGIC
        if mode == "Custom Input":
            deg = decl_deg_input
            minute = decl_min_input
            direction = direction_input

        # 🔹 DEFAULT MODE LOGIC (unchanged, just inside else)
        else:
            total_mag = mag_deg + mag_min/60

            if total_mag > 180:
                decl = 180 - total_mag
                direction = "E"
            else:
                decl = total_mag
                direction = "W"

            deg = int(abs(decl))
            minute = int((abs(decl) - deg) * 60)

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

            st.write("**STEP 3:** Calculation")
            if direction == "E":
                st.write(f"Declination = 180° − {mag_deg}° {mag_min}′")
            else:
                st.write(f"Declination = {mag_deg}° {mag_min}′")

        # FINAL RESULT
        st.success(f"Final Answer: {deg}° {minute}′ {direction}")

        # 🔹 CONVERT TO MINUTES (added)
        total_minutes = deg * 60 + minute
        st.info(f"Declination in Minutes: {total_minutes}′")

        # ---------------- GRAPH ----------------
        angle = deg + minute/60

        if direction == "E":
            magnetic_angle = 90 - angle
        else:
            magnetic_angle = 90 + angle

        fig, ax = plt.subplots(figsize=(7,6))

        # DARK BACKGROUND
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')

        # TRUE NORTH
        ax.plot([0, 0], [0, 5], color='#4FC3F7', linewidth=2)
        ax.text(0, 5.3, "True North", color='white', ha='center')

        # MAGNETIC NORTH
        x = 5 * math.cos(math.radians(magnetic_angle))
        y = 5 * math.sin(math.radians(magnetic_angle))

        ax.plot([0, x], [0, y], color='#FF7043', linewidth=2)
        ax.text(x, y, "Magnetic North", color='#FF7043')

        # 🔹 DECLINATION ARC (added)
        theta = np.linspace(0, math.radians(abs(angle)), 100)

        if direction == "E":
            arc_x = 1.5 * np.sin(theta)
            arc_y = 1.5 * np.cos(theta)
        else:
            arc_x = -1.5 * np.sin(theta)
            arc_y = 1.5 * np.cos(theta)

        ax.plot(arc_x, arc_y, color='yellow')

        # 🔹 LABEL ANGLE
        ax.text(arc_x[len(arc_x)//2], arc_y[len(arc_y)//2],
                f"{deg}°{minute}′ {direction}",
                color='yellow')

        # STATION
        ax.scatter(0, 0, color='yellow', s=80)
        ax.text(0, -0.6, "Station", color='white', ha='center')

        # 🔹 COMPASS DIRECTIONS (added)
        ax.text(0, 5.8, "N", color='white', ha='center')
        ax.text(0, -5.8, "S", color='white', ha='center')
        ax.text(5.8, 0, "E", color='white', va='center')
        ax.text(-5.8, 0, "W", color='white', va='center')

        # 🔹 LEGEND (added)
        ax.plot([], [], color='#4FC3F7', label='True North')
        ax.plot([], [], color='#FF7043', label='Magnetic North')
        ax.legend(facecolor='#0e1117', labelcolor='white')

        # STYLE
        ax.set_title("Magnetic Declination Diagram", color='white')

        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        ax.grid(True, linestyle='--', linewidth=0.5, color='gray')
        ax.set_aspect('equal')

        plt.tight_layout()

        st.pyplot(fig)