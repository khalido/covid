import streamlit as st

import numpy as np
import pandas as pd

st.header("NSW Covid Dashboard")

with st.beta_expander("See explanation"):
    st.write(
        """
    Choose R values in the cols below
    """
    )

# col1, col2, col3, col4 = st.beta_columns(4)

for i, col in enumerate(st.beta_columns(3)):
    col.write(f"R_{i+1}")
    col.bar_chart(np.random.random((10, 3)))


# we will need session state sooner or later, see
# https://docs.streamlit.io/en/stable/add_state_app.html
