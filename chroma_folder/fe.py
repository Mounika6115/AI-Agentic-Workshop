#  # streamlit
# it is py third party lib / package which is used to build ui based with python


# pip install streamlit
# pip install requests
# python -m pip install requests

import streamlit as st
import requests as r

be_srever_url_loc="http://127.0.0.1:8000"
st.title("AI RESUME ANALYZER")

resume=st.file_uploader("UploadResumePdf",type=["pdf"])
submit_btn=st.button("AnalyzeResume")

if submit_btn:
    mouni=r.post(f"{be_srever_url_loc}/anylyse_resume", files={"resume": resume})
    st.write(mouni)
    if mouni.status_code == 200:
        st.write(mouni.json()["msg"])
    # f"{be.server_loc}/anylyse_resume"
    

# Run:python -m streamlit run fe.py

# http://127.0.0.1:8000/anylyse_resume
# email :-

# st.info()
# st.success()
# st.warning()
# st.text_input()  etc..
