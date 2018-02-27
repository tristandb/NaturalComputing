import matplotlib.pyplot as plt
import os

for lang in ['hiligaynon', 'middle-english', 'plautdietsch', 'xhosa']:
	for r in range(1, 10):
		os.system("java -jar negsel2.jar -self english.train -n 10 -r {} -c -l < english.test > english.results.{}".format(r, r))
		os.system("java -jar negsel2.jar -self english.train -n 10 -r {} -c -l < lang/{}.txt > {}.results.{}".format(r, lang, lang, r))

		with open("english.results.{}".format(r)) as f:
			e_data = f.read()

		with open("{}.results.{}".format(lang, r)) as f:
			l_data = f.read()

		e_scores = [int(2**float(s)) for s in e_data.split(' \n') if s]
		l_scores = [int(2**float(s)) for s in l_data.split(' \n') if s]

		tprs, fprs = [0], [0]
		for threshold in sorted(list(set(e_scores + l_scores)))[::-1]:
			tprs += [len([score for score in l_scores if score >= threshold]) / len(l_scores)]
			fprs += [len([score for score in e_scores if score >= threshold]) / len(e_scores)]

		area = sum([(fprs[i]-fprs[i-1]) * (tprs[i-1]+tprs[i])/2 for i in range(1, len(tprs))])
		print("For lang={}, n=10 and r={}, the area under the ROC curve is: {}".format(lang, r, round(area, 3)))

		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_title("ROC curves")
		ax.set_xlabel('False positive rate')
		ax.set_ylabel('True positive rate')

		roc = plt.plot(fprs, tprs, label="Negative selection with n=10, r={}".format(r))
		avg = plt.plot([0, 1], [0, 1], label="Useless model")

		ax.legend(loc=4)
		plt.savefig("ROC_{}_{}.png".format(lang, r))
		#plt.show()
		plt.close(fig)
