from tabulate import tabulate as tb
import pickle
from coords import Coords
from coords import Rcc
import os
import sys

your_location="80.2707, 13.082"
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# importing dictionary and list already extracted from pandas - To reduce startup time
with open(resource_path('DB/mainDB'), 'rb') as file:
    mainDB = pickle.load(file)
with open(resource_path('DB/gl'), 'rb') as file:
    gl = pickle.load(file)
with open(resource_path('DB/hd'), 'rb') as file:
    hd = pickle.load(file)
with open(resource_path('DB/hip'), 'rb') as file:
    hip = pickle.load(file)
with open(resource_path('DB/hr'), 'rb') as file:
    hr = pickle.load(file)
with open(resource_path('DB/lum_sch'), 'rb') as file:
    lum_sch = pickle.load(file)
with open(resource_path('DB/mag_sch'), 'rb') as file:
    mag_sch = pickle.load(file)
with open(resource_path('DB/names'), 'rb') as file:
    names = pickle.load(file)
with open(resource_path('DB/dist_sch'), 'rb') as file:
    dist_sch = pickle.load(file)
with open(resource_path('DB/constals'), 'rb') as file:
    constals = pickle.load(file)
with open(resource_path('DB/const_stars'), 'rb') as file:
    const_stars = pickle.load(file)
# ------------
msg = """
Welcome to celestial catalogue
        0:Search through catalogue of 119614 stars
        1:Find stars visible now at Chennai
        2:Search through constellations 
        3:Constellations available right now
choose using number:
    exit - Exit
"""
list_columns = ['id', 'dist', 'mag', 'lum', 'spect']
while True:
    print(msg)
    user_in = input('>>>')
    if user_in == 'exit':
        exit()
    user_in = int(user_in)
    os.system('cls')
    if user_in == 0:  # catalogue
        # selection of catalogues
        print("""
Choose a catalog:
0:Henry Draper catalogue
1:Hertz sprung catalogue
2:Gliese catalogue
3:Hipparcos catalogue
4:Stars with verbal names - 332 stars
5:All in one - 119614 stars
want suggestion? 4 or 5 should be fun!!

""")
        user_in = input('>>>')
        os.system('cls')
        if len(user_in) == 0:
            continue

        user_in = int(user_in)
        # selecting catalogue according usr given number and store in var data
        if user_in == 5:  # 5th option have special representation due to structure of program
            data = dict(zip(mainDB.keys(), mainDB.keys()))
        else:
            data = [hd, hr, gl, hip, names][user_in]
        # -------------------------------------------------
        while True:  # The catalogue
            # searching
            srch_keywrd = input('Give me a keyword to search:\ncmds:\n\tback - to go back\n>>>').lower()
            os.system('cls')
            if srch_keywrd == 'back':
                break
            srch_rslt = [x for x in data.keys() if srch_keywrd in str(x)]  # the actuall search
            if len(srch_rslt) == 0:
                print('no match found!!! Try another?')
                continue
            elif len(srch_rslt) == 1:  # just automatically printing if only one match is found
                srch_no = 0
            else:
                # since multiple match found,asking user to select one
                n = 0
                for i in srch_rslt:
                    print(f'{n}:{i}')
                    n += 1
                print('multiple matches!!! [@_@] help me!!')
                srch_no = input('>>>')
                os.system('cls')

                if len(srch_no) == 0:
                    continue
            ID = data[srch_rslt[int(srch_no)]]
            rslt = [[mainDB[ID][j] for j in list_columns]]  # getting info about star from database - mainDB
            print(tb(rslt, headers=list_columns))  # just a pretty-print
    elif user_in == 1:
        # Visible stars
        Me = Coords(*[float(x) for x in your_location.split(",")])  # coordinates of chennai
        Me.x = 360 - (Rcc().x - Me.x)  # adventure finding us w.r.t. celestial coordinates
        Me.hrs()  # degree to hours conversion (eg: 360 --> 24 )
        visible_stars = []

        # # Locating stars in visible direction
        for i, j in zip(mainDB.keys(), mainDB.values()):
            star = Coords(j['ra'], j['dec'], Deg=False)
            _, ang = Me.is_visible(star)  # checking if star is visible direction. ang is a tuple
            if _:  # _ is True if star is in visible direction, False otherwise
                ang = f"{str(round(ang[0], 1))}\'W  {str(round(ang[1], 1))}\'N"
                # tuple is converted into better string representation
                visible_stars.append((i, ang))
        print('Number of stars visivle RN:', len(visible_stars))

        rslt = []
        # # collecting information about stars from database
        for i in visible_stars:
            a = [mainDB[i[0]][j] for j in list_columns]
            rslt.append(a + [i[1]])

        # # presenting result to user
        i = 20
        flag = True
        while i < len(rslt):
            os.system('cls')
            if flag:
                rslt = [[x] + rslt[x] for x in range(len(rslt))]
            flag = True
            lst = rslt[i - 20:i]
            print(len(rslt), 'Stars are visible')
            print(tb(lst, headers=['ln no.'] + list_columns + ['Angle from Zeneth']))
            u_in = input(
                '<enter> for nxt 20 stars \n type dist/mag/lum to sort this list\ncmds:\n\tback - to exit\nenter ln ' 
                'no. to jump>>>')
            if u_in.isdigit():  # jumps to specified number line (if exists)
                i = int(u_in)
            elif u_in == 'back':
                break

            elif u_in in ['mag', "dist", 'lum']:
                d = {"dist": 1, 'mag': 2, 'lum': 3}
                for j in range(len(rslt)):
                    del rslt[j][0]
                rslt.sort(key=lambda x: x[d[u_in]])
                continue
            flag = False  # this solves the prob of adding extra no.line column due to line 115
            i += 20
    elif user_in == 2:
        # constellation catalogue
        msg1 = 'Search up constellations here\ncmds:\n\tshow - show all constellations\n\tback - exit'
        while True:
            print(msg1)
            user_in = input('>>>').lower()
            os.system('cls')
            name_list = list(constals.keys())
            if user_in == 'back':
                print('bu-byee!!!')
                break
            elif user_in == 'show':  # just prints name of all stars
                ls = []
                r = 6
                for i in range(0, len(name_list), r):  # creating a list to fold all names into r number of columns
                    ls.append(name_list[i:i + r])
                print(tb(ls))
                msg1 = 'Search now?\n\ncmds:\n\tshow - show all constellations\n\tback - exit'
                continue
            rslt = [i for i in name_list if user_in in i.lower()]  # searching for matches
            if len(rslt) == 0:
                msg1 = 'no match! :(\nPls check spelling and try again\n\ncmds:\n' \
                       '\tshow - show all constellations\n\tback - exit'
                continue
            elif len(rslt) == 1:
                no = 0  # automatically selects the only available search result
            else:
                print('multiple matches!!! [@_@] help me!!\n')
                for i in range(len(rslt)):
                    print(f'{i}:{rslt[i]}')
                print('\nresult is of the form:\n   N:<name>')
                while True:
                    no = int(input('Choose with N: '))
                    if no >= len(rslt):
                        print('incorrect value!!\n\n')
                        continue
                    break
            print('\n\n')
            out = [list(constals[name_list[0]].keys()), constals[rslt[no]].values()]  # fetching info from database
            print(tb(out, headers="firstrow"))
            print('\n' + '-' * 20)
            msg1 = 'Search nxt one?\ncmds:\n show - show all constellations\n bye - exit'
    elif user_in == 3:
        # # visible constellations

        list_columns = ['id', 'dist', 'mag', 'lum', 'spect']
        #  adventure finding us w.r.t. celestial coordinates
        Me = Coords(*[float(x) for x in your_location.split(",")])
        Me.x = 360 - (Rcc().x - Me.x)
        Me.hrs()

        visible_stars = []
        # # collecting all stars that is visible right now
        for i, j in zip(mainDB.keys(), mainDB.values()):
            star = Coords(j['ra'], j['dec'], Deg=False)
            _, ang = Me.is_visible(star)
            if _:
                ang = f"{str(round(ang[0], 1))}\'W  {str(round(ang[1], 1))}\'N"
                visible_stars.append((i, ang))
        rslt = []
        # # filtering the brightest star of the constellation and renaming with their constellation
        for i in visible_stars:
            if mainDB[i[0]]['id'] in const_stars:
                star_name = const_stars[mainDB[i[0]]['id']]
                for j in constals.values():
                    if j['Brightest star'] == star_name:
                        rslt.append([j['Name'], mainDB[i[0]]['dist'], mainDB[i[0]]['mag'], i[1]])
        if rslt == 0:
            print('Seems pretty-much nothing, come back later!!')
        os.system('cls')
        print(tb(rslt, headers=['Name', 'Distance', 'Mag', 'Ang from Zeneth']))  # yet another pretty-print
        print("-" * 45)
        print(len(rslt), 'constellations are visible right now')
        input('enter to continue')
        os.system('cls')
