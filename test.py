feb_seq = [1,2]

for i in range(2, 8):
    list_of_sequeance = feb_seq[i-1 ]+ feb_seq[i-2]
    feb_seq.append(list_of_sequeance)

print(feb_seq)
    