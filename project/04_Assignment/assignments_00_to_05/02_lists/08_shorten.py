MAX_LENGTH :int = 3
def shorten (lst):
    while len(lst) > MAX_LENGTH:
        last_elem = lst.pop()
        print(last_elem)

def get_lst():
    lst = []
    elem = input("Enter a value: ")
    while elem!= "":
        lst.append(elem)
        elem = input("Enter a value: ")
    return lst

def main():
    lst = get_lst()
    shorten(lst)
if __name__ == '__main__':
    main()
