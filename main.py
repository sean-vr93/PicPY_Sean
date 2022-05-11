
from tkinter import *
from tkinter.font import BOLD, Font
from tkinter import filedialog as tfd
from tkinter import messagebox as tmb
import sys, os, sys, PIL
from PIL import ImageTk, Image

class Lecteur_Image(object):
    def __init__(self):
        # Paramètres fenetre
        self.fenetre = Tk()
        self.fenetre.geometry("1920x1080")
        self.fenetre.title("PyPICTURES")
        self.fenetre.config(background='#283f4a')
        # Polices
        self.bold25 = Font(self.fenetre, size=25, weight=BOLD)
        # Variables et listes
        self.boutons_apres = False
        self.filetypes = [("Tous les fichiers","*.*"),(".png","*.png"),(".jpeg","*.jpeg"),(".gif","*.gif"),(".jpg","*.jpg")]
        ###########################################################################################################################################
        # Frame Boutons
        self.affichage_boutons_frame = Frame(self.fenetre, background='#283f4a')
        self.affichage_boutons_frame.pack(side=TOP,padx=5,pady=5)
        # Bouton Image Ajouter -> Frame Boutons
        self.affichage_boutons_ajouter = Button(self.affichage_boutons_frame, command=self.afficher_image_choix, text="Sélectionner une Image")
        self.affichage_boutons_ajouter.pack()
        self.affichage_image_label_nom = Label(self.affichage_boutons_frame, background='#283f4a', foreground="white")
        self.affichage_image_label_nom.pack()
        ###########################################################################################################################################
        # Frame Image
        self.affichage_image_frame = Frame(self.fenetre, background='#283f4a')
        self.affichage_image_frame.pack(side=TOP,padx=5)
        # Label Image -> Frame Image
        self.affichage_image_label = Label(self.affichage_image_frame, background='#283f4a')
        self.affichage_image_label.pack()
        ###########################################################################################################################################

    def afficher_image_choix(self):
        try:
            self.img = tfd.askopenfilename(title="Choisissez un fichier à renommer",filetypes=self.filetypes)
            self.image = Image.open(self.img)
            self.s = self.image.size
            if self.s[0] > 1600 or self.s[1] > 900:
                self.resize_image()
            self.image = ImageTk.PhotoImage(self.image)
            self.affichage_image_label.config(image=self.image, height=900, width=1600)
            self.img_nom = os.path.basename(self.img)
            self.affichage_image_label_nom.config(text=self.img_nom)
            self.img_dossier = os.path.dirname(self.img)
            self.img_dossier_liste = os.listdir(self.img_dossier)
            self.liste_all_images = []
            for item in self.img_dossier_liste:
                if item.endswith(('.png', '.jpeg', '.gif', '.jpg')):
                    self.liste_all_images.append(item)
                else:
                    pass
            if self.boutons_apres == False:
                self.boutons_frame = Frame(self.fenetre, background='#283f4a')
                self.boutons_frame.pack(side=TOP,padx=5)
                self.bouton_image_precedente = Button(self.boutons_frame, command=self.precedente_image_methode, text ="Image Précédente")
                self.bouton_image_precedente.grid(row=0,column=0,padx=10)
                self.label_liste_nombre_image = Label(self.boutons_frame, background='#283f4a', foreground='white')
                self.label_liste_nombre_image.grid(row=0, column=1, padx=10)
                self.bouton_image_suivante = Button(self.boutons_frame, command=self.prochaine_image_methode, text ="Image Suivante")
                self.bouton_image_suivante.grid(row=0,column=2,padx=10)
                self.boutons_apres = True
            if self.boutons_apres == True:
                self.index_img = int(self.liste_all_images.index(self.img_nom))
                self.label_liste_nombre_image.config(text ="Image "+str(self.index_img+1)+" sur "+str(len(self.liste_all_images)))
        except PIL.UnidentifiedImageError:
            tmb.showerror(title="Erreur", message="Le fichier selectionné n'est pas une image.")

    def prochaine_image_methode(self):
        if self.img_dossier_liste != []:
            self.index_img = int(self.liste_all_images.index(self.img_nom)+1)
            if self.index_img > len(self.liste_all_images) - 1:
                self.index_img = 0
            self.label_liste_nombre_image.config(text ="Image "+str(self.index_img+1)+" sur "+str(len(self.liste_all_images)))
            self.prochaine_image = str(self.img_dossier+"/"+self.liste_all_images[self.index_img])
            self.img_nom = os.path.basename(self.prochaine_image)
            self.affichage_image_label_nom.config(text=self.img_nom)
            self.image = Image.open(self.prochaine_image)
            self.s = self.image.size
            if self.s[0] > 1600 or self.s[1] > 900:
                self.resize_image()
            self.image = ImageTk.PhotoImage(self.image)
            self.affichage_image_label.config(image=self.image, height=900, width=1600)
            self.affichage_image_label.image = self.image

    def precedente_image_methode(self):
        if self.img_dossier_liste != []:
            self.index_img = int(self.liste_all_images.index(self.img_nom)-1)
            if self.index_img < 0:
                self.index_img = len(self.liste_all_images) - 1
            self.label_liste_nombre_image.config(text ="Image "+str(self.index_img+1)+" sur "+str(len(self.liste_all_images)))
            self.precedente_image = str(self.img_dossier+"/"+self.liste_all_images[self.index_img])
            self.img_nom = os.path.basename(self.precedente_image)
            self.affichage_image_label_nom.config(text=self.img_nom)
            self.image = Image.open(self.precedente_image)
            self.s = self.image.size
            if self.s[0] > 1600 or self.s[1] > 900:
                self.resize_image()
            self.image = ImageTk.PhotoImage(image = self.image)
            self.affichage_image_label.config(image=self.image,height=900,width=1600)
            self.affichage_image_label.image = self.image

    def resize_image(self):
        largeur_ratio = 1600 / self.s[0]
        hauteur_ratio = 900 / self.s[1]
        meilleur_ratio = min(largeur_ratio, hauteur_ratio)
        w =  int(round(self.s[0] * meilleur_ratio))
        h = int(round(self.s[1] * meilleur_ratio))
        self.image = self.image.resize((w,h))

if __name__ == "__main__":
    app = Lecteur_Image()
    app.fenetre.mainloop()
    sys.exit()
