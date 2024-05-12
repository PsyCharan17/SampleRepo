import streamlit as st
import pdfplumber, base64
from data_processor import extract_data_from_pdf, extract_transcript, extract_text_from_url
from graph_retrieval_system import GraphRAG
from llm_processor import llm_invoker
from datetime import time

def main():
    st.set_page_config(page_title="AI Notes Maker", page_icon=":notebook_with_decorative_cover:")
    st.markdown("<style>body { background-color: black; color: white; }</style>", unsafe_allow_html=True)
    st.title("AI Notes Maker")

    content_type = st.selectbox("Select content type", ["PDF", "YouTube Link", "Website", "PowerPoint"])

    if content_type in ["YouTube Link", "Website"]:
        link = st.text_input("Enter the link")
    else:
        file = st.file_uploader(f"Upload a {content_type.lower()} file")

    if st.button("Submit"):
        if content_type == "PDF":
            if file is not None:
                bytes_data = file.getvalue()
                file2 = base64.b64encode(bytes_data)
                notes_data = extract_data_from_pdf(file2)
            else:
                st.warning("Please upload a PDF file.")
        elif content_type == "YouTube Link":
            if link:
                notes_data = extract_transcript(link)
            else:
                st.warning("Please enter a YouTube link.")
        elif content_type == "Website":
            if link:
                st.markdown(f'<iframe src="{link}" width="800" height="600"></iframe>', unsafe_allow_html=True)
                notes_data = extract_text_from_url(link)
            else:
                st.warning("Please enter a website link.")

        if notes_data:
            graph_rag = GraphRAG()
            llm = llm_invoker()
            graph_rag.constructGraph(notes_data)
            print("hello")
            sumamrized_data = []
            print("check 123")
            print(len(graph_rag.lines))
            i = 0
            while(i < len(len(graph_rag.lines)-1)):
                print("helllooo")
                temp_data = llm.process_chunks(graph_rag.lines[i] + graph_rag.lines[i+1]) 
                print(temp_data)
                sumamrized_data.append(temp_data)
            for i in range(0,len(graph_rag.lines)-1,2):
                print("helllooo")
                temp_data = llm.process_chunks(graph_rag.lines[i] + graph_rag.lines[i+1]) 
                print(temp_data)
                sumamrized_data.append(temp_data)
            
            final_notes = ""
            for i in range(0, len(sumamrized_data)-2, 3):
                print("helllooooo")
                sentence = sumamrized_data[i]+" "+ sumamrized_data[i+1]+" "+ sumamrized_data[i+2]
                temp_data = llm.process_notes(sentence)
                print(len(sentence))
                print("____")
                print(sentence)
                final_notes += temp_data
                time.sleep(21)

            st.write(final_notes)

                


if _name_ == "_main_":
    main()