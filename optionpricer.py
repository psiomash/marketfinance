
# OUTIL DE PRICING D'OPTION - NOMENCLATURE

# C = la valeur de l'option Call
# P = la valeur de l'option Put
# K = le strike price
# r = le taux sans risque
# t = le temps restant jusqu'à la date d'exercice de l'option (en année)
# N = loi normale centrée réduite N(0,1)
# o = sigma, volatilité du sous-jacent
# d = rendement des dividendes

# FORMULE POUR L'EVALUATION D'UNE OPTION CALL

# C = S*N(d1) - K*exp(-rt)*N(d2)
# d1 = [ln(S/K) + (r - d + (o**2/2)) * t] / [o * sqrt(t)]
# d2 = d1 - (o * sqrt(t))

# FORMULE POUR L'EVALUATION D'UNE OPTION PUT

# P = -S*N(-d1) + K*exp(-rt)*N(d2)
# d1 = [ln(S/K) + (r - d + (o**2/2)) * t] / [o * sqrt(t)]
# d2 = d1 - (o * sqrt(t))

from pymathematics import sqrt, ln, exp
from scipy import stats
from cmath import pi

is_Call = True
s = 45          # cours du sous-jacent
k = 40          # strike price
r = 0.03        # risk-free rate
t = 1           # en fraction d'année
o = 0.68        # volatilité implicite sous-jacente
q = 0.05        # taux de dividende

# 1) Input est-ce que c'est un call ou un put (formule différente)
# 2) Indiquer ce que l'on cherche à calculer (price, vega, teta, gamma, delta etc...)
# 3) Mettre les informations nécessaire pour le calcul de ces informations
# 4) Indication du résultat
# 5) Potentiellement mettre un graphique

# --> définir toutes les formules de calcul

# stats.norm.cdf() => fonction de répartition de la loi normale centrée réduite
# stats.norm.pdf() => fonction de densité de la loi normale centrée réduite

def d1(s, k, r, q, o, t):
    d1 = (ln(s / k) + (r - q + (0.5 * (o ** 2))) * t) / (o * sqrt(t))
    return d1

def d2(d1, o, t):
    d2 = d1 - (o * sqrt(t))
    return d2

def price(d1, d2, s, k, r, q, t):
    if is_Call == True:
        cdf_d1 = stats.norm.cdf(d1)
        cdf_d2 = stats.norm.cdf(d2)
        price = s*exp(-q*t)*cdf_d1-k*exp(-r*t)*cdf_d2
    else:
        d1 = -d1
        cdf_d1 = stats.norm.cdf(d1)
        d2 = -d2
        cdf_d2 = stats.norm.cdf(d2)
        price = k*exp(-r*t)*cdf_d2-s*exp(-q*t)*cdf_d1
    return round(price,3)

def delta(d1, q, t):
    cdf_d1 = stats.norm.cdf(d1)
    if is_Call == True:
        delta = exp(-q*t)*cdf_d1
    else:
        delta = exp(-q*t)*(cdf_d1-1)
    return round(delta, 3)

def vega(d1, s, q, t):
    pdf_d1 = stats.norm.pdf(d1)/100
    vega = s*exp(-q*t)*pdf_d1*sqrt(t)
    return round(vega,3)

def rho(d2, k, t, r):
    if is_Call == True:
        cdf_d2 = stats.norm.cdf(d2)/100
        rho = k*t*exp(-r*t)*cdf_d2
    else:
        d2 = -d2
        cdf_d2 = stats.norm.cdf(d2)/100
        rho = -k*t*exp(-r*t)*cdf_d2
    return round(rho,3)

def gamma(d1, q, t, s, o):
    pdf_d1 = stats.norm.pdf(d1)
    gamma = (pdf_d1*exp(-q*t))/(s*o*sqrt(t))
    return round(gamma,3)

def theta(d1, d2, s, o, t, r, k, q):
    if is_Call == True:
        pdf_d1 = stats.norm.cdf(d1)/100
        cdf_d1 = stats.norm.pdf(d1)/100
        cdf_d2 = stats.norm.pdf(d2)/100
        theta = -((s*exp(-q*t)*pdf_d1*o)/(2*sqrt(t)))-r*k*exp(-r*t)*cdf_d2+q*s*exp(-q*t)*cdf_d1
    return theta


def theta(d1, d2, s, k, r, q, o, t):
    if is_Call == True:
        pdf_d1 = stats.norm.pdf(d1)
        cdf_d1 = stats.norm.cdf(d1)
        cdf_d2 = stats.norm.cdf(d2)
        theta = (- (s * pdf_d1 * o * exp(-q * t)) / (2 * sqrt(t))
                 - r * k * exp(-r * t) * cdf_d2
                 + q * s * exp(-q * t) * cdf_d1)
    else:
        d1 = -d1
        d2 = -d2
        pdf_d1 = stats.norm.pdf(d1)
        cdf_d1 = stats.norm.cdf(d1)
        cdf_d2 = stats.norm.cdf(d2)
        theta = (- (s * pdf_d1 * o * exp(-q * t)) / (2 * sqrt(t))
                 + r * k * exp(-r * t) * cdf_d2
                 - q * s * exp(-q * t) * cdf_d1)
    return round(theta / 365, 3)

d1 = d1(s, k, r, q, o, t)
d2 = d2(d1, o, t)

price = price(d1, d2, s, k, r, q, t)
delta = delta(d1, q, t)
vega = vega(d1, s, q, t)
rho = rho(d2, k, t, r)
gamma = gamma(d1, q, t, s, o)
theta = theta(d1, d2, s, k, r, q, o, t)

print(f"Prix : {price}")
print(f"Delta : {delta}")
print(f"Vega : {vega}")
print(f"Rho : {rho}")
print(f"Gamma : {gamma}")
print(f"Theta : {theta}")
