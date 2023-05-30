import numpy as np

class PascalTriangle:
        def __init__(self, size=10, degree=2):
            self.degree=degree
            self.size = size
            self.v = [np.zeros((n+1,n+1),float) for n in range(size)]
            self.coefs = [np.ones((degree, n+1, n+1), float) for n in range(size-1)]

        def construct(self, v0):
            v=self.v

            v[0][0,0] = v0
            for n1 in range(self.size - 1):
                n = n1 + 1

                for i in range(n):
                    for j in range(n):
                        if (j+i>=n): continue
                        v[n][i,j] = i+j

        def print(self):
            v = self.v

            for n in range(self.size):
                for i in range(n):
                    for j in range(n):
                        if (j + i >= n): continue
                        print(v[n][i,j], end=" ")
                    print()
                print("----")

def main():
    t = PascalTriangle(degree=3)
    t.construct(1)
    t.print()

if __name__=="__main__":
    main()


