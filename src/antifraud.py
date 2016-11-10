import time
import sys

from collections import defaultdict

class PayMo:
  """ 
   PayMo
   Contains the method and attribute to process the batch input and the stream input.
  """ 
  def __init__(self):
    # Use for staging the 1st and 2nd degree of connections
    self.d1 = defaultdict(set)
    self.d2 = defaultdict(set)

  def parse_trans(self, list_of_tuple):
    """
    parse all input tuple and store the 1st degree of connections

        :type List[tuple(int)]
        :rtype: None
    """
    for k, v in list_of_tuple:
      self.d1[k].add(v)
      self.d1[v].add(k)

  def get_second_degree_connection(self, n):
    """
    parse all input tuple and store the 1st degree of connections

        :type int - id n
        :rtype: Set of 2nd degree of connections for input id n
    """
    if self.d2[n]:
      return self.d2[n]

    s = set()
    for i in self.d1[n]:
      if n != i:
        s.add(i)
        for j in self.d1[i]:
          s.add(j)

    if n in s:
      s.remove(n)
    self.d2[n] = s
    return s

  def verify_transaction_first_degree(self, a, b):
    """
    Return whether a and b is first degree connected

        :type int - a, b
        :rtype: boolean
    """
    return b in self.d1[a]

  def verify_transaction_second_degree(self, a, b):
    """
    Return whether a and b is second degree connected

        :type int - a, b
        :rtype: boolean
    """
    if self.verify_transaction_first_degree(a, b):
      return True
    return bool(self.d1[a] & self.d1[b])

  def verify_transaction_forth_degree(self, a, b):
    """
    Return whether a and b is forth degree connected

        :type int - a, b
        :rtype: boolean
    """
    if self.verify_transaction_second_degree(a, b):
      return True
    else:
      s1 = self.get_second_degree_connection(a)
      s2 = self.get_second_degree_connection(b)
      return b in s1 or a in s2 or bool(s1 & s2)

if __name__ == '__main__':

    if len(sys.argv) != 6:
     print "Argument: sys.argv"

    batch_input_file = sys.argv[1]
    stream_input_file = sys.argv[2]
    first_file = sys.argv[3]
    second_file = sys.argv[4]
    forth_file = sys.argv[5]

    list_of_connections = []
    f = open(batch_input_file, 'r')
    first_line = f.readline()
    for line in f:
      fields = line.split(',')
      list_of_connections.append((int(fields[1]), int(fields[2])))
    end = time.time()
    f.close()

    positive = 'trusted'
    negative = 'unverified'

    pm = PayMo()
    pm.parse_trans(list_of_connections)
    first_count, second_count, forth_count = 0, 0, 0

    f = open(stream_input_file, 'r')
    first_line = f.readline()

    first = open(first_file, 'w')
    second = open(second_file, 'w')
    forth = open(forth_file, 'w')

    start = time.time()

    for line in f:
      fields = line.split(',')
      x, y = int(fields[1]), int(fields[2])
      if x == y or pm.verify_transaction_first_degree(x, y):
        first_count += 1
        first.write(positive + '\n')
      else:
        first.write(negative + '\n')

      if x == y or pm.verify_transaction_second_degree(x, y):
        second_count += 1
        second.write(positive + '\n')
      else:
        second.write(negative + '\n')

      if x == y or pm.verify_transaction_forth_degree(x, y):
        forth_count += 1
        forth.write(positive + '\n')
      else:
        forth.write(negative + '\n')

    end = time.time()
    f.close()
    print 'first:%d second:%d forth:%d in %ds' % (first_count, second_count, forth_count, (end - start))
