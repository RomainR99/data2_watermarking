from numpy import asarray
from PIL import Image
#on enleve sinon streamlit plante
#import cv2 #librairie OpenCV : pip install opencv-python 
from backend import cesar_cipher   # mport de fonction

#on enleve sinon streamlit plante
# def afficher_image(image_name):
#     image = cv2.imread(image_name)  # charge l'image
#     cv2.imshow("Image importée", image)  # affiche l'image
#     cv2.waitKey(0)  # attend qu'une touche soit pressée
#     cv2.destroyAllWindows()  # ferme la fenêtre


#afficher_image("photo.png")


# Convertir texte → Unicode → binaire 21 bits
def texte_en_binaire_unicode(msg):
    binaire = ""
    for lettre in msg:
        code = ord(lettre)                 # Unicode (0 → 1 114 111)
        binaire += format(code, "021b")    # 21 bits
    return binaire

# HIDE : msg -> Unicode en 21 bits 
# pixel pair = 0, pixel impair = 1
def hide(msg, image_name,key):
    msg_chiffre = cesar_cipher(msg, key, cipher=True) #Chiffrement msg en César 
    print("Message chiffré :", msg_chiffre)
    image = Image.open(image_name).convert("RGB") # load image RGB
    data = asarray(image).copy()
    h, w, _ = data.shape
    bits_message = texte_en_binaire_unicode(msg_chiffre)  # on encode le message CHIFFRÉ
    taille = len(bits_message)
    taille_bits = format(taille, "032b")
    bits = taille_bits + bits_message
    total_bits = len(bits)

    #Rend  pixels paires  0b11111110 = 254
    for y in range(h):
        for x in range(w):
            for c in range(3):
                data[y, x, c] = data[y, x, c] & 0b11111110   # LSB = 0 LSB:Least Significant Bit
                #Il n’y a que un seul opérateur (&), donc pas besoin de parenthèses comme endessous

    # Encodage des bits 0b11111110 = 254
    index = 0
    for y in range(h):
        for x in range(w):
            for c in range(3):
                if index >= total_bits:
                    break
                bit = int(bits[index])  # 0 ou 1
                # Pixel pair
                data[y, x, c] = (data[y, x, c] & 0b11111110) | bit
                #opérateur & a une priorité différente de |
                index += 1
            if index >= total_bits:
                break
        if index >= total_bits:
            break

    # Sauvegarde image finale
    out = Image.fromarray(data.astype("uint8"))
    out.save("secret.png")
    print("Message_secret.png")



def discover(image_name, key): #key de César
    image = Image.open(image_name).convert("RGB")
    data = asarray(image)
    h, w, _ = data.shape

    bits = []

    # Lecture des LSB
    for y in range(h):
        for x in range(w):
            for c in range(3):
                bits.append(str(data[y, x, c] & 1))

    bits = "".join(bits)

    # Lire la taille sur 32 bits
    taille_bits = bits[:32]
    taille = int(taille_bits, 2)

    # Lire les bits du message
    message_bits = bits[32:32 + taille]

    # Reconstruction en blocs de 21 bits
    texte_chiffre = ""
    for i in range(0, taille, 21):
        bloc = message_bits[i:i+21]
        code = int(bloc, 2)
        texte_chiffre += chr(code)

    print("Texte chiffré extrait :", texte_chiffre)

    # Déchiffrement César
    texte_dechiffre = cesar_cipher(texte_chiffre, key, cipher=False)
    print("Message extrait déchiffré :", texte_dechiffre)

    return texte_dechiffre


# TEST
if __name__ == "__main__":
    cle = 12
    hide("Bonjour", "photo.png",cle)
    discover("secret.png",cle)

