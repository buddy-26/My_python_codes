n = 123
ulta = 0

while n > 0:
    piche_ka_ank = n % 10       # 3 nikala
    ulta = (ulta * 10) + piche_ka_ank  # 0 se 3 bana, phir 30+2=32...
    n = n // 10                 # 123 se 12 bana
    
print(ulta)