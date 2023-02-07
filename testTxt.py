FILE_DIR = "F:/test/05_02_2023 13_04_23/"
WINNER_FILE = FILE_DIR + "winners.txt"
f = open(WINNER_FILE, "r")
text = f.read().split("\n")
while "" in text:
    text.remove("")
print(text)
