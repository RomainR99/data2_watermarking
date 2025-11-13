from numpy import asarray
from PIL import Image

def hide(msg,image_name):
    #image = Image.open(image_name)
    #data = asarray(image)
    #on force la copie

    image = Image.open(image_name).convert("RGB")
    data = asarray(image).copy()

    #Convertir le message en octet
    final_message=""
    for lettre in msg:
        position_ascii = ord(lettre) #donne les position des lettre de bonjour en numero ascii
        binaire = bin(position_ascii)[2:] #donne ascii en binaire avec 0b avant chaque bianaire 
                                                    #qu'on veut pas d'ou le sélecteure [2:]
        #met on veut 8 chiffre donc:
        while len(binaire) < 8:
            binaire = "0" + binaire
        #print(binaire) pour verifier
        final_message += binaire
    print("Message encodé en binaire:", final_message)   

    #Récupere la longueur et l'inscrit sur 2 octets (16bits) 
    longueur = len(final_message)
    binaire = bin(longueur)[2:] #c'est pas sur 2 octets dons on comble
    while len(binaire)<16:
        binaire = "0" + binaire
    print("Taille a encoder:",binaire)
    result_message = binaire + final_message #comme ca on encode en une fois

    print(data[0][0][0]) #on a le premier pixel colonne 0 et ligne 0 et la valeur du pixel

    #print(len(data[0])) # donne nombre de colonne
    #print(len(data)) # donne nombre de ligne
    
    tour=0
    y=0
    for line in data:
        x=0
        for colonne in line:
            rgb=0
            # for color in colonne:
            #     valeur=data[y][x][rgb]
            #     binaire=bin(valeur)[2:]
            #     binaire_list = list(binaire)
            #     del binaire_list[-1]
            #     binaire_list.append(result_message[tour])
            #     decimal = int("".join(binaire_list),2)
            #     data[y][x][rgb]=decimal
            #     tour +=1
            #     rgb +=1
            #     if tour>= len(result_message):
            #         break
            # x+=1
            for color in colonne:
                valeur = data[y][x][rgb]
                # rendre la valeur paire en mettant le bit de poids faible à 0
                valeur_pair = valeur & ~1   # efface le dernier bit → force un nombre pair
                data[y][x][rgb] = valeur_pair
                tour += 1
                rgb += 1
                if tour >= len(result_message):
                    break

            x += 1
        y+=1
        


        if tour>= len(result_message):
            break
    imagefinal =Image.fromarray(data)
    imagefinal.save("SECRET.png")

def discover(image_name):
    image =Image.open(image_name)
    data = asarray(image).copy()

    tour=0
    taille=""
    message=""
    taille_new=12345
    y=0
    for line in data:
        x=0
        for colonne in line:
            rgb=0
            for color in colonne:
                valeur=data[y][x][rgb]
                binaire=bin(valeur)[2:]
                last= binaire[-1]
                if tour<16:
                    taille+=16
                if tour==16:
                    taille_new=int(taille,2)
                if tour-16<taille_new-1:
                    message+=last
                if tour-16>=taille_new-1:
                    break
                tour+=1
                rgb +=1
            if tour-16<=taille_new-1:
                break
            x+=1
        if tour-16>=taille_new-1:
                break
        y+=1
    print(message)   
    octet=[]
    result = ""
    for i in range(len(message)//8):
        octet.append(message[i*8:(i+1)*8])
    print(octet)
    for oct in octet:
        index=int(oct,2)
        lettre_ascii=chr(index)
        print(lettre_ascii)
        result+=lettre_ascii
    print("MESSAGE",str(result[2:]))

#hide("bonjour","photo.png")
discover("SECRET.png")

