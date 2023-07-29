import streamlit as st
import requests
import os
import base64
from streamlit_option_menu import option_menu
import streamlit as st
import pdf2image
import os
from io import BytesIO


def save_pdf_from_url(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)

def get_download_link(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    href = f'<a href="data:application/pdf;base64,{b64}" download> Télécharger le fichier PDF </a>'
    return href



st.title("URL to PDF Downloader")
st.write("Entrez l'URL du PDF que vous souhaitez télécharger et obtenir le lien de téléchargement.")

    # 1. as sidebar menu
with st.sidebar:
        sidebar_selection = option_menu(" Menu", ['Home','URL','pdf2_image','Layout parser','Extract Table','Question Answering','footprint','Chatboot','Upload json file','Settings','contact' ], 
            icons=['house','file-earmark-pdf-fill','bi bi-file-earmark-image','bi bi-columns-gap','table','bi bi-patch-question-fill','bi bi-app','bi bi-chat-left-dots-fill','bi bi-filetype-json','gear','bi bi-person-lines-fill'], menu_icon="cast", default_index=1)
        sidebar_selection

if sidebar_selection == 'URL':    
        # Saisie de l'URL du PDF
        pdf_url = st.text_input("URL du PDF")

        if pdf_url and st.button("Télécharger"):
            try:
                # Récupérer le nom du fichier à partir de l'URL et ajouter l'extension .pdf
                file_name = pdf_url.split('/')[-1] + ".pdf"
                # Chemin d'accès complet pour enregistrer le PDF
                folder_path = "downloads"
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, file_name)
                # Télécharger le PDF depuis l'URL
                save_pdf_from_url(pdf_url, file_path)
                st.success(f"Le PDF a été téléchargé avec succès !")
                st.info("Cliquez sur le lien ci-dessous pour télécharger le fichier.")
                # Afficher le lien de téléchargement
                st.markdown(get_download_link(file_path), unsafe_allow_html=True)
            except Exception as e:
                st.error("Une erreur s'est produite lors du téléchargement du PDF.")
                st.error(e)

if sidebar_selection == 'pdf2_image':
        pdf_uploaded = st.file_uploader("Select a file", type="pdf")
        button = st.button("Confirm")
        image_down = []
        st.write("test1")
        if button and pdf_uploaded is not None:
            st.write("test2")
            if pdf_uploaded.type == "application/pdf":
                st.write("test3")
                images = pdf2image.convert_from_bytes(pdf_uploaded.read())
                for i, page in enumerate(images):
                    st.write(i)
                    st.write(page)
                    st.image(page, use_column_width=True)
                    img = page
                    buf = BytesIO()
                    img.save(buf, format="JPEG")
                    byte_im = buf.getvalue()
                    st.download_button("Download", data=byte_im, file_name=f"Image_{i}.png")



   
