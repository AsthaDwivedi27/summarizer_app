import streamlit as st
from utils import extract_text_from_pdf, generate_summary, translate_to_hindi

st.set_page_config(page_title="Summarizer App", layout="centered")

st.title("AI Summarizer")
st.write("Upload a file and get English + Hindi summary.")

uploaded_file = st.file_uploader("Upload the File", type=["pdf"])

if uploaded_file is not None:

    if st.button("Generate Summary"):

        with st.spinner("Processing File..."):

            text = extract_text_from_pdf(uploaded_file)

            english_summary = generate_summary(text)

            hindi_summary = translate_to_hindi(english_summary)

        st.success("Summary Generated!")

        st.subheader("English Summary")
        st.write(english_summary)

        st.subheader("Hindi Summary")
        st.write(hindi_summary)

        st.download_button(
            "Download English Summary",
            data=english_summary,
            file_name="english_summary.txt"
        )

        st.download_button(
            "Download Hindi Summary",
            data=hindi_summary,
            file_name="hindi_summary.txt"
        )
