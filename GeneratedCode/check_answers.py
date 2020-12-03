
total = 0
correct = 0

with open("myOutput1") as f1, open("answers") as f2:
    for l1, l2 in zip(f1, f2):
        v1 = float(l1.split()[1])
        v2 = float(l2.split()[1])
        if abs(v1 - v2) < 1E-5:
            correct+=1
        else:
            print(l1, l2)
        total+=1

print(f"Percentage of correct answers: {correct/total*100}%")
