def sum(a, b):
    a += b
    print(a)
    return a


class ConsumeSum:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def sum(self):
        a = sum(self.a, self.b)
        print(a)

if __name__ == "__main__":
    c = ConsumeSum(2,3)
    c.sum()

