import streamlit as st
from utils import extract_text, summarize_text, translate_to_hindi

st.set_page_config(page_title="Summarizer App")

st.title("📄 AI Summarizer App")
st.write("Upload your file and get summary")

uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")

    file_type = uploaded_file.name.split(".")[-1]

    text = extract_text(uploaded_file, file_type)

    st.subheader("Extracted Text Preview")
    preview = " ".join(text.split()[:500])
    st.write(preview)

    if st.button("Generate Summary"):
        with st.spinner("Generating summary... ⏳"):

            summary = summarize_text(text)

            # enforce 500-word limit
            summary = " ".join(summary.split()[:500])

            hindi_summary = translate_to_hindi(summary)

            st.subheader("📌 English Summary")
            st.write(summary)

            st.subheader("📌 Hindi Summary")
            st.write(hindi_summary)

            st.download_button(
                label="📥 Download English Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

            st.download_button(
                label="📥 Download Hindi Summary",
                data=hindi_summary,
                file_name="summary_hindi.txt",
                mime="text/plain"
            )
