import streamlit as st
from PIL import Image, ImageDraw
import time
import numpy as np

st.title("Bouncing DVD Logo")

# Load DVD image from local file
dvd_img = Image.open("dvd.jpg").convert("RGBA")
dvd_img = dvd_img.resize((100, 60))  # Resize for better animation

# Canvas size
canvas_width, canvas_height = 600, 400

# Initial position and velocity
x, y = np.random.randint(0, canvas_width-100), np.random.randint(0, canvas_height-60)
vx, vy = 3, 2

# Animation loop
frame = st.empty()
run = st.button("Start Animation")

if run:
    while True:
        # Create blank canvas
        canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 255))
        canvas.paste(dvd_img, (x, y), dvd_img)

        # Display frame
        frame.image(canvas)

        # Update position
        x += vx
        y += vy

        # Bounce off walls
        if x <= 0 or x >= canvas_width - 100:
            vx = -vx
        if y <= 0 or y >= canvas_height - 60:
            vy = -vy

        time.sleep(0.01)