import matplotlib.pyplot as plt

with open('english_results') as f:
	e_data = f.read()

with open('tagalog_results') as f:
	t_data = f.read()

e_scores = [int(2**float(s)) for s in e_data.split(' \n') if s]
t_scores = [int(2**float(s)) for s in t_data.split(' \n') if s]

#For each meaningful treshold (i.e. each anomaly score in the list), compute
#true positive rate (fpr) = true positives / all positives
#false positive rate (tpr) = false positives / all negatives
#Then plot the point (fpr, tpr)

tprs, fprs = [], []
for threshold in sorted(list(set(e_scores + t_scores)))[::-1]:
	tprs += [len([score for score in t_scores if score >= threshold]) / len(t_scores)]
	fprs += [len([score for score in e_scores if score >= threshold]) / len(e_scores)]

area = 0
for i in range(1, len(tprs)):
	area += (fprs[i]-fprs[i-1]) * tprs[i-1]
print("Area: {}".format(area))

plt.plot(fprs, tprs)
plt.plot([0, 1], [0, 1])

plt.show()