# Fill out the function get_first_element(lst) which takes in a list lst as a parameter and prints the first element in the list. The list is guaranteed to be non-empty. We've written some code for you which prompts the user to input the list one element at a time.
def get_first_element(lst):
    """Print the first elemts of a provided list"""
    print(lst[0])

def get_lst():
    """
    prompts the user to enter on elemnt of the list ata  atime return teh first resulting list
    """
    lst = []
    elem:str= input("Enter an elemet sof the list and press the enter: ")
    while elem != "":
        lst.append(elem)
        elem = input("Please enter an element o f teh list and press enter to stop")
    return lst

def main():
    lst = get_lst()
    get_first_element(lst)

if __name__ == '__main__':
    main()



