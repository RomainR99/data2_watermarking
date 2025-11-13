import streamlit as st
from steganographie import hide, discover
from PIL import Image
from io import BytesIO
import os
import uuid


st.set_page_config(page_title="Stéganographie LSB + César", layout="centered")

st.title("🔐 Stéganographie LSB + Chiffrement César")
st.write("Encode et décode un message caché dans une image, avec chiffrement César + Unicode 21 bits.")


tab_encode, tab_decode = st.tabs(["📝 Encoder un message", "📖 Décoder un message"])


# ==========================================================
# 📝 ONGLET ENCODAGE
# ==========================================================
with tab_encode:
    st.header("Encoder un message dans une image")

    uploaded_image = st.file_uploader("Choisis une image de base (photo.png, etc.)", type=["png", "jpg", "jpeg"])
    message = st.text_area("Message à cacher")
    key = st.number_input("Clé du chiffrement César (entier)", min_value=0, max_value=1_114_111, value=12, step=1)

    if st.button("Encoder le message"):
        if uploaded_image is None:
            st.error("⚠ Merci de sélectionner une image.")
        elif not message:
            st.error("⚠ Merci de saisir un message.")
        else:
            # Sauvegarder l'image uploadée dans un fichier temporaire
            temp_input_name = f"input_{uuid.uuid4().hex}.png"
            img = Image.open(uploaded_image).convert("RGB")
            img.save(temp_input_name)

            # Appeler ta fonction hide (qui enregistre secret.png)
            try:
                hide(message, temp_input_name, key)
            except Exception as e:
                st.error(f"Erreur pendant l'encodage : {e}")
            finally:
                # Nettoyage du fichier temporaire
                if os.path.exists(temp_input_name):
                    os.remove(temp_input_name)

            # Charger l'image secrète générée (secret.png)
            if os.path.exists("secret.png"):
                secret_img = Image.open("secret.png")
                st.success("✅ Message encodé avec succès dans `secret.png`.")
                st.image(secret_img, caption="Image avec message caché", use_column_width=True)

                # Préparer le téléchargement
                buf = BytesIO()
                secret_img.save(buf, format="PNG")
                buf.seek(0)

                st.download_button(
                    label="📥 Télécharger l'image secrète",
                    data=buf,
                    file_name="secret.png",
                    mime="image/png"
                )
            else:
                st.error("❌ Impossible de trouver `secret.png`. Vérifie la fonction hide().")


# ==========================================================
# 📖 ONGLET DÉCODAGE
# ==========================================================
with tab_decode:
    st.header("Décoder un message depuis une image")

    uploaded_secret = st.file_uploader("Choisis l'image contenant le message (secret.png)", type=["png", "jpg", "jpeg"])
    key_dec = st.number_input("Clé du chiffrement César utilisée pour l'encodage", 
                              min_value=0, max_value=1_114_111, value=12, step=1, key="decode_key")

    if st.button("Décoder le message"):
        if uploaded_secret is None:
            st.error("⚠ Merci de sélectionner une image secrète.")
        else:
            # Sauvegarder l'image secrète dans un fichier temporaire
            temp_secret_name = f"secret_{uuid.uuid4().hex}.png"
            img_secret = Image.open(uploaded_secret).convert("RGB")
            img_secret.save(temp_secret_name)

            try:
                texte = discover(temp_secret_name, key_dec)
                st.success("✅ Message décodé avec succès :")
                st.code(texte, language="text")
            except Exception as e:
                st.error(f"Erreur pendant le décodage : {e}")
            finally:
                if os.path.exists(temp_secret_name):
                    os.remove(temp_secret_name)
