##import os.path
##
##erg = str(42)
##
##if os.path.exists("C:/Users/moses/OneDrive/power point songs/" + erg +".pptx"):
##   print("Exists")
##else:
##   print("Nay")
##
##
##"C:/Users/moses/OneDrive/power point songs/" + erg + " CONVERTED!" +".pptx"
##

Hyro = "îñïáõÙ »Ý ÑÇÙ³ »ñ·»ñ¹, "
Arm = "տրտում"
leg = "HEllo"
print(Arm.isascii())

s1 = "I enjoy coding in Pythn"
s2 = "Hello, this is Educative"

print("S1: ", s1.isascii())
print("S2: ", s2.isascii())


import re

for c in Hyro:
    if 0 <= ord(c) <= 127:
        print("this is a ascii character")
    else:
        print("this is a non-ascii character. Do something.")

