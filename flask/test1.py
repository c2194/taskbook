def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Arguments:", args)
        print("Keyword Arguments:", kwargs)
        func(*args, **kwargs)
    return wrapper

@my_decorator
def my_function(name, age, **kwargs):
    print("Name:", name)
    print("Age:", age)
    print("Other Info:", kwargs)

my_function("John", 25, occupation="Engineer", location="New York")