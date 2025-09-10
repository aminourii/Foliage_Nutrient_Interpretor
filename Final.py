import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import matplotlib.patches as patches
from PIL import Image   # ✅ added this for image handling
import fpdf as FPDF
import plotly.express as px
import plotly.graph_objs as go
import plotly.subplots as sp
from plotly.subplots import make_subplots
import reportlab


# st.image("Logo_Thatcher_Blue.png", width=350, use_column_width=None, caption="Think It. We TAnk It")

# --- Display Logo ---
logo = Image.open("images/Logo_Thatcher_Blue.png")  # ✅ use relative path
st.image(logo, width=350, caption="Think It. We Tank It.")

st.title("Crop Tissue Analysis Interpretor")

# st.image("I_0020DJa.PNG", width=1000, use_column_width=None, caption="Think It. We Tank It.")

# --- Display Product Image ---
product_img = Image.open("images/I_0020DJa.PNG")  # ✅ use relative path
st.image(product_img, width=1000, caption="Think It. We Tank It.")

# Read the CSV file
uploaded_file = st.sidebar.file_uploader("📁 Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.warning("Please upload a CSV file.")
    st.stop()

st.markdown("-----")

# Ask the user to select the crop type
st.sidebar.title("*Select Crop Type & Growth Stage*")
crop_type = st.sidebar.selectbox(
    "🌽 Select Crop Type:",
    ["Corn", "Soybean", "Winter Wheat", "Blueberry-High Bush", "Blueberry", "Pepper", "Squash", "Tomato"]
)

# Define growth stages for each crop type in a dictionary
crop_growth_stages = {
    "Blueberry-High Bush": ["Stage 1"],
    "Blueberry": ["Stage 1"],
    "Corn": ["Vegetative (V1-V9)", "Early Ear (R1-R3)", "Late Ear (R4-R6)", "Tasseling (V13+)", "Whorl (V10-12)", "Whole Plant"],
    "Soybean": ["Vegetative [V1-V(n)]", "Early Bloom (R1-R2)", "Late Bloom (R3)", "Full Pod-Full Seed (R4-R6)"],
    "Winter Wheat": ["Tillering F1-F2", "Tillering F3-F5", "Stem Extension F6-F9", "In Boot F10", "Heading F10.1-F11"],
    "Pepper": ["Early Bloom", "Fruiting", "Vegetative", "Fruit Set"],
    "Squash": ["Bloom-Fruiting", "Vegetative", "Harvest"],
    "Tomato": ["Vegetative", "Early Bloom", "Fruit Set", "Late Fruit Set"]
}

# Populate the "Select Growth Stage" dropdown based on the selected crop type
if crop_type in crop_growth_stages:
    growth_stage = st.sidebar.selectbox("📆 Select Growth Stage", crop_growth_stages[crop_type])

# Add a "Generate" button to trigger the calculation
generate_button = st.sidebar.button("📊 Generate Results")

# Define nutrient ranges based on the selected crop type and growth stage
if generate_button:
    if crop_type == "Blueberry-High Bush":
        nutrient_ranges = {
            'N': [(0, 0.75), (0.76, 1.1), (1.11, 2), (2.01, 3.5), (3.51, 7)],
            'P': [(0, 0.1), (0.11, 0.14), (0.15, 0.3), (0.31, 1), (1.01, 2)],
            'K': [(0, 0.35), (0.36, 0.4), (0.41, 0.75), (0.76, 1.5), (1.51, 3)],
            'Ca': [(0, 0.15), (0.16, 0.25), (0.26, 1), (1.01, 2.2), (2.21, 4.4)],
            'Mg': [(0, 0.1), (0.11, 0.14), (0.15, 0.3), (0.31, 1.2), (1.21, 2.4)],
            'S': [(0, 0.1), (0.11, 0.18), (0.19, 0.3), (0.31, 1), (1.01, 2)],
            'Zn': [(0, 10), (11, 20), (21, 35), (36, 200), (201, 400)],
            'B': [(0, 10), (11, 25), (26, 75), (76, 125), (126, 300)],
            'Mn': [(0, 20), (21, 30), (31, 150), (151, 200), (201, 400)],
            'Fe': [(0, 20), (21, 30), (31, 90), (91, 250), (251, 360)],
            'Cu': [(0, 2), (2.1, 4), (4.1, 17), (17.1, 25), (25.1, 50)]
        }
    elif crop_type == "Blueberry":
        nutrient_ranges = {
            'N': [(0, 0.85), (0.86, 1.45), (1.46, 2.2), (2.21, 4), (4.01, 8)],
            'P': [(0, 0.1), (0.11, 0.14), (0.15, 0.4), (0.41, 1), (1.01, 2)],
            'K': [(0, 0.1), (0.11, 0.4), (0.41, 1.1), (1.11, 2.2), (2.21, 4.4)],
            'Ca': [(0, 0.15), (0.16, 0.25), (0.26, 1), (1.01, 2.5), (2.51, 5)],
            'Mg': [(0, 0.1), (0.11, 0.14), (0.15, 0.3), (0.31, 0.8), (0.81, 1.6)],
            'S': [(0, 0.1), (0.11, 0.18), (0.19, 0.4), (0.41, 0.8), (0.81, 1.6)],
            'Zn': [(0, 5), (5.1, 10), (10.1, 100), (100.1, 225), (225.1, 550)],
            'B': [(0, 10), (10.1, 25), (25.1, 75), (75.1, 125), (125.1, 300)],
            'Mn': [(0, 20), (20.1, 30), (30.1, 500), (500.1, 650), (650.1, 1200)],
            'Fe': [(0, 20), (20.1, 35), (35.1, 200), (200.1, 300), (300.1, 600)],
            'Cu': [(0, 1), (1.1, 4), (4.1, 20), (20.1, 50), (50.1, 100)]
        }   
    elif crop_type == "Corn":
        if growth_stage == "Vegetative (V1-V9)":  
            nutrient_ranges = {      
                'N': [(0, 2.7), (2.71, 3), (3.01, 4.5), (4.51, 5.4), (5.41, 10.8)],
                'P': [(0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 0.6), (0.61, 1.2)],
                'K': [(0, 1.8), (1.81, 2), (2.01, 3), (3.01, 3.6), (3.61, 7.2)],
                'Ca': [(0, 0.2), (0.21, 0.25), (0.26, 0.7), (0.71, 0.85), (0.86, 1.7)],
                'Mg': [(0, 0.14), (0.15, 0.18), (0.19, 0.3), (0.31, 0.4), (0.41, 0.8)],
                'S': [(0, 0.1), (0.11, 0.15), (0.16, 0.5), (0.51, 0.6), (0.61, 1.2)],
                'Zn': [(0, 10), (10.01, 15), (15.01, 60), (60.01, 75), (75.01, 150)],
                'B': [(0, 2), (2.01, 4), (4.01, 25), (25.01, 30), (30.01, 60)],
                'Mn': [(0, 15), (15.01, 20), (20.01, 200), (200.01, 360), (360.01, 720)],
                'Fe': [(0, 20), (20.01, 30), (30.01, 300), (300.01, 400), (400.01, 800)],
                'Cu': [(0, 2), (2.01, 3), (3.01, 20), (20.01, 25), (25.01, 50)]
            }
        elif growth_stage == "Early Ear (R1-R3)":
            nutrient_ranges = {
                'N': [(0, 2.45), (2.46, 2.75), (2.76, 4), (4.01, 5.4), (5.41, 10.8)],
                'P': [(0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 0.6), (0.61, 1.2)],
                'K': [(0, 1.55), (1.56, 1.75), (1.76, 3), (3.01, 3.6), (3.61, 7.2)],
                'Ca': [(0, 0.2), (0.21, 0.25), (0.26, 0.6), (0.61, 0.85), (0.86, 1.7)],
                'Mg': [(0, 0.1), (0.11, 0.13), (0.14, 0.3), (0.31, 0.4), (0.41, 0.8)],
                'S': [(0, 0.08), (0.09, 0.12), (0.13, 0.4), (0.41, 0.6), (0.61, 1.2)],
                'Zn': [(0, 10), (10.01, 15), (15.01, 60), (60.01, 75), (75.01, 150)],
                'B': [(0, 2), (2.01, 4), (4.01, 25), (25.01, 35), (35.01, 70)],
                'Mn': [(0, 13), (13.01, 20), (20.01, 200), (200.01, 360), (360.01, 720)],
                'Fe': [(0, 20), (20.01, 30), (30.01, 250), (250.01, 300), (300.01, 600)],
                'Cu': [(0, 2), (2.01, 5), (5.01, 20), (20.01, 25), (25.01, 50)]
            }
        elif growth_stage == "Late Ear (R4-R6)":
            nutrient_ranges = {
                'N': [(0, 2.25), (2.26, 2.5), (2.51, 4), (4.01, 4.8), (4.81, 9.6)],
                'P': [(0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 0.6), (0.61, 1.2)],
                'K': [(0, 1.35), (1.36, 1.5), (1.51, 2.5), (2.51, 3), (3.01, 6)],
                'Ca': [(0, 0.2), (0.21, 0.4), (0.41, 0.7), (0.71, 0.85), (0.86, 1.7)],
                'Mg': [(0, 0.1), (0.11, 0.2), (0.21, 0.3), (0.31, 0.4), (0.41, 0.8)],
                'S': [(0, 0.1), (0.11, 0.2), (0.21, 0.45), (0.46, 0.55), (0.56, 1.1)],
                'Zn': [(0, 10), (10.01, 15), (15.01, 50), (50.01, 75), (75.01, 150)],
                'B': [(0, 2), (2.01, 4), (4.01, 20), (20.01, 35), (35.01, 70)],
                'Mn': [(0, 10), (10.01, 20), (20.01, 200), (200.01, 360), (360.01, 720)],
                'Fe': [(0, 20), (20.01, 35), (35.01, 200), (200.01, 300), (300.01, 600)], 
                'Cu': [(0, 2), (2.01, 5), (5.01, 15), (15.01, 25), (25.01, 50)]
            }
        elif growth_stage == "Tasseling (V13+)":
            nutrient_ranges = {
                'N': [ (0, 2.45), (2.46, 2.75), (2.76, 4.5), (4.51, 5.4), (5.41, 10.8) ],
                'P': [ (0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 0.6), (0.61, 1.2) ],
                'K': [ (0, 0.85), (0.86, 1.75), (1.76, 3), (3.01, 3.6), (3.61, 7.2) ],
                'Ca': [(0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 0.85), (0.86, 1.7)],
                'Mg': [ (0, 0.1), (0.11, 0.13), (0.14, 0.3), (0.31, 0.4), (0.41, 0.8) ],
                'S': [ (0, 0.09), (0.1, 0.12), (0.13, 0.5), (0.51, 0.6), (0.61, 1.2) ],
                'Zn': [ (0, 10), (10.01, 15), (15.01, 60), (60.01, 75), (75.01, 150) ],
                'B': [(0, 2), (2.01, 4), (4.01, 25), (25.01, 30), (30.01, 60)],
                'Mn': [ (0, 15), (15.01, 20), (20.01, 200), (200.01, 360), (360.01, 720) ],
                'Fe': [(0, 20), (20.01, 30), (30.01, 250), (250.01, 300), (300.01, 600)],
                'Cu': [(0, 2), (2.01, 5), (5.01, 20), (20.01, 25), (25.01, 50)] 
            }  
        elif growth_stage == "Whorl (V10-12)":
            nutrient_ranges = {
                'N': [ (0, 2.7), (2.71, 3), (3.01, 4.5), (4.51, 5.4), (5.41, 10.8) ],
                'P': [ (0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 0.6), (0.61, 1.2) ],
                'K': [ (0, 1.8), (1.81, 2), (2.01, 3), (3.01, 3.6), (3.61, 7.2) ],
                'Ca': [ (0, 0.2), (0.21, 0.4), (0.41, 0.8), (0.81, 0.85), (0.86, 1.7) ],
                'Mg': [ (0, 0.1), (0.11, 0.18), (0.19, 0.3), (0.31, 0.4), (0.41, 0.8) ],
                'S': [ (0, 0.1), (0.11, 0.15), (0.16, 0.5), (0.51, 0.6), (0.61, 1.2) ],
                'Zn': [ (0, 10), (10.01, 15), (15.01, 60), (60.01, 75), (75.01, 150) ],
                'B': [ (0, 2), (2.01, 4), (4.01, 25), (25.01, 30), (30.01, 60) ],
                'Mn': [ (0, 15), (15.01, 28), (28.01, 200), (200.01, 360), (360.01, 720) ],
                'Fe': [ (0, 25), (25.01, 30), (30.01, 250), (250.01, 300), (300.01, 600) ],
                'Cu': [ (0, 2), (2.01, 3), (3.01, 20), (20.01, 25), (25.01, 50) ]   
            }  
        elif growth_stage == "Whole Plant":
            nutrient_ranges = {
                'N': [(0, 3.15), (3.16, 3.5), (3.51, 5), (5.01, 6), (6.01, 12)],
                'P': [(0, 0.25), (0.26, 0.3), (0.31, 0.6), (0.61, 0.75), (0.76, 1.5)],
                'K': [(0, 2.25), (2.26, 2.5), (2.51, 3.5), (3.51, 4.2), (4.21, 8.4)],
                'Ca': [ (0, 0.15), (0.16, 0.3), (0.31, 0.6), (0.61, 0.85), (0.86, 1.7) ],
                'Mg': [(0, 0.14), (0.14, 0.2), (0.21, 0.3), (0.31, 0.4), (0.41, 0.8)],
                'S': [(0, 0.1), (0.11, 0.13), (0.14, 0.6), (0.61, 0.75), (0.76, 1.5)],
                'Zn': [(0, 15), (15.01, 20), (20.01, 60), (60.01, 75), (75.01, 150)],
                'B': [ (0, 3), (3.01, 5), (5.01, 25), (25.01, 30), (30.01, 60) ],
                'Mn': [(0, 15), (15.01, 20), (20.01, 200), (200.01, 360), (360.01, 720)],
                'Fe': [(0, 40), (40.01, 50), (50.01, 300), (300.01, 400), (400.01, 800)],
                'Cu': [(0, 3), (3.01, 5), (5.01, 20), (20.01, 25), (25.01, 50)]
            }   
    elif crop_type == "Soybean":
        if growth_stage == "Vegetative [V1-V(n)]":
            nutrient_ranges = {
                'N': [(0, 3.8), (3.81, 4.25), (4.26, 5), (5.01, 6), (6.01, 12)],
                'P': [(0, 0.25), (0.26, 0.3), (0.31, 0.5), (0.51, 1), (1.01, 2)],
                'K': [(0, 1.8), (1.81, 2), (2.01, 3), (3.01, 4), (4.01, 8)],
                'Ca': [(0, 0.45), (0.46, 1), (1.01, 2.2), (2.21, 3.5), (3.51, 7)],
                'Mg': [(0, 0.25), (0.26, 0.3), (0.31, 0.8), (0.81, 1.8), (1.81, 3.6)],
                'S': [(0, 0.15), (0.16, 0.2), (0.21, 0.6), (0.61, 1.2), (1.21, 2.4)],
                'Zn': [(0, 15), (15.01, 20), (20.01, 100), (100.01, 200), (200.01, 400)],
                'B': [(0, 20), (20.1, 25), (25.1, 60), (60.1, 90), (90.1, 180)],
                'Mn': [(0, 15), (15.01, 20), (20.01, 350), (350.01, 400), (400.01, 800)],
                'Fe': [(0, 40), (40.01, 50), (50.01, 250), (250.01, 350), (350.01, 700)],
                'Cu': [(0, 3), (3.01, 6), (6.01, 25), (25.01, 50), (50.01, 100)] 
            }  
        elif growth_stage == "Early Bloom (R1-R2)":  
            nutrient_ranges = {      
                'N': [(0, 3.8), (3.81, 4.25), (4.26, 5), (5.01, 6), (6.01, 12)],
                'P': [(0, 0.2), (0.21, 0.25), (0.26, 0.6), (0.61, 1), (1.01, 2)],
                'K': [(0, 1.55), (1.56, 1.75), (1.76, 2.5), (2.51, 3.6), (3.61, 7.2)],
                'Ca': [(0, 0.45), (0.46, 0.5), (0.51, 1.5), (1.51, 2.5), (2.51, 5)],
                'Mg': [(0, 0.2), (0.21, 0.25), (0.26, 0.8), (0.81, 1.5), (1.51, 3)],
                'S': [(0, 0.15), (0.16, 0.2), (0.21, 0.6), (0.61, 1), (1.01, 2)],
                'Zn': [(0, 15), (15.01, 20), (20.01, 70), (70.01, 90), (90.01, 180)],
                'B': [(0, 20), (20.01, 25), (25.01, 60), (60.01, 90), (90.01, 180)],
                'Mn': [(0, 15), (15.01, 20), (20.01, 100), (100.01, 200), (200.01, 400)],
                'Fe': [(0, 40), (40.01, 50), (50.01, 300), (300.01, 390), (390.01, 780)],
                'Cu': [(0, 3), (3.01, 6), (6.01, 25), (25.01, 50), (50.01, 100)]
            }
        elif growth_stage == "Late Bloom (R3)":
            nutrient_ranges = {
                'N': [ (0, 3.8), (3.81, 4.25), (4.26, 5.5), (5.51, 6.25), (6.26, 12.5) ],
                'P': [ (0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 1), (1.01, 2), (2.01, 4) ],
                'K': [ (0, 1.55), (1.56, 1.75), (1.76, 2.25), (2.26, 3.6), (3.61, 7.2) ],
                'Ca': [(0, 0.45), (0.46, 0.5), (0.51, 1.6), (1.61, 2.5), (2.51, 5)],
                'Mg': [ (0, 0.2), (0.21, 0.25), (0.26, 0.8), (0.81, 2.7), (2.71, 5.4) ],
                'S': [(0.0, 0.15), (0.16, 0.2), (0.21, 0.4), (0.41, 0.75), (0.76, 1.5)],
                'Zn': [(0.0, 15), (16, 20), (21, 50), (51, 85), (86, 170)],
                'B': [(0, 20), (20.01, 25), (25.01, 60), (60.01, 90), (90.01, 180)],
                'Mn': [ (0, 15), (15.01, 20), (20.01, 100), (100.01, 200), (200.01, 400) ],
                'Fe': [ (0, 40), (40.01, 50), (50.01, 300), (300.01, 360), (360.01, 720) ],
                'Cu': [ (0, 3), (3.01, 6), (6.01, 30), (30.01, 60), (60.01, 120) ]
            }
        elif growth_stage == "Full Pod-Full Seed (R4-R6)":
            nutrient_ranges = {
                'N': [(0.0, 2.2), (2.21, 3.5), (3.51, 5), (5.01, 6), (6.01, 12)],
                'P': [(0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 0.6), (0.61, 1.2)],
                'K': [(0.0, 1.25), (1.26, 1.75), (1.76, 2.5), (2.51, 3.6), (3.61, 7.2)],
                'Ca': [(0.0, 0.3), (0.31, 0.6), (0.61, 1.35), (1.36, 1.8), (1.81, 3.6)],
                'Mg': [(0.0, 0.2), (0.21, 0.25), (0.26, 0.6), (0.61, 1), (1.01, 2)],
                'S': [(0, 0.15), (0.16, 0.2), (0.21, 0.4), (0.41, 0.75), (0.76, 1.5)],
                'Zn': [(0, 15), (15.1, 20), (20.1, 50), (50.1, 85), (85.1, 170)],
                'B': [(0.0, 20), (21, 25), (26, 60), (61, 75), (76, 150)],
                'Mn': [(0.0, 15), (15.01, 20), (20.01, 125), (125.01, 240), (240.01, 480)],
                'Fe': [(0.0, 40), (40.01, 50), (50.01, 250), (250.01, 360), (360.01, 720)], 
                'Cu': [(0.0, 3), (3.01, 6), (6.01, 25), (25.01, 30), (30.01, 60)]
            }
    elif crop_type == "Winter Wheat":
        if growth_stage == "Tillering F1-F2":
            nutrient_ranges = {      
                'N': [(0, 2.5), (2.51, 3), (3.01, 4), (4.01, 4.8), (4.81, 9.6)],
                'P': [(0, 0.15), (0.16, 0.2), (0.21, 0.4), (0.41, 0.5), (0.51, 1)],
                'K': [(0, 1.6), (1.61, 2), (2.01, 3), (3.01, 4), (4.01, 8)],
                'Ca': [(0, 0.15), (0.16, 0.2), (0.21, 1), (1.01, 2), (2.01, 4)],
                'Mg': [(0, 0.1), (0.11, 0.15), (0.16, 0.6), (0.61, 0.75), (0.76, 1.5)],
                'S': [(0, 0.15), (0.16, 0.17), (0.18, 0.6), (0.61, 1), (1.01, 2)],
                'Zn': [(0, 15), (15.01, 25), (25.02, 80), (80.03, 110), (110.04, 220)],
                'B': [(0, 2), (2.01, 3), (3.01, 20), (20.01, 30), (30.01, 60)],
                'Mn': [(0, 15), (15.01, 25), (25.02, 150), (150.03, 180), (180.04, 360)],
                'Fe': [(0, 10), (10.01, 18), (18.01, 70), (70.01, 100), (100.01, 200)],
                'Cu': [(0, 3), (3.01, 4), (4.01, 20), (20.01, 25), (25.01, 50)]
            }
        elif growth_stage == "Tillering F3-F5":
            nutrient_ranges = {
                'B': [(0, 2), (2.01, 3), (3.02, 15), (15.03, 25), (25.04, 50)],
                'Ca': [(0, 0.15), (0.16, 0.3), (0.31, 0.8), (0.81, 1.25), (1.26, 2.5)],
                'Cu': [(0, 2), (2.01, 5), (5.02, 20), (20.03, 30), (30.04, 60)],
                'Fe': [(0, 10), (10.01, 25), (25.02, 150), (150.03, 200), (200.04, 400)],
                'K': [(0, 0.8), (0.81, 1.8), (1.81, 3.5), (3.51, 4.25), (4.26, 8.5)],
                'Mg': [(0, 0.1), (0.11, 0.15), (0.16, 0.85), (0.86, 1.2), (1.21, 2.4)],
                'Mn': [(0, 10), (10.01, 20), (20.02, 150), (150.03, 250), (250.04, 500)],
                'N': [(0, 2.5), (2.51, 3.3), (3.31, 4.5), (4.51, 5.5), (5.51, 11)],
                'P': [(0, 0.1), (0.11, 0.25), (0.26, 0.5), (0.51, 0.75), (0.76, 1.5)],
                'S': [(0, 0.1), (0.11, 0.2), (0.21, 0.55), (0.56, 0.75), (0.76, 1.5)],
                'Zn': [(0, 10), (10.01, 25), (25.01, 80), (80.01, 150), (150.01, 300)]
            }
        elif growth_stage == "Stem Extension F6-F9":
            nutrient_ranges = {
                'N': [(0, 2.5), (2.51, 3.3), (3.31, 4.5), (4.51, 5.5), (5.51, 11)],
                'P': [(0, 0.1), (0.11, 0.25), (0.26, 0.5), (0.51, 0.75), (0.76, 1.5)],
                'K': [(0, 0.8), (0.81, 1.8), (1.81, 3.25), (3.26, 4.25), (4.26, 8.5)],
                'Ca': [(0, 0.15), (0.16, 0.3), (0.31, 0.8), (0.81, 1.25), (1.26, 2.5)],
                'Mg': [(0, 0.1), (0.11, 0.15), (0.16, 0.85), (0.86, 1.2), (1.21, 2.4)],
                'S': [(0, 0.1), (0.11, 0.2), (0.21, 0.55), (0.56, 0.75), (0.76, 1.5)],
                'Zn': [(0, 10), (10.01, 25), (25.01, 80), (80.01, 150), (150.01, 300)],
                'B': [(0, 2), (2.01, 5), (5.01, 20), (20.01, 25), (25.01, 50)],
                'Mn': [(0, 10), (10.01, 20), (20.01, 150), (150.01, 250), (250.01, 500)],
                'Fe': [(0, 0.8), (0.81, 1.8), (1.81, 3.25), (3.26, 4.25), (4.26, 8.5)],
                'Cu': [(0, 2), (2.01, 5), (5.01, 20), (20.01, 25), (25.01, 50)]
            } 
        elif growth_stage == "In Boot F10":
            nutrient_ranges = {
                'N': [(0, 2.2), (2.21, 3.5), (3.51, 4.75), (4.76, 5.25), (5.26, 10.5)],
                'P': [(0, 0.1), (0.11, 0.25), (0.26, 0.5), (0.51, 0.75), (0.76, 1.5)],
                'K': [(0, 1.3), (1.31, 2), (2.01, 4), (4.01, 5), (5.01, 10)],
                'Ca': [(0, 0.1), (0.11, 0.25), (0.26, 1), (1.01, 2), (2.01, 4)],
                'Mg': [(0, 0.1), (0.11, 0.25), (0.26, 1), (1.01, 2), (2.01, 4)],
                'S': [(0, 0.15), (0.16, 0.17), (0.18, 0.65), (0.66, 0.8), (0.81, 1.6)],
                'Zn': [(0, 10), (10.01, 18), (18.01, 70), (70.01, 100), (100.01, 200)],
                'B': [(0, 1), (1.01, 3), (3.01, 20), (20.01, 30), (30.01, 60)],
                'Mn': [(0, 10), (10.01, 25), (25.01, 150), (150.01, 300), (300.01, 600)],
                'Fe': [(0, 10), (10.01, 30), (30.01, 250), (250.01, 400), (400.01, 800)],
                'Cu': [(0, 3), (3.01, 5), (5.01, 20), (20.01, 30), (30.01, 60)]
            }   
        elif growth_stage == "Heading F10.1-F11":
            nutrient_ranges = {
                'N': [(0, 2.7), (2.71, 3), (3.01, 4.5), (4.51, 5.4), (5.41, 10.8)],
                'P': [(0, 0.2), (0.21, 0.25), (0.26, 0.5), (0.51, 0.6), (0.61, 1.2)],
                'K': [(0, 1.8), (1.81, 2), (2.01, 3), (3.01, 3.6), (3.61, 7.2)],
                'Ca': [(0, 0.2), (0.21, 0.25), (0.26, 0.7), (0.71, 0.85), (0.86, 1.7)],
                'Mg': [(0, 0.14), (0.15, 0.18), (0.19, 0.3), (0.31, 0.4), (0.41, 0.8)],
                'S': [(0, 0.1), (0.11, 0.15), (0.16, 0.5), (0.51, 0.6), (0.61, 1.2)],
                'Zn': [(0, 10), (10.01, 15), (15.01, 60), (60.01, 75), (75.01, 150)],
                'B': [(0, 2), (2.01, 4), (4.01, 25), (25.01, 30), (30.01, 60)],
                'Mn': [(0, 15), (15.01, 20), (20.01, 200), (200.01, 360), (360.01, 720)],
                'Fe': [(0, 20), (20.01, 30), (30.01, 300), (300.01, 400), (400.01, 800)],
                'Cu': [(0, 2), (2.01, 3), (3.01, 20), (20.01, 25), (25.01, 50)]
            }
    elif crop_type == "Pepper":
        if growth_stage == "Early Bloom":  # Pepper - Growth Stage 1
            nutrient_ranges = {      
                'N': [(0, 3), (3.01, 3.5), (3.51, 5.5), (5.51, 7.2), (7.21, 14.4)],
                'P': [(0, 0.3), (0.31, 0.35), (0.36, 0.6), (0.61, 0.9), (0.91, 1.8)],
                'K': [(0, 3.6), (3.61, 4), (4.01, 5), (5.01, 7.2), (7.21, 14.4)],
                'Ca': [(0, 1.05), (1.06, 1.2), (1.21, 2.2), (2.21, 2.65), (2.66, 5.3)],
                'Mg': [(0, 0.25), (0.26, 0.3), (0.31, 0.8), (0.81, 1), (1.01, 2)],
                'S': [(0, 0.35), (0.36, 0.4), (0.41, 0.6), (0.61, 0.85), (0.86, 1.7)],
                'Zn': [(0, 15), (15.1, 20), (20.1, 100), (100.1, 240), (240.1, 480)],
                'B': [(0, 15), (15.1, 20), (20.1, 70), (70.1, 85), (85.1, 170)],
                'Mn': [(0, 45), (45.1, 50), (50.1, 200), (200.1, 240), (240.1, 480)],
                'Fe': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 300), (300.1, 600)],
                'Cu': [(0, 3), (3.1, 6), (6.1, 20), (20.1, 30), (30.1, 60)]
            }
        elif growth_stage == "Fruiting":
            nutrient_ranges = {
                'N': [(0, 2), (2.01, 3), (3.01, 5), (5.01, 7.2), (7.21, 14.4)],
                'P': [(0, 0.15), (0.16, 0.3), (0.31, 0.5), (0.51, 0.9), (0.91, 1.8)],
                'K': [(0, 1.8), (1.81, 3), (3.01, 4.5), (4.51, 7.2), (7.21, 14.4)],
                'Ca': [(0, 0.75), (0.76, 1.2), (1.21, 2), (2.01, 2.65), (2.66, 5.3)],
                'Mg': [(0, 0.2), (0.21, 0.35), (0.36, 0.8), (0.81, 1), (1.01, 2)],
                'S': [(0, 0.2), (0.21, 0.3), (0.31, 0.5), (0.51, 0.85), (0.86, 1.7)],
                'Zn': [(0, 15), (15.1, 25), (25.1, 100), (100.1, 240), (240.1, 480)],
                'B': [(0, 15), (15.1, 20), (20.1, 50), (50.1, 85), (85.1, 170)],
                'Mn': [(0, 20), (20.1, 40), (40.1, 150), (150.1, 240), (240.1, 480)],
                'Fe': [(0, 40), (40.1, 40), (40.1, 200), (200.1, 300), (300.1, 600)],
                'Cu': [(0, 4), (4.1, 7), (7.1, 15), (15.1, 30), (30.1, 60)]
            }
        elif growth_stage == "Vegetative":
            nutrient_ranges = {
                'N': [(0, 3), (3.01, 4), (4.01, 5.5), (5.51, 7.2), (7.21, 14.4)],
                'P': [(0, 0.2), (0.21, 0.35), (0.36, 0.5), (0.51, 0.9), (0.91, 1.8)],
                'K': [(0, 4.05), (4.06, 4.5), (4.51, 6), (6.01, 7.2), (7.21, 14.4)],
                'Ca': [(0, 1.35), (1.36, 1.5), (1.51, 2.2), (2.21, 2.65), (2.66, 5.3)],
                'Mg': [(0, 0.3), (0.31, 0.35), (0.36, 0.8), (0.81, 1), (1.01, 2)],
                'S': [(0, 0.4), (0.41, 0.45), (0.46, 0.6), (0.61, 0.85), (0.86, 1.7)],
                'Zn': [(0, 20), (20.1, 25), (25.1, 100), (100.1, 240), (240.1, 480)],
                'B': [(0, 15), (15.1, 20), (20.1, 60), (60.1, 85), (85.1, 170)],
                'Mn': [(0, 45), (45.1, 50), (50.1, 200), (200.1, 240), (240.1, 480)],
                'Fe': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 300), (300.1, 600)], 
                'Cu': [(0, 4), (4.1, 8), (8.1, 20), (20.1, 30), (30.1, 60)]
            }
        elif growth_stage == "Fruit Set":
            nutrient_ranges = {
                'N': [(0, 2), (2.01, 3), (3.01, 5), (5.01, 7.2), (7.21, 14.4)],
                'P': [(0, 0.15), (0.16, 0.3), (0.31, 0.5), (0.51, 0.9), (0.91, 1.8)],
                'K': [(0, 1.8), (1.81, 3), (3.01, 4.5), (4.51, 7.2), (7.21, 14.4)],
                'Ca': [(0, 0.75), (0.76, 1.2), (1.21, 2), (2.01, 2.65), (2.66, 5.3)],
                'Mg': [(0, 0.3), (0.31, 0.35), (0.36, 0.8), (0.81, 1), (1.01, 2)],
                'S': [(0, 0.4), (0.41, 0.3), (0.31, 0.5), (0.51, 0.85), (0.86, 1.7)],
                'Zn': [(0, 15), (15.1, 25), (25.1, 100), (100.1, 240), (240.1, 480)],
                'B': [(0, 15), (15.1, 20), (20.1, 50), (50.1, 85), (85.1, 170)],
                'Mn': [(0, 20), (20.1, 40), (40.1, 150), (150.1, 240), (240.1, 480)],
                'Fe': [(0, 40), (40.1, 40), (40.1, 200), (200.1, 300), (300.1, 600)],
                'Cu': [(0, 4), (4.1, 7), (7.1, 15), (15.1, 30), (30.1, 60)]   
            }
        # Define nutrient ranges for other growth stages
    elif crop_type == "Squash":
        if growth_stage == "Bloom-Fruiting":  # Squash - Growth Stage 1
            nutrient_ranges = {      
                'N': [(0, 3.6), (3.61, 4), (4.01, 6), (6.01, 7.2), (7.21, 14.4)],
                'P': [(0, 0.35), (0.36, 0.4), (0.41, 0.55), (0.56, 0.7), (0.71, 1.4)],
                'K': [(0, 2.45), (2.46, 2.75), (2.76, 5), (5.01, 6), (6.01, 12)],
                'Ca': [(0, 0.95), (0.96, 1.1), (1.11, 2.5), (2.51, 3), (3.01, 6)],
                'Mg': [(0, 0.45), (0.46, 0.5), (0.51, 1.2), (1.21, 1.45), (1.46, 2.9)],
                'S': [(0, 0.45), (0.46, 0.5), (0.51, 1), (1.01, 1.2), (1.21, 2.4)],
                'Zn': [(0, 20), (20.1, 25), (25.1, 200), (200.1, 250), (250.1, 500)],
                'B': [(0, 20), (20.1, 25), (25.1, 75), (75.1, 90), (90.1, 180)],
                'Mn': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 250), (250.1, 500)],
                'Fe': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 250), (250.1, 500)],
                'Cu': [(0, 4), (4.1, 8), (8.1, 25), (25.1, 30), (30.1, 60)]
            }
        elif growth_stage == "Vegetative":
            nutrient_ranges = {
                'N': [(0, 3.85), (3.86, 4.3), (4.31, 6), (6.01, 7.2), (7.21, 14.4)],
                'P': [(0, 0.4), (0.41, 0.45), (0.46, 0.55), (0.56, 0.7), (0.71, 1.4)],
                'K': [(0, 2.7), (2.71, 3), (3.01, 5), (5.01, 6), (6.01, 12)],
                'Ca': [(0, 1), (1.01, 1.2), (1.21, 2.5), (2.51, 3), (3.01, 6)],
                'Mg': [(0, 0.5), (0.51, 0.55), (0.56, 1.2), (1.21, 1.45), (1.46, 2.9)],
                'S': [(0, 0.5), (0.51, 0.55), (0.56, 1), (1.01, 1.2), (1.21, 2.4)],
                'Zn': [(0, 25), (25.1, 30), (30.1, 200), (200.1, 250), (250.1, 300)],
                'B': [(0, 25), (25.1, 30), (30.1, 75), (75.1, 90), (90.1, 180)],
                'Mn': [(0, 50), (50.1, 60), (60.1, 200), (200.1, 250), (250.1, 500)],
                'Fe': [(0, 50), (50.1, 60), (60.1, 200), (200.1, 250), (250.1, 500)],
                'Cu': [(0, 5), (5.1, 9), (9.1, 25), (25.1, 30), (30.1, 60)]
            }
        elif growth_stage == "Harvest":
            nutrient_ranges = {
                'N': [(0, 2.4), (2.41, 3), (3.01, 4.25), (4.26, 6.2), (6.21, 12.4)],
                'P': [(0, 0.35), (0.36, 0.4), (0.41, 0.55), (0.56, 0.7), (0.71, 1.4)],
                'K': [(0, 2.45), (2.46, 2.75), (2.76, 5), (5.01, 6), (6.01, 12)],
                'Ca': [(0, 0.95), (0.96, 1.1), (1.11, 2.5), (2.51, 3), (3.01, 6)],
                'Mg': [(0, 0.45), (0.46, 0.5), (0.51, 1.2), (1.21, 1.45), (1.46, 2.9)],
                'S': [(0, 0.45), (0.46, 0.5), (0.51, 1), (1.01, 1.2), (1.21, 2.4)],
                'Zn': [(0, 20), (20.1, 25), (25.1, 200), (200.1, 250), (250.1, 500)],
                'B': [(0, 20), (20.1, 25), (25.1, 75), (75.1, 90), (90.1, 180)],
                'Mn': [(0, 40), (40.1, 50), (50.1, 250), (250.1, 300), (300.1, 600)],
                'Fe': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 250), (250.1, 500)],
                'Cu': [(0, 4), (4.1, 8), (8.1, 25), (25.1, 30), (30.1, 60)]
            }
    elif crop_type == "Tomato":
        if growth_stage == "Vegetative":  
            nutrient_ranges = {      
                'N': [(0, 3.6), (3.61, 4), (4.01, 6), (6.01, 7.2), (7.21, 14.4)],
                'P': [(0, 0.25), (0.26, 0.3), (0.31, 0.75), (0.76, 0.9), (0.91, 1.8)],
                'K': [(0, 2.7), (2.71, 3), (3.01, 5), (5.01, 6), (6.01, 12)],
                'Ca': [(0, 1.1), (1.11, 1.25), (1.26, 3), (3.01, 3.6), (3.61, 7.2)],
                'Mg': [(0, 0.35), (0.36, 0.4), (0.41, 0.7), (0.71, 0.85), (0.86, 1.7)],
                'S': [(0, 0.55), (0.56, 0.65), (0.66, 1.2), (1.21, 1.45), (1.46, 2.9)],
                'Zn': [(0, 15), (15.1, 20), (20.1, 50), (50.1, 60), (60.1, 120)],
                'B': [(0, 15), (15.1, 20), (20.1, 60), (60.1, 75), (75.1, 150)],
                'Mn': [(0, 45), (45.1, 50), (50.1, 250), (250.1, 300), (300.1, 600)],
                'Fe': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 240), (240.1, 480)],
                'Cu': [(0, 3), (3.1, 5), (5.1, 20), (20.1, 25), (25.1, 50)]
            }
        elif growth_stage == "Early Bloom":
            nutrient_ranges = {
                'N': [(0, 3.6), (3.61, 4), (4.01, 6), (6.01, 7.2), (7.21, 14.4)],
                'P': [(0, 0.25), (0.26, 0.3), (0.31, 0.75), (0.76, 0.9), (0.91, 1.8)],
                'K': [(0, 2.7), (2.71, 3), (3.01, 5), (5.01, 6), (6.01, 12)],
                'Ca': [(0, 1.1), (1.11, 1.25), (1.26, 3), (3.01, 3.6), (3.61, 7.2)],
                'Mg': [(0, 0.35), (0.36, 0.4), (0.41, 0.7), (0.71, 0.85), (0.86, 1.7)],
                'S': [(0, 0.55), (0.56, 0.65), (0.66, 1.2), (1.21, 1.45), (1.46, 2.9)],
                'Zn': [(0, 15), (15.01, 20), (20.01, 50), (50.01, 60), (60.01, 120)],
                'B': [(0, 15), (15.01, 20), (20.01, 60), (60.01, 75), (75.01, 150)],
                'Mn': [(0, 45), (45.1, 50), (50.1, 250), (250.1, 300), (300.1, 600)],
                'Fe': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 240), (240.1, 480)],
                'Cu': [(0, 3), (3.1, 5), (5.1, 20), (20.1, 25), (25.1, 50)]
            }
        elif growth_stage == "Fruit Set":
            nutrient_ranges = {
                'N': [(0, 3.25), (3.26, 3.6), (3.61, 4), (4.01, 6.2), (6.21, 12.4)],
                'P': [(0, 0.25), (0.26, 0.3), (0.31, 0.75), (0.76, 0.9), (0.91, 1.8)],
                'K': [(0, 2.7), (2.71, 3), (3.01, 5), (5.01, 6), (6.01, 12)],
                'Ca': [(0, 1.1), (1.11, 1.25), (1.26, 3), (3.01, 3.6), (3.61, 7.2)],
                'Mg': [(0, 0.35), (0.36, 0.4), (0.41, 0.7), (0.71, 0.85), (0.86, 1.7)],
                'S': [(0, 0.55), (0.56, 0.65), (0.66, 1.2), (1.21, 1.45), (1.46, 2.9)],
                'Zn': [(0, 15), (15.1, 20), (20.1, 50), (50.1, 60), (60.1, 120)],
                'B': [(0, 15), (15.1, 20), (20.1, 60), (60.1, 75), (75.1, 150)],
                'Mn': [(0, 45), (45.1, 50), (50.1, 250), (250.1, 300), (300.1, 600)],
                'Fe': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 300), (300.1, 600)],
                'Cu': [(0, 3), (3.1, 5), (5.1, 20), (20.1, 25), (25.1, 50)]
            }
        elif growth_stage == "Late Fruit Set":
            nutrient_ranges = {
                'N': [(0, 3.6), (3.61, 4), (4.01, 6), (6.01, 7.2), (7.21, 14.4)],
                'P': [(0, 0.25), (0.26, 0.3), (0.31, 0.75), (0.76, 0.9), (0.91, 1.8)],
                'K': [(0, 2.7), (2.71, 3), (3.01, 5), (5.01, 6), (6.01, 12)],
                'Ca': [(0, 1.1), (1.11, 1.25), (1.26, 3), (3.01, 3.6), (3.61, 7.2)],
                'Mg': [(0, 0.35), (0.36, 0.4), (0.41, 0.7), (0.71, 0.85), (0.86, 1.7)],
                'S': [(0, 0.55), (0.56, 0.65), (0.66, 1.2), (1.21, 1.45), (1.46, 2.9)],
                'Zn': [(0, 15), (15.1, 20), (20.1, 50), (50.1, 60), (60.1, 120)],
                'B': [(0, 15), (15.1, 20), (20.1, 60), (60.1, 75), (75.1, 150)],
                'Mn': [(0, 45), (45.1, 50), (50.1, 250), (250.1, 300), (300.1, 600)],
                'Fe': [(0, 40), (40.1, 50), (50.1, 200), (200.1, 240), (240.1, 480)],
                'Cu': [(0, 3), (3.1, 5), (5.1, 20), (20.1, 25), (25.1, 50)]
            }

def classify_nutrient_level(value, nutrient_range):
    for i, (lower, upper) in enumerate(nutrient_range):
        if lower <= value <= upper:
            return i
    return -1

if generate_button:

    # Initialize lists to store Shapiro-Wilk values and normality test results
    shapiro_wilk_values = []
    normality_test_results = []

    # Iterate through nutrients and calculate averages and standard deviations
    nutrient_averages = {}
    nutrient_stddevs = {}  # Store standard deviations

    for nutrient, nutrient_range in nutrient_ranges.items():
        if nutrient in df.columns:
            df[nutrient + '_Level'] = df[nutrient].apply(lambda x: classify_nutrient_level(x, nutrient_range))
            nutrient_averages[nutrient] = df[nutrient].mean()
            nutrient_stddevs[nutrient] = df[nutrient].std()  # Calculate standard deviation

            # Perform Shapiro-Wilk normality test if there are more than two data points
            if len(df[nutrient]) > 2:
                shapiro_wilk_stat, shapiro_wilk_p = stats.shapiro(df[nutrient])
                shapiro_wilk_values.append(shapiro_wilk_stat)
                normality_test_results.append("Normal" if shapiro_wilk_p > 0.05 else "Not Normal")
            else:
                shapiro_wilk_values.append(None)
                normality_test_results.append("Not Applicable")
        else:
            st.warning(f"Warning: Nutrient '{nutrient}' not found in the CSV file. Skipping.")

    # Create a single legend that explains the color codes

    legend_labels = ['Very Low', 'Low', 'Sufficient', 'High', 'Very High']
    legend_colors = ['navy', 'deepskyblue', 'green', 'orange', 'red']
    legend_elements = [
        f'<div style="display: inline-block; background-color:{color}; padding: 5px; margin-right: 10px;">{label}</div>'
        for label, color in zip(legend_labels, legend_colors)
    ]


    # Create a DataFrame to store the average nutrient levels with standard deviations

    average_levels = []
    for nutrient, average in nutrient_averages.items():
        if nutrient in nutrient_ranges:
            level = classify_nutrient_level(average, nutrient_ranges[nutrient])
            level_names = ['Very Low', 'Low', 'Sufficient', 'High', 'Very High']
            average_levels.append({'Nutrient': nutrient, 'Average': average, 'Standard Deviation': nutrient_stddevs[nutrient], 'Nutrient Level': level_names[level]})

    # Convert the list of dictionaries to a DataFrame


    average_levels_df = pd.DataFrame(average_levels)

    # Print the table of average nutrient levels

    st.subheader("Table of Average Nutrient Levels:")
    st.write(average_levels_df)
    st.markdown("-----")

    # Define colors based on nutrient levels
    nutrient_colors = {
        'Very Low': 'navy',
        'Low': 'deepskyblue',
        'Sufficient': 'green',
        'High': 'orange',
        'Very High': 'red'
    }

    # Create a new column in average_levels_df to map nutrient levels to colors
    average_levels_df['Color'] = average_levels_df['Nutrient Level'].map(nutrient_colors)

    # Create a bar graph with true colors using Plotly Express
    st.subheader("Mean nutrient levels & standard deviation: ")

    fig = px.bar(
        average_levels_df,
        x='Average',
        y='Nutrient',
        error_x='Standard Deviation',
        color='Nutrient Level',  # Use the 'Nutrient Level' column for colors
        color_discrete_map=nutrient_colors,  # Map colors to nutrient levels
        labels={'Average': 'Mean Value (log)'},
        title='Average Nutrient Levels',
        orientation='h',  # Horizontal bar chart
        log_x=True,  # Set x-axis to log scale
    )

    # Customize the legend
    fig.update_layout(
        legend_title_text='Nutrient Status',
        legend=dict(
            x=1.1,
            y=1
        )
    )



    # Display the Plotly figure using Streamlit
    st.plotly_chart(fig)

   
    st.markdown("-----")
    st.subheader('Normality test & data distribution: ')

    # Create a 2x6 grid for the subplots
    fig = make_subplots(rows=2, cols=6, subplot_titles=list(nutrient_averages.keys()), shared_yaxes=False)

    # Create lists to store Shapiro-Wilk statistics and normality decisions
    shapiro_wilk_stats = []
    normality_decisions = []

    for nutrient, shapiro_wilk_stat, normality in zip(nutrient_averages.keys(), shapiro_wilk_values, normality_test_results):
        if nutrient in nutrient_ranges and shapiro_wilk_stat is not None:
            row_idx, col_idx = divmod(list(nutrient_averages.keys()).index(nutrient), 6)

            # Create a histogram
            hist_data = df[nutrient]
            hist, bin_edges = np.histogram(hist_data, bins=20, density=True)
            bin_centers = (bin_edges[1:] + bin_edges[:-1]) / 2
            fig.add_trace(go.Bar(x=bin_centers, y=hist, opacity=0.9, name='Data'), row=row_idx + 1, col=col_idx + 1)

            # Create a normal distribution curve (change line color to black)
            xmin, xmax = min(hist_data), max(hist_data)
            x = np.linspace(xmin, xmax, 100)
            p = stats.norm.pdf(x, nutrient_averages[nutrient], nutrient_stddevs[nutrient])
            fig.add_trace(go.Scatter(x=x, y=p, mode='lines', name='Fit', line=dict(color='black')), row=row_idx + 1, col=col_idx + 1)

            # Update subplot title with Shapiro-Wilk statistic
            shapiro_wilk_stats.append(shapiro_wilk_stat)
            normality_decision = "Normal" if shapiro_wilk_stat > 0.9 else "Not Normal"
            normality_decisions.append(normality_decision)

            fig.update_annotations(text=f'{nutrient}<br>Shapiro-Wilk: {shapiro_wilk_stat:.3f}<br>Normality: {normality}', selector=dict(row=row_idx + 1, col=col_idx + 1))

            # Configure axes
            if col_idx == 0:
                fig.update_yaxes(title_text='Density', row=row_idx + 1, col=col_idx + 1)

            fig.update_xaxes(title_text=nutrient, row=row_idx + 1, col=col_idx + 1)

    # Update layout for better spacing
    fig.update_layout(
        height=600,
        width=1200,
        showlegend=False,
        title_text="Data Distribution"
    )

    # Display the interactive plot
    st.plotly_chart(fig)

    # Create a table with Shapiro-Wilk statistics and normality decisions
    shapiro_wilk_table_data = {'Nutrient': list(nutrient_averages.keys()), 'Shapiro-Wilk Statistic': shapiro_wilk_stats, 'Normality Test': normality_decisions}
    st.write ("**Shapiro-Wilk Statistics and Normality Test:**")
    Shapiro_df = pd.DataFrame(shapiro_wilk_table_data)
    st.write(Shapiro_df)


    # Define the main Streamlit app
    def main():
        st.markdown("-----")  
        # Check if nutrient levels at Vegetative stage are "Very Low" and provide recommendations
        if crop_type == "Corn" and growth_stage == "Vegetative (V1-V9)":
            nutrient_Ca_level = classify_nutrient_level(nutrient_averages['Ca'], nutrient_ranges['Ca'])
            nutrient_N_level = classify_nutrient_level(nutrient_averages['N'], nutrient_ranges['N'])
            nutrient_K_level = classify_nutrient_level(nutrient_averages['K'], nutrient_ranges['K'])
            nutrient_Zn_level = classify_nutrient_level(nutrient_averages['Zn'], nutrient_ranges['Zn'])
            nutrient_Fe_level = classify_nutrient_level(nutrient_averages['Fe'], nutrient_ranges['Fe'])
            nutrient_Mg_level = classify_nutrient_level(nutrient_averages['Mg'], nutrient_ranges['Mg'])
            nutrient_Mn_level = classify_nutrient_level(nutrient_averages['Mn'], nutrient_ranges['Mn'])
            nutrient_S_level = classify_nutrient_level(nutrient_averages['S'], nutrient_ranges['S'])
            nutrient_P_level = classify_nutrient_level(nutrient_averages['P'], nutrient_ranges['P'])
            nutrient_B_level = classify_nutrient_level(nutrient_averages['B'], nutrient_ranges['B'])
            nutrient_Cu_level = classify_nutrient_level(nutrient_averages['Cu'], nutrient_ranges['Cu'])

            recommendations = []

            if nutrient_N_level == 0 :  
                recommendations.append({"Element": "Nitrogen", "Fertilizer 1": "Agri-N", "Application rate 1": "2 qts", "Fertilizer 2": "Midnight", "Application rate 2": "2 qts"})
            
            if nutrient_P_level == 4 :  
                recommendations.append({"Element": "Phosphorus", "Fertilizer 1": "Premium Blend", "Application rate 1": "2 qts"})

            if nutrient_K_level == 0 or 1:  
                recommendations.append({"Element": "Potassium", "Fertilizer 1": "K-28", "Application rate 1": "2 qts", "Fertilizer 2": "Premium Blend", "Application rate 2": "1 gal"})

            if nutrient_Cu_level or nutrient_Zn_level or nutrient_Mn_level or nutrient_B_level or nutrient_Fe_level== 0 :
                recommendations.append({"Element": "Micronutrients", "Fertilizer 1": "Microhance", "Application rate 1": "2 qts", "Fertilizer 2": "Drivas", "Application rate 2": "2 qts"})  

            if nutrient_S_level == 0 or 1:  
                recommendations.append({"Element": "Sulfur", "Fertilizer 1": "Sulfur 15 or Sulfur LC", "Application rate 1": "2 qts"})  

            if nutrient_Mg_level == 0 or 1:  
                recommendations.append({"Element": "Magnesium", "Fertilizer 1": "Mg 2.5%", "Application rate 1": "2 qts", "Fertilizer 2": "Nauxin", "Application rate 2": "2 qts"})   

            if nutrient_Ca_level == 0 or 1 or 2:  
                recommendations.append({"Element": "Calcium", "Fertilizer 1": "Calcium Plus", "Application rate 1": "2 qts", "Fertilizer 2": "Nauxin", "Application rate 2": "2 qts"}
) 


            if recommendations:
                st.subheader("**Fertilizer Recommendation:**")  
                st.write("**To avoid the nutrient deficiencies and subsequent yield loss, apply the following nutrient quantities per acre of farmland area (For more information consult a Monty's trusted advisor):**")
                recommendations_df = pd.DataFrame(recommendations)
                st.write(recommendations_df)

        # Check if nutrient levels at Vegetative stage are "Very Low" and provide recommendations
        elif crop_type == "Pepper" and growth_stage == "Fruiting":
            nutrient_S_level = classify_nutrient_level(nutrient_averages['S'], nutrient_ranges['S'])

            recommendations = []

            if nutrient_S_level == 1:  # "Very Low" S
                recommendations.append("S: Calcium Plus 2 Quarts, Nauxin 2 qts")

            if recommendations:
                st.subheader("**Fertilizer Recommendation:**")  
                st.write("**To avoid the nutrient deficiencies and subsequent yield loss, apply the following nutrient quantities per acre of farmland area (For more information consult a Monty's trusted advisor):**")
                recommendations_df = pd.DataFrame(recommendations)
                st.write(recommendations_df)

  


        # Create a button to generate the PDF report
        if st.button("💾 Generate PDF Report"):
            pdf_file_name = generate_pdf_report(results, crop_type, growth_stage)
            st.success(f"PDF Report generated. You can download it from [here](/{pdf_file_name}).")
    # Run the Streamlit app
    if __name__ == '__main__':
        main()

    # Function to generate PDF report
    def generate_pdf_report(results, crop_type, growth_stage):
        class PDF(FPDF.FPDF):
            def header(self):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, f"Nutrient Analysis Report for {crop_type} - {growth_stage}", align="C", ln=True)
                self.ln(10)

            def footer(self):
                self.set_y(-15)
                self.set_font("Arial", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", align="C")

            def chapter_title(self, title):
                self.set_font("Arial", "B", 12)
                self.cell(0, 10, title, 0, 1)
                self.ln(4)

            def chapter_body(self, body):
                self.set_font("Arial", "", 12)
                self.multi_cell(0, 10, body)
                self.ln()

        pdf = PDF()
        pdf.add_page()
        pdf.chapter_title(f"Nutrient Analysis Results for {crop_type} - {growth_stage}")
        
        # Add results to the PDF
        for nutrient, result in results.items():
            pdf.chapter_title(f"Plant tissue Analysis")
            pdf.chapter_body(f"Mean Value: {result['mean']:.2f}")
            pdf.chapter_body(f"Standard Deviation: {result['std']:.2f}")
            pdf.chapter_body(f"Recommendation: {result['recommendation']}")
            pdf.ln(10)

        # Save the PDF
        pdf_file_name = f"nutrient_analysis_{crop_type}_{growth_stage}.pdf"
        pdf.output(pdf_file_name)

        return pdf_file_name

    # Function to analyze nutrient levels
    def analyze_nutrient_levels(df, nutrient_ranges):
        results = {}
        for nutrient, ranges in nutrient_ranges.items():
            nutrient_values = df[nutrient]
            mean = np.mean(nutrient_values)
            std = np.std(nutrient_values)
            
            recommendation = ""
            for i, (low, high) in enumerate(ranges):
                if low <= mean <= high:
                    recommendation = f"Sufficient ({i+1})"
                    break
                elif mean < low:
                    recommendation = f"Low ({i+1})"
                    break
                elif mean > high:
                    recommendation = f"High ({i+1})"
            
            results[nutrient] = {
                "mean": mean,
                "std": std,
                "recommendation": recommendation,
            }
        
        return results

    # Perform nutrient analysis
    if nutrient_ranges is not None:
        results = analyze_nutrient_levels(df, nutrient_ranges)

    # Display nutrient analysis results and recommendations
    if nutrient_ranges is not None:
        results = analyze_nutrient_levels(df, nutrient_ranges)



