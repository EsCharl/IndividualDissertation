# note to self you can't add a list into a set

setA = {[1],[2],[3],[4]}
setB = {[1],[2],[3],[4]}
if setA-setB:
    print("setA-setB")
setA.add([5])
if setA-setB:
    print(setA-setB)