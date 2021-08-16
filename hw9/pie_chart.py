# Author: Cheryl Dugas

#  Pie chart plot

import matplotlib.pyplot as plt

OSN_names = [ 'SnapChat', 'FB', 'Instagram', 'LinkedIn', 'YouTube', 'Reddit', 'Twitter' ]

OSN_numbers = [ 23, 23, 21, 12, 11, 11, 10 ]


plt.pie(OSN_numbers, labels=OSN_names)
plt.title('CS581 Social Media Use')

plt.show()
plt.savefig(fname="./test,png")

x=3