import matplotlib.pyplot as plt
import os

for r in range(1, 10):
	os.system("java -jar negsel2.jar -self english.train -n 10 -r {} -c -l < english.test > english.results.{}".format(r, r))
	os.system("java -jar negsel2.jar -self english.train -n 10 -r {} -c -l < tagalog.test > tagalog.results.{}".format(r, r))

	with open("english.results.{}".format(r)) as f:
		e_data = f.read()

	with open("tagalog.results.{}".format(r)) as f:
		t_data = f.read()

	e_scores = [int(2**float(s)) for s in e_data.split(' \n') if s]
	t_scores = [int(2**float(s)) for s in t_data.split(' \n') if s]

	tprs, fprs = [0], [0]
	for threshold in sorted(list(set(e_scores + t_scores)))[::-1]:
		tprs += [len([score for score in t_scores if score >= threshold]) / len(t_scores)]
		fprs += [len([score for score in e_scores if score >= threshold]) / len(e_scores)]

	area = sum([(fprs[i]-fprs[i-1]) * (tprs[i-1]+tprs[i])/2 for i in range(1, len(tprs))])
	print("For n=10 and r={}, the area under the ROC curve is: {}".format(r, round(area, 3)))

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_title("ROC curves")
	ax.set_xlabel('False positive rate')
	ax.set_ylabel('True positive rate')

	roc = plt.plot(fprs, tprs, label="Negative selection with n=10, r={}".format(r))
	avg = plt.plot([0, 1], [0, 1], label="Useless model")

	ax.legend(loc=4)
	plt.savefig("ROC_{}.png".format(r))
	#plt.show()
	plt.close(fig)

#Output:
#For n=10 and r=1, the area under the ROC curve is: 0.544
#For n=10 and r=2, the area under the ROC curve is: 0.74
#For n=10 and r=3, the area under the ROC curve is: 0.831
#For n=10 and r=4, the area under the ROC curve is: 0.792
#For n=10 and r=5, the area under the ROC curve is: 0.728
#For n=10 and r=6, the area under the ROC curve is: 0.668
#For n=10 and r=7, the area under the ROC curve is: 0.591
#For n=10 and r=8, the area under the ROC curve is: 0.52
#For n=10 and r=9, the area under the ROC curve is: 0.512