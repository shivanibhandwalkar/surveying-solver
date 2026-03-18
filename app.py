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
            total_mag = mag_deg + mag_min / 60
            decl = 180 - total_mag

            if decl >= 0:
                direction = "E"
            else:
                direction = "W"

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

        # ---------------- COMPASS ----------------
        angle = deg + minute / 60

        # 🔥 SIGNED ANGLE FIX
        if direction == "E":
            signed_angle = angle
        else:
            signed_angle = -angle

        rad = math.radians(signed_angle)

        fig, ax = plt.subplots(figsize=(7,7))

        fig.patch.set_facecolor("#506080")
        ax.set_facecolor("#495a7d")

        # -------- GRID --------
        for d in range(0, 360, 30):
            r = math.radians(d)
            xg = 7 * math.sin(r)
            yg = 7 * math.cos(r)
            ax.plot([0, xg], [0, yg], linestyle='--', linewidth=0.5, alpha=0.4)

        # -------- AXES --------
        ax.axhline(0, linewidth=1)
        ax.axvline(0, linewidth=1)

        # -------- TRUE NORTH --------
        ax.arrow(0, 0, 0, 6, head_width=0.35, length_includes_head=True)
        ax.text(0, 6.6, "True North", color='white', ha='center', fontsize=9)

        # -------- MAGNETIC NORTH (FIXED) --------
        x = 6 * math.sin(rad)
        y = 6 * math.cos(rad)

        ax.arrow(0, 0, x, y, head_width=0.35, length_includes_head=True)
        ax.text(x, y, "Magnetic North", color='white', fontsize=9)

        # -------- DECLINATION ARC (FIXED) --------
        arc_radius = 2.5

        theta = np.linspace(0, rad, 200)

        arc_x = arc_radius * np.sin(theta)
        arc_y = arc_radius * np.cos(theta)

        ax.plot(arc_x, arc_y, linewidth=2)

        # -------- ARC ARROW --------
        dx = arc_x[-1] - arc_x[-3]
        dy = arc_y[-1] - arc_y[-3]

        ax.arrow(
            arc_x[-3], arc_y[-3],
            dx, dy,
            head_width=0.25,
            color='white',
            length_includes_head=True
        )

        # -------- LABEL --------
        mid = len(arc_x)//2

        ax.text(
            arc_x[mid]*1.4,
            arc_y[mid]*1.4,
            f"Declination\n{deg}° {minute}′ {direction}",
            color='yellow',
            fontsize=9,
            ha='center',
            bbox=dict(facecolor='#222', edgecolor='white', boxstyle='round,pad=0.3')
        )

        # -------- STATION --------
        ax.scatter(0, 0, s=80)
        ax.text(0, -0.9, "Station", color='white', ha='center')

        # -------- COMPASS --------
        ax.text(0, 7.8, "N", color='white', ha='center', fontsize=10)
        ax.text(0, -7.8, "S", color='white', ha='center', fontsize=10)
        ax.text(7.8, 0, "E", color='white', fontsize=10)
        ax.text(-7.8, 0, "W", color='white', fontsize=10)

        # -------- DEGREE MARKS --------
        for d in range(0, 360, 30):
            r = math.radians(d)
            xd = 7.5 * math.sin(r)
            yd = 7.5 * math.cos(r)
            ax.text(xd, yd, f"{d}°", color='gray', fontsize=6, ha='center')

        # -------- STYLE --------
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        ax.set_aspect('equal')

        ax.grid(False)

        for spine in ax.spines.values():
            spine.set_color('white')

        ax.tick_params(colors='white')

        ax.set_title("Advanced Compass Declination Diagram", color='white', fontsize=11)

        plt.tight_layout()
        st.pyplot(fig)