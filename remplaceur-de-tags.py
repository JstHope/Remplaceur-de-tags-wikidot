# !!!!!!!! LIBRARY !!!!!!!! pip install lxml requests bs4 colorama

# Envoyer des requêtes HTTP et fonctions propres aux systèmes
import requests,sys
# Parseur HTML et XML
from bs4 import BeautifulSoup
# Permet d’afficher une sortie en couleurs, entre autres (inutilisé dans le fonctionnement de fond)
from colorama import Fore
import colorama

# Pour générer un token7 aléatoire
from random import randint

################### À MODIFIER ######################## Tutoriel : https://prnt.sc/GipvrEQ1dbDo ||| https://prnt.sc/i1sBMkKe1J2T ||| https://prnt.sc/ePwFDuvo-H9O
USERAGENT = ''
SESSION_ID = ''
#######################################################
#génére un token random
TOKEN7 = str(randint(10000000000,100000000000))

THESERVER = 'fondationscp'

colorama.init()
# Retourn la liste des tags d’une page ainsi que son ID Wikidot.
# url : l’url de la page sur laquelle chercher les tags et l’ID
def get_tags_id(url):
	# Va chercher la page HTML de l’url donnée
    r = requests.get(url, headers={'User-Agent':USERAGENT,'Cookie':'WIKIDOT_SESSION_ID=' + SESSION_ID + '; wikidot_token7=' + TOKEN7 + ';'},data={'wikidot_token7':TOKEN7})
    # Interprète l’HTML
    results = BeautifulSoup(r.text, features='lxml')
    # Récupère la liste des tags en allant chercher dans le div des tags les liens de tags
    # L’organisation des tags sur les pages est <div class="page-tags"><span>Liste des tags</span></div>
    # avec chaque tag sous la forme d’un lien <a href="liendutag">nomdutag</a>
    # On a donc ici une liste de toutes les balises de lien de tags
    all_results = results.select('div.page-tags > span > a')
    # Retourne les textes dans les balises de lien en retirant tout caractère en trop (espace, autres mots)
    results = [r.text.split(' ')[0].strip() for r in all_results]
   	# Récupère l’identifiant de la page par une recherche dans le code source
   	# Celui-ci est situé dans un script Javascript dans la balise <head>
    rr = r.text
    # Se positionne au départ de l’identifiant
    startindex = rr.find('WIKIREQUEST.info.pageId = ')
    id_page = ''
    k=''
    count = 0
    # Récupère l’identifiant de la page caractère par caractère
    while k != ';':
        count += 1
        k = rr[startindex + 25 + count]
        id_page += k

    return results,id_page[:-1] # Retire le dernier caratère de id_page qui est un point-virgule.

# Ajoute un tag newTag à une page link
def addtag(newTag,link):
	# Retourne la liste des tags et l’identifiant de la page link
    tags,ids = get_tags_id(link)
    # Forme la liste de tags à uploader (tous les tags actuels) séparés par des espaces
    uploadtags = ''
    for i in range(len(tags)):
        uploadtags += tags[i] + ' '
    # Ajoute le tag à ajouter à la liste totale des tags
    uploadtags += newTag
    # Envoie une requête à Wikidot pour renvoyer tous les tags sur la page
    requests.post(url = 'http://' + THESERVER + '.wikidot.com/ajax-module-connector.php', headers={'Host': THESERVER + '.wikidot.com','User-Agent': USERAGENT,'Cookie': 'wikidot_token7=' + TOKEN7 + '; WIKIDOT_SESSION_ID='+ SESSION_ID + ';'},data={'tags':uploadtags,'pageId':ids,'action':'WikiPageAction','event':'saveTags','moduleName':'Empty','callbackIndex':'1','wikidot_token7':TOKEN7})

# Remplace un tag oldTag par un tag newTag sur une page link
def replacetag(newTag,oldTag,link):
	# Retourne la liste des tags et l’identifiant de la page link
    tags,ids = get_tags_id(link)
    # Supprime le tag oldTag
    del tags[tags.index(oldTag)]
    # Forme la liste de tags à uploader (tous les tags actuels à l’exception de celui retiré) séparés par des espaces
    uploadtags = ''
    for i in range(len(tags)):
        uploadtags += tags[i] + ' ' # Le tag supprimé va faire que deux espaces vont se suivre
    uploadtags += newTag # Ajout du nouveau tag à la liste totale
    # Envoie une requête à Wikidot pour renvoyer tous les tags sur la page
    requests.post(url = 'http://' + THESERVER + '.wikidot.com/ajax-module-connector.php', headers={'Host': THESERVER + '.wikidot.com','User-Agent': USERAGENT,'Cookie': 'wikidot_token7=' + TOKEN7 + '; WIKIDOT_SESSION_ID='+ SESSION_ID + ';'},data={'tags':uploadtags,'pageId':ids,'action':'WikiPageAction','event':'saveTags','moduleName':'Empty','callbackIndex':'1','wikidot_token7':TOKEN7})

# Retourne toutes les pages ayant le tag demandé, d’abord leurs titres puis leurs liens.
def finddallpageswithtag(tag):
	# Récupère la page du tag donné
    r = requests.get('http://' + THESERVER + '.wikidot.com/system:page-tags/tag/' + tag, headers={'User-Agent':USERAGENT,'Cookie':'WIKIDOT_SESSION_ID=' + SESSION_ID + '; wikidot_token7=' + TOKEN7 + ';'},data={'wikidot_token7':TOKEN7})
    # Interprète l’HTML
    results = BeautifulSoup(r.text, features='lxml')
    # Retourne la liste des liens présents dans la page dans les divs qui présentent la liste des pages
    all_results = results.select('div.pages-list > div.pages-list-item > div.title > a')
    # Récupère le texte de toutes les balises liens, soit les titres des pages
    titles = [r.text for r in all_results]
    # Transforme les noms de pages en réelles URLs
    links = ['http://' + THESERVER + '.wikidot.com' + r['href'] for r in all_results]
    if all_results == []: # S’il n’y a aucun lien sur la page à cet endroit
        print(Fore.BLUE + "\n[INFO] " + Fore.WHITE + "Votre tag n'apparait sur aucune page")
        exit()
    return titles,links

# Paramètres d’appel du programme
methode = None
oldtag = None
newtag = None

if len(sys.argv) == 1 or sys.argv[1] == '-h': # Si on demande l’aide ou qu’il n’y a aucun paramètre
	# Affichage d’un texte en Ascii Art, avec un texte d’aide le tout en couleurs
    print(Fore.CYAN + "\n _____               _                          _        _____            \n| __  |___ _____ ___| |___ ___ ___ _ _ ___    _| |___   |_   _|__ ___ ___ \n|    -| -_|     | . | | .'|  _| -_| | |  _|  | . | -_|    | || .'| . |_ -|\n|__|__|___|_|_|_|  _|_|__,|___|___|___|_|    |___|___|    |_||__,|_  |___|\n                |_|                                              |___|    \n\n" + Fore.RED +"Par Η Ο Ρ Ξ#9999" + Fore.GREEN + "\n\nUsage:\n\n-o,--olTag\t[ancien tag]\n-n,--newTag\t[nouveau tag]\n-r,--replace\tremplace l'ancien tag par le nouveau\n-a,--add\tajoute un nouveau tag en plus de l'ancien et des autres\n\n" + Fore.YELLOW + "Exemple :\npython tag.py -o "+ '"euklide"' + " -n"+' "euclide" --replace' + '\n//remplacera le tag euklide par euclide\n\ntips: remplacer un ancien tag par un nouveau vide (-n "") le supprimera' + Fore.WHITE)
else:
	# Cas où les identifiants n’ont pas bien été rentrés dans le code
    if SESSION_ID == '':
        print(Fore.RED + "\n[ERREUR] "+ Fore.WHITE + "MODIFIEZ L'ID DE SESSION DANS LE PROGRAMME SVP")
    if USERAGENT == '':
        print(Fore.RED + "\n[ERREUR] "+ Fore.WHITE + "MODIFIEZ LE USERAGENT DANS LE PROGRAMME SVP")
    try: # Parse l’ancien tag à remplacer
        oldtag = sys.argv[sys.argv.index("-o") + 1]
    except: # Exception probable : -o non trouvé
        try: # Recherche alors avec l’option complète
            oldtag = sys.argv[sys.argv.index("--oldTag") + 1]
        except: # Exception --oldTag non trouvé, erreur
            print(Fore.RED + "\n[ERREUR] "+ Fore.WHITE + "Veuillez entrer l'ancien tag : -o,--oldTag")
    try: # Parse le nouveau tag
        newtag = sys.argv[sys.argv.index("-n") + 1]
    except: # Exception probable : -n non trouvé
        try: # Recherche alors avec l’option complète
            newtag = sys.argv[sys.argv.index("--newTag") + 1]
        except: # Exception --newTag non trouvé, erreur
            print(Fore.RED + "\n[ERREUR] "+ Fore.WHITE + "Veuillez entrer le nouveau tag : -n,--newTag")
    try: # Recherche de la méthode
        if sys.argv.index("-a") != -1:
            methode = 1
    except: # Si -a non trouvé
        try:
            if sys.argv.index("--add") != -1:
                methode = 1
        except: # Si -add non trouvé
            try: 
                if sys.argv.index("-r") != -1:
                    methode = 2
            except: # Si -r non trouvé
                try:
                    if sys.argv.index("--replace") != -1:
                        methode = 2
                except: # Si --replace non trouvé, rien de valide n’a donc été trouvé, erreur
                    print(Fore.RED + "\n[ERREUR] "+ Fore.WHITE + "Veuillez entrer une méthode : --add,--replace")
	# Vérification qu’il n’y a pas de paramètres oubliés pour commencer le remplacement
	# Vérification aussi que les paramètres à rentrer dans le code (SESSION_ID) sont bien entrés
    if methode != None and newtag != None and oldtag != None and SESSION_ID != '':
        titlesList,PageList = finddallpageswithtag(oldtag) # Recherche de toutes les pages où il y a l’ancien tag pour agir dessus
        print(Fore.BLUE + "\n[!]" + Fore.YELLOW + " Remplacement en cours..." + Fore.BLUE + " [!]\n" + Fore.WHITE)
        if methode == 1: # On ne fait qu’ajouter les nouveaux tags sans enlever l’ancien
            for i in range(len(PageList)): # Pour toutes les pages
                try:
                    addtag(newtag,PageList[i]) # Ajoute le nouveau tag
                    print(titlesList[i] + Fore.GREEN + " [OK]" + Fore.WHITE)
                except: # S’il y a une erreur (potentiellement récupération de la page web échouée)
                    print(titlesList[i] + Fore.RED + " [ERROR] " + PageList[i] + Fore.WHITE)
        elif methode == 2: # Remplace les tags
            for i in range(len(PageList)): # Pour toutes les pages
                try:
                    replacetag(newtag,oldtag,PageList[i]) # Remplace le tag
                    print(titlesList[i] + Fore.GREEN + " [OK]" + Fore.WHITE)
                except: # S’il y a une erreur (potentiellement récupération de la page web échouée)
                    print(titlesList[i] + Fore.RED + " [ERROR] " + PageList[i] + Fore.WHITE)
