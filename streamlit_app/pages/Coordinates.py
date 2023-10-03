import pandas as pd
from PIL import Image
import streamlit as st
import numpy as np
from streamlit_drawable_canvas import st_canvas



objects = []
left_shelf = []
right_shelf = []
flag = False
st.session_state["drawing_mode"] = "point"


if st.session_state.drawing_mode == 'point':
    point_display_radius = "3"
elif st.session_state.drawing_mode == 'none':
    point_display_radius = "0"
bg_image = st.sidebar.camera_input("Background image:")

realtime_update = True

col1, col2 = st.columns(2)
with col1:
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)", 
        stroke_width="1",
        stroke_color="#000000",
        background_color="#eee",
        background_image=Image.open(bg_image) if bg_image else None,
        update_streamlit=realtime_update,
        height=300, width=350,
        drawing_mode="point",
        point_display_radius=point_display_radius if st.session_state.drawing_mode == 'point' else 0,
        key="canvas",
    )


    if len(objects) < 5 :
        if canvas_result.image_data is not None:
            st.image(canvas_result.image_data)
        if canvas_result.json_data is not None:
            objects = pd.json_normalize(canvas_result.json_data["objects"])
            for col in objects.select_dtypes(include=['object']).columns:
                objects[col] = objects[col].astype("str")
                num_of_rows = len(objects)
                if num_of_rows < 4:
                    print (objects["left"])
                else: 
                    st.session_state.drawing_mode = "none"
with col2:                    
        df = pd.DataFrame(objects)
        if len(objects) != 0:
            points = df[['left','top']]
            top4 = points.head(4)
            array = top4.to_numpy()
            print(array)
            
            left_shelf = array
            st.success("Coordinates are saving..")

            next4 = points.iloc[3:7]
            array2 = next4.to_numpy()
            print(array2)

            right_shelf = array2
        else: 
            st.error("Select four points to cover a region")
        col1, col2 = st.columns(2)
        with col1:
            st.write("First Shelf")
            st.write(left_shelf)
        with col2:
            st.write("Second Shelf")
            st.write(right_shelf)
            