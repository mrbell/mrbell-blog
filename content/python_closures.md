Title: Closures in Python
Date: 2015-08-16
Tags: python
Slug: python_closures

The concept of [*closures*](https://en.wikipedia.org/wiki/Closure_\(computer_programming\)) is something that I've been 
familiar with for a while, but I haven't used in my own work until recently. I started thinking more about closures while reading 
[A Software Engineer Learns HTML5, JavaScript and jQuery](http://www.amazon.com/Software-Engineer-Learns-JavaScript-jQuery-ebook/dp/B00GAMTRI8) 
by Dane Cameron (an excellent book, btw). They are introduced in the book as a way to protect object members. 
In JS, like in Python, members of an object are public. In the absence of a *private* keyword or the like, one can use 
closures to protect state variables from tampering by external code. Here's an example:

    :::javascript
    function incrementer() {
        var i=0;
        return function() {return ++i;}
    }
    
    f = incrementer()
    f() -> 1
    f() -> 2
    f() -> 3
    ...
 
What has happened here is that the function returned by `incrementer` has "closed" over `i`. `i` is declared in the scope 
of `incrementer` but is accessible within `function`. Since `function` refers to `i`, the variable gets carried around 
by `function` *even after `incrementer` has returned.* 

The utility of this pattern is that `i` can be modifed (incremented) by calling `f`, the function returned by `incrementer`, but 
it can't be accessed directly in any other way. 
 
I hadn't seen closures mentioned often in Python circles, at least not in scientific and data analysis contexts. But as I 
learned about closures in JS I couldn't help but wonder how they operate in Python, my language of choice. So does this 
same code pattern work in Python?

    :::python
    def incrementer():
        i = 0
        def function():
            i += 1
            return i
        return function
    
    >> f = incrementer()
    
    >> f()
    
    ---------------------------------------------------------------------------
    UnboundLocalError                         Traceback (most recent call last)
    <ipython-input-6-0ec059b9bfe1> in <module>()
    ----> 1 f()
    
    <ipython-input-5-fe458f37d60a> in function()
          2     i = 0
          3     def function():
    ----> 4         i += 1
          5         return i
          6     return function
    
    UnboundLocalError: local variable 'i' referenced before assignment

Nope. We get an `UnboundLocalError`. What if we just refer to `i` rather than try to increment it's value?

    :::python
    def incrementer():
        i = 120
        def function():
            return i
        return function
    
    >> f = incrementer()
    
    >> f()
     
    120

That works fine. Well, `incrementer` no longer increments anything, but at least the code executes without error. So what 
happened here? In Python, you can access a variable from a parent scope, but you can't overwrite it. Assignment in Python is
done within the local scope, even if a variable with the same name is declared in a parent 
scope. The parent variable is not overridden, but instead a new variable is created in the nested scope. 
Take the following code for example:

    :::python
    def incrementer():
        i = 120
        def function():
            i = 10
            return i
        return function
    
    >> f = incrementer()
    >> f()
    10

The `i` declared in `function` is local to the nested function and "shadows" the `i` declared in `incrementer`.  

Although we can't overwrite a variable in a parent scope, we can modify its contents *if the object is a 
mutable type* like a list or an object. So to replicate the JS style closure in Python, one could close over a
mutable object, e.g.

    def get_incrementer():
        i = [0]
        def function():
            i[0] += 1
            return i[0]
        return function
    
    >> f = get_incrementer()
    >> f()
    1
    >> f()
    2
    >> f()
    3

Let's say that instead of using the pattern given above, we defined `incrementer` to be a method of a class and used it 
to increment a normal class attribute.

    :::python
    class MyClass(object):
        def __init__(self):
            self._i = 0
        def incrementer(self):
            self._i += 1
            return self._i
            
    >> test = MyClass()
    >> test.incrementer() 
    1
    >> test.incrementer()
    2
    >> test._i = 100
    >> test.incrementer()
    101

This works, but of course one can always just modify `test._i`, so subsequent calls to incrementer might not always 
behave as expected. 

So closures can be used to protect a variable. I don't think I've come across anyone that does this in practice, and I've 
seen some discussion that it might not be a good idea, but I don't really understand why. 

A much more common use case for closures in Python, and one that I now make use of myself, is 
[*function decoration*](https://www.python.org/dev/peps/pep-0318/). Function decorators 
are a powerful concept that allow you to modify a function's behavior without changing its implementation. 

For example, let's say you're writing an application and decide you want to log every call to a set of functions. 
You could implement your functions to have logging statements sprinkled throughout, mixing logging code together with
the rest of your code. But this makes for code that is hard to read and maintain. 

Instead, you can use a function decorator to handle the logging for you keeping the logging features separate from your 
application code. This is called [*separation of concerns*](https://en.wikipedia.org/wiki/Separation_of_concerns) and is 
central to a programming paradigm known as [*aspect oriented programming*](https://en.wikipedia.org/wiki/Aspect-oriented_programming). 

Let's write a logging decorator that logs the name of the function call, the arguments passed to the function, and 
the return value.
 
    :::python
    def log_me(func):
        def function_wrapper(*args, **kwargs):
            print 'Calling function {:}'.format(func.func_name)
            args_list = ' '.join([str(a) for a in args])
            print 'Positional arguments: {:}'.format(args_list)
            print 'Keyword arguments: {:}'.format(kwargs)
            
            # Call the original function
            result = func(*args, **kwargs)
            
            print 'Return: {:}'.format(result)
        return function_wrapper
        
`log_me` takes a function as an argument and returns a function (a decorator must return a function). The function that 
we return, defined within the scope of `log_me` is called `function_wrapper` and it closes over the argument `func`. 
`function_wrapper` takes in a set of arguments, logs them, calls the decorated function `func`, and finally
logs the result. 

**A side note** I know I'm not really "logging" here, per se, but just printing to standard output. In principle one should 
use the [logging module](https://docs.python.org/2/library/logging.html) or something similar.

To *use* `log_me` we can use the Python decorator syntax (which you're familiar with if you've used e.g. [flask](http://flask.pocoo.org/) 
or many other popular Python packages that use decorators):
    
    @log_me
    def adder(a, b, **kwargs):
        return a + b
        
    @log_me
    def multiplier(a, b, **kwargs):
        return a * b
        
Here I've defined two simple functions and decorated them with `log_me`. Equivalently I could have just done:
    
    def multiplier(a, b, **kwargs):
        return a * b
    multiplier = log_me(multiplier)

Anyway, the result is that when I call either of these two functions, their inputs and outputs get logged.
       
    >> adder(1,2, another='argument')
    Calling function adder
    Positional arguments: 1 2
    Keyword arguments: {'another': 'argument'}
    Return: 3
    
    >> multiplier(3, 4, another='argument')
    Calling function multiplier
    Positional arguments: 1 2
    Keyword arguments: {'another': 'argument'}
    Return: 12
            
This is really cool. We have now separated the logging code entirely from the rest of our code, making everything
easier to read and maintain. It's also super easy to start logging new functions. Just add the `log_me` decorator! And
all of this is made possible by closures.

