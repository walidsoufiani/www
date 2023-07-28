import streamlit as st
import requests
import os
import base64
from streamlit_option_menu import option_menu
import fitz  
import PyMuPDF


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

def convert_pdf_to_images(pdf_file):
    images = []
    pdf_document = fitz.open("pdf", pdf_file.read())
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        for img_number, img in enumerate(image_list):
            images.append(img[0].get_pixmap())

    pdf_document.close()
    return images

st.title("URL to PDF Downloader")
st.write("Entrez l'URL du PDF que vous souhaitez télécharger et obtenir le lien de téléchargement.")

def main():
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
        # Titre de l'application
        st.title("Conversion PDF en images")

        # Afficher le bouton de téléchargement de fichier PDF
        uploaded_file = st.file_uploader("Téléchargez un fichier PDF", type="pdf")

        # Vérifier si un fichier a été téléchargé
        if uploaded_file is not None:
            # Convertir le PDF en images
            images = convert_pdf_to_images(uploaded_file)

            # Afficher les images en rangées sur Streamlit
            row_num = len(images) // 3 + 1
            selected_images = []

            # Afficher le choix pour sélectionner une seule image ou toutes les images
            choice = st.radio("Choisissez une option :", options=["Choisir une image", "Choisir toutes les images"])

            if choice == "Choisir une image":
                for row in range(row_num):
                    columns = st.columns(3)
                    for i, column in enumerate(columns):
                        index = row * 3 + i
                        if index < len(images):
                            # Afficher l'image et la case à cocher correspondante
                            image = images[index]
                            checkbox = column.checkbox(label="", key=f"checkbox_{index}")
                            if checkbox:
                                selected_images.append(image)
                            column.image(image, use_column_width=True)

            else:  # Choisir toutes les images
                selected_images = images

                for row in range(row_num):
                    columns = st.columns(3)
                    for i, column in enumerate(columns):
                        index = row * 3 + i
                        if index < len(images):
                            # Afficher l'image
                            column.image(images[index], use_column_width=True)

            # Bouton pour sauvegarder les images sélectionnées
            if len(selected_images) > 0:
                st.write("---")
                save_directory = st.text_input("Chemin de sauvegarde des images", value="chemin/vers/repertoire")
                if choice == "Choisir toutes les images":
                    if st.button("Sauvegarder toutes les images"):
                        for i, image in enumerate(images):
                            image_path = os.path.join(save_directory, f"image_{i}.png")
                            image.save(image_path, "PNG")
                        st.success("Toutes les images sauvegardées avec succès!")
                else:
                    if st.button("Sauvegarder les images sélectionnées"):
                        for i, image in enumerate(selected_images):
                            image_path = os.path.join(save_directory, f"image_{i}.png")
                            image.save(image_path, "PNG")
                        st.success("Images sauvegardées avec succès!")

if __name__ == "__main__":
    main()
