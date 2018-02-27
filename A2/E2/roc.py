from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np

name = 'snd-unm'
number = 3

test_file_name = 'syscalls/{}/10/scores/{}.{}.{}.scores'
labels_file_name = 'syscalls/{}/{}.{}.labels'

false_positive_rate = dict()
true_positive_rate = dict()
roc_auc = dict()

for i in range(1, 10):
	with open(test_file_name.format(name, name, number, i), 'r') as test_file, open(labels_file_name.format(name, name, number), 'r') as labels_file:
		labels = np.array(labels_file.read().splitlines()).astype(np.float)
		prediction = np.array(test_file.read().splitlines()).astype(np.float)
		prediction = prediction / float(max(prediction))

		false_positive_rate[i], true_positive_rate[i], _ = roc_curve(labels, prediction)
		roc_auc[i] = auc(false_positive_rate[i], true_positive_rate[i])

plt.figure()
for i in range(1, 10):
	plt.plot(false_positive_rate[i], true_positive_rate[i], lw=2, label='ROC r={} (area = {:0.2f})'.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve for {}-{}'.format(name, number))
plt.legend(loc="lower right")
plt.savefig('{}.{}.png'.format(name,number))

