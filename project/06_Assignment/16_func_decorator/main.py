def log_function_call(func):
    def wrapper():
        print("Function is being caleed")
        return func()
    return wrapper

@log_function_call
def say_hello():
    print("Hello!")
    
say_hello()