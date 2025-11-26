"""Q51_exo.py"""



from Q51_calc_313 import Calculator
# from Q51_calc_312 import Calculator
cal = Calculator("POOC")    # nom du groupe en argument, par ex. POOZ



# --- Expression 1 : (5 * 3) + (4 * 2)
cal1 = cal.fois(5, 3)
cal2 = cal.fois(4, 2)
try:
    expr1 = cal.plus(cal1, cal2)
    print(expr1)
except :
    print("Erreur expression 1 :")



# --- Expression 2 : (24 * 18) * (3 + 4)
cal3 = cal.fois(24, 18)
cal4 = cal.plus(3, 4)
try:
    expr2 = cal.fois(cal3, cal4)
    print(expr2)
except:
    print("Multiplication par Zéro impossible :")



# --- Expression 3 : (-4 * 6) * ((6 - 3) - (2 + 1))
cal5 = cal.fois(-4, 6)
cal6 = cal.moins(6, 3)
cal7 = cal.plus(2, 1)
try:
    cal8 = cal.moins(cal6, cal7)
    expr3 = cal.fois(cal5, cal8)
    print(expr3)
except NameError:
    print("Résultat de la soustraction non valide.")
except:
    print("Multiplication par Zéro impossible :")