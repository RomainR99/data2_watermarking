# 🔐 Projet : Stéganographie LSB + Chiffrement César & Vigenère (Unicode 21 bits)

Ce projet illustre comment cacher un message texte dans une image en utilisant :

- la **stéganographie LSB (Least Significant Bit)** ;
- un **chiffrement César Unicode** ;
- un **chiffrement Vigenère** basé sur César ;
- une interface **Streamlit** pour encoder et décoder facilement.

L’image résultante reste visuellement identique à l’œil humain mais contient un message chiffré dans les bits de poids faible de ses pixels.

---

## 📂 1. Objectifs du projet

- Encoder un message dans une image via **LSB**  
- Chiffrer le message avant insertion (**César** ou **Vigenère**)  
- Supporter **tous les caractères Unicode (21 bits)**  
- Fournir une interface web (**Streamlit**)  

---

## 📦 2. Création de l’environnement virtuel

Créer un environnement virtuel Python :


python3 -m venv watermarking_env


L’activer :

macOS / Linux :
source watermarking_env/bin/activate

Windows :
watermarking_env\Scripts\activate

---

## 📥 3. Installation des dépendances

Installer les librairies nécessaires :

pip install streamlit
pip install numpy
pip install pillow
pip install opencv-python   # facultatif, non requis par Streamlit

---

## 🧠 4. Fonctionnement

🔒 Chiffrement César

décalage Unicode modulo 1_114_112

support complet de tout l’espace Unicode

chiffrement et déchiffrement avec la même fonction :

cesar_cipher(text, key, cipher=True)

🔑 Chiffrement Vigenère (Unicode)

clé = mot de passe (chaîne)

chaque caractère du mot de passe → clé de César

modulo Unicode

vigenere_cipher(text, password, cipher=True)

🧬 Conversion texte → binaire (21 bits)

Chaque caractère Unicode est converti sur 21 bits fixes :

format(ord(char), "021b")


Avantages :

support des emojis

support multilingue

reconstruction fiable

🖼 Stéganographie LSB
Encodage :

Chiffrer le message (César ou Vigenère)

Convertir en binaire (21 bits par caractère)

Encoder la taille (32 bits)

Mettre tous les pixels à pair (& 0b11111110)

Insérer chaque bit du message dans le LSB

Sauvegarder secret.png

Décodage :

Lire tous les LSB

Extraire la taille

Reformer les blocs de 21 bits → Unicode

Déchiffrer avec la même clé

---

## 🖥 5. Lancer l’application Streamlit

Depuis le dossier racine, exécuter :


streamlit run app.py


L’application ouvre automatiquement votre navigateur :

Onglet Encoder un message

Onglet Décoder un message

---

## 🗂 6. Structure du projet

data2_watermarking/
│
├── app.py                   # Interface Streamlit
├── steganographie.py        # LSB + Unicode + encode/decode
├── backend.py               # César + Vigenère
│
├── photo.png                # Image source
├── secret.png               # Image générée
│
├── cmd_env_virtuel.png      # Capture 1
└── cmd_librairie_python_ds_env_virtuel.png  # Capture 2

---

## 🛠 7. Extensions possibles

ajouter AES-256 avant LSB

visualiser les bits LSB dans l’interface

comparer l’image originale et modifiée

détecter automatiquement la présence d’un message caché

---

## 🎉 8. Résultat final

Ce projet combine :

✔ Cryptographie (César, Vigenère)
✔ Stéganographie LSB
✔ Interface Web Streamlit
✔ Support Unicode complet (21 bits)



