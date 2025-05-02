class A:
    def show(self):
        print("A.show()")

class B(A):
    def show(self):
        print("B.show()")
        
class C(A):
    def show(self):
        print("C.show()")

class D(B , C):
    pass

d= D()
d.show()
print(D.__mro__)