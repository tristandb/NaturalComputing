from scipy.special import binom as binom
import numpy as np
import matplotlib.pyplot as plt

@np.vectorize
def S(c, p):
  return 1 - sum([binom(int(c), i) * p**i * (1-p)**(int(c)-i) for i in range(int(c)//2+1)])

competence = np.linspace(0, 1, 100)
jury_size = np.linspace(0, 100, 100)
competence, jury_size = np.meshgrid(competence, jury_size)

probability = S(jury_size, competence)

plt.pcolormesh(jury_size, competence, probability)
plt.colorbar()
ax = plt.gca()
ax.set_xlim(1, 100)
plt.title('Probability of a correct decision for various sizes of the jury')
plt.xlabel('Jury size')
plt.ylabel('Competence level')
plt.savefig('competence_jury.png')
plt.show()

plt.clf()
plt.plot(np.linspace(0, 1, 100), probability[1, :])
plt.xlabel('Jury Size')
plt.ylabel('Probability of making a Correct Decision')
plt.title('Probability of making a Correct Decision versus Jury Size')
plt.savefig('competence_single.png')
plt.show()