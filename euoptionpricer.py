                                                                                                                                                          
# OPTION PRICING BASED ON THE BLACK & SCHOLES FORMULA -----------------------                                                                             
                                                                                                                                                          
# Carries out Black-Scholes calculations for European options on stocks, stock indices and currencies                                                     
                                                                                                                                                          
                                                                                                                                                          
# The limits of this model --------------------------------------------------                                                                             
                                                                                                                                                          
# The model assumes that the volatility of the underlying asset is constant over time                                                                     
# The return of the underlying assets follow a normal distribution so it doesn't take into account fat tails                                              
# It assumes an absence of arbitrage in a perfect market with no opportunities of arbitrage                                                               
# There is no transaction costs or dividends paid by the underlying assets, adjustments can be made                                                       
# The model assumes that the risk-free rate remains constant over the time, not always realistic                                                          
# The underlying is considered as liquid and can be traded continiously                                                                                   
                                                                                                                                                          
# Informations to give are the following -------------------------------------                                                                            
                                                                                                                                                          
from pymathematics import sqrt, ln, exp                                                                                                                   
from scipy import stats                                                                                                                                   
                                                                                                                                                          
is_Call = False     # Put = False / Call = True                                                                                                           
s = 45              # Underlying stock price                                                                                                              
k = 40              # Strike price                                                                                                                        
r = 0.03            # Risk-free rate                                                                                                                      
t = 1               # Expiration (years)                                                                                                                  
o = 0.68            # Volatility                                                                                                                          
q = 0.05            # Dividend yield                                                                                                                      
                                                                                                                                                          
# Additionnal information ----------------------------------------------------                                                                            
                                                                                                                                                          
# stats.norm.cdf() => Distribution function of the reduced centered normal distribution                                                                   
# stats.norm.pdf() => Density function of the reduced centered normal distribution                                                                        
                                                                                                                                                          
                                                                                                                                                          
# Beginning of the code ------------------------------------------------------                                                                            
                                                                                                                                                          
                                                                                                                                                          
# First probability factor (D1)                                                                                                                           
def d1(s, k, r, q, o, t):                                                                                                                                 
    d1 = (ln(s / k) + (r - q + (0.5 * (o ** 2))) * t) / (o * sqrt(t))                                                                                     
    return d1                                                                                                                                             
                                                                                                                                                          
# Second probability factor (D2)                                                                                                                          
#                                                                                                                                                         
def d2(d1, o, t):                                                                                                                                         
    d2 = d1 - (o * sqrt(t))                                                                                                                               
    return d2                                                                                                                                             
                                                                                                                                                          
# Price of the option                                                                                                                                     
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
                                                                                                                                                          
# Delta value                                                                                                                                             
def delta(d1, q, t):                                                                                                                                      
    cdf_d1 = stats.norm.cdf(d1)                                                                                                                           
    if is_Call == True:                                                                                                                                   
        delta = exp(-q*t)*cdf_d1                                                                                                                          
    else:                                                                                                                                                 
        delta = exp(-q*t)*(cdf_d1-1)                                                                                                                      
    return round(delta, 3)                                                                                                                                
                                                                                                                                                          
# Vega value                                                                                                                                              
def vega(d1, s, q, t):                                                                                                                                    
    pdf_d1 = stats.norm.pdf(d1)/100                                                                                                                       
    vega = s*exp(-q*t)*pdf_d1*sqrt(t)                                                                                                                     
    return round(vega,3)                                                                                                                                  
                                                                                                                                                          
# Rho value                                                                                                                                               
def rho(d2, k, t, r):                                                                                                                                     
    if is_Call == True:                                                                                                                                   
        cdf_d2 = stats.norm.cdf(d2)/100                                                                                                                   
        rho = k*t*exp(-r*t)*cdf_d2                                                                                                                        
    else:                                                                                                                                                 
        d2 = -d2                                                                                                                                          
        cdf_d2 = stats.norm.cdf(d2)/100                                                                                                                   
        rho = -k*t*exp(-r*t)*cdf_d2                                                                                                                       
    return round(rho,3)                                                                                                                                   
                                                                                                                                                          
# Gamma value                                                                                                                                             
def gamma(d1, q, t, s, o):                                                                                                                                
    pdf_d1 = stats.norm.pdf(d1)                                                                                                                           
    gamma = (pdf_d1*exp(-q*t))/(s*o*sqrt(t))                                                                                                              
    return round(gamma,3)                                                                                                                                 
                                                                                                                                                          
# Theta value                                                                                                                                             
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
                                                                                                                                                          
# Vanna value                                                                                                                                             
def vanna(d1, d2, q, t, o):                                                                                                                               
    pdf_d1 = stats.norm.pdf(d1)/100                                                                                                                       
    vanna = (-exp(-q*t)*pdf_d1*d2)/o                                                                                                                      
    return round(vanna,3)                                                                                                                                 
                                                                                                                                                          
# Vonna value                                                                                                                                             
def vonna(d1, d2, s, t, q):                                                                                                                               
    pdf_d1 = stats.norm.pdf(d1)/100                                                                                                                       
    vonna = (s*sqrt(t)*exp(-q*t)*pdf_d1*d1*d2)/o                                                                                                          
    return round(vonna,3)                                                                                                                                 
                                                                                                                                                          
                                                                                                                                                          
# Function execution ---------------------------------------------------------                                                                            
                                                                                                                                                          
d1 = d1(s, k, r, q, o, t)                                                                                                                                 
d2 = d2(d1, o, t)                                                                                                                                         
                                                                                                                                                          
price = price(d1, d2, s, k, r, q, t)                                                                                                                      
delta = delta(d1, q, t)                                                                                                                                   
vega = vega(d1, s, q, t)                                                                                                                                  
rho = rho(d2, k, t, r)                                                                                                                                    
gamma = gamma(d1, q, t, s, o)                                                                                                                             
theta = theta(d1, d2, s, k, r, q, o, t)                                                                                                                   
vanna = vanna(d1, d2, q, t, o)                                                                                                                            
vonna = vonna(d1, d2, s, t, q)                                                                                                                            
                                                                                                                                                          
print(f"< Option Pricer & Values >\nPrix : {price}\n< First order values >\nDelta : {delta}\nGamma : {gamma}\n"                                           
      f"Vega : {vega}\nTheta : {theta}\nRho : {rho}\n< Second order values >\n"                                                                           
      f"Vanna : {vanna}\nVonna / Volga : {vonna}")                                                                                                        
                                                                                                                                                          
