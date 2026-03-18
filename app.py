import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.title("Surveying Problem 4 Solver")

# INPUTS
mag_deg = st.number_input("Enter Magnetic Bearing Degree", min_value=0, max_value=360, value=175)
mag_min = st.number_input("Enter Minutes", min_value=0, max_value=59, value=30)

# BUTTON
if st.button("Solve"):

    total_mag = mag_deg + mag_min/60

    if total_mag > 180:
        decl = 180 - total_mag
        direction = "E"
    else:
        decl = total_mag
        direction = "W"

    deg = int(abs(decl))
    minute = int((abs(decl) - deg) * 60)

    st.subheader("Solution Steps")

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

    st.success(f"Final Answer: {deg}° {minute}′ {direction}")

    # DRAW DIAGRAM
    angle = deg + minute/60

    if direction == "E":
        magnetic_angle = 90 - angle
    else:
        magnetic_angle = 90 + angle

    fig, ax = plt.subplots()

    # True North
    ax.plot([0,0],[0,5])
    ax.text(0,5.2,"True North")

    # Magnetic North
    x = 5 * math.cos(math.radians(magnetic_angle))
    y = 5 * math.sin(math.radians(magnetic_angle))

    ax.plot([0,x],[0,y])
    ax.text(x,y,"Magnetic North")

    ax.scatter(0,0)
    ax.text(0,-0.5,"Station")

    ax.set_title("Magnetic Declination Diagram")
    ax.axis('equal')
    ax.grid()

    st.pyplot(fig)