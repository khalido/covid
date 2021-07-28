import streamlit as st

import numpy as np
import pandas as pd


# import plotly.express as px
# import plotly.graph_objects as go

# my files
import data
import static

st.set_page_config(layout="wide")

st.header("NSW Covid Dashboard")

with st.beta_expander("This page -does- will do stuff"):
    st.write(
        """
    Currently just a simple static graph of daily cases in NSW. More to follow:

    - interactive version of cases
    - vaccine plots
    - extrapolation of cases and the effect of Vaccines
    
    Now all this is done already on much better dashboards, so this is just for my own self. 
    
    Wear a mask.
    """
    )


# col1, col2, col3, col4 = st.beta_columns(4)

#for i, col in enumerate(st.beta_columns(3)):
#    col.button(f"R_{i+1}")
    # col.bar_chart(np.random.random((10, 3)))


# we will need session state sooner or later, see
# https://docs.streamlit.io/en/stable/add_state_app.html

@st.cache(ttl=3600)
def get_data():
    df = data.get_data()
    print(f"using dataframe with shape {df.shape}")
    return df


fig = static.make_plot(df)
st.pyplot(fig)

st.subheader("Raw Data")
st.write("this data is a bit too busy....")
st.write(df)