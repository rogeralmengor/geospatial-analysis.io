---
title: Stop Wasting Time on Intermediate Variables, function composition to the rescue!
description: Exploring a powerful technique from the functional programming paradigm in your python code. 
time: 2023-4-13
---

# Stop Wasting Time on Intermediate Variables: function composition to the rescue!
Have you ever found yourself trying to make many array manipulations, and storing the results in temporal variables such as temp1, temp2, temp_prefinal, temp_before_final, etc.?

I had this sort of problem, until I came across to a technique called function composition. This can be applied in python using the functools, and it’s undoubtedly a good tool for any data scientist to write efficient and readable code. That will avoid the need to store intermediate variables (with poor names ;o) ) and make your code easier to read and understand.

Consider the following code that calculates the sum of the squares of the first five integers using intermediate variables:

```python title="example_1.py" linenums="1"

# Bad practice: using intermediate variables
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
squared_arr = np.square(arr)
sum_of_squares = np.sum(squared_arr)
print(sum_of_squares)  # Output: 55
```

While this approach can be useful for some situations, it can become cumbersome when working with larger datasets and complex manipulations.

By chaining NumPy array manipulations, you can save time and avoid creating multiple intermediate variables. That’s when the technique of function composition comes in handy.

You can use the functools.reduce method to apply a list of functions to an initial input value, allowing you to further streamline your code.

```python title="example_2.py" linenums="1"
# Using functools.reduce to apply a list of 
# functions to an initial input value
import numpy as np
import functools

arr = np.array([1, 2, 3, 4, 5])
sum_of_squares = functools.reduce(lambda x, f: f(x), 
                              [np.square, np.sum], arr)

print(sum_of_squares)  # Output: 55
```

In this example, functools.reduce applies the list of functions [np.square, np.sum] to the initial input value arr in a sequential manner, with each function taking the output of the previous function as its input. The lambda function lambda x, f:f(x) is used to apply each function in the list to the previous result.

Using functools.reduce can be a powerful way to streamline your code and avoid the need for intermediate variables when working with NumPy arrays.

Regarding functional programming, functools.reduce is a common technique used in functional programming languages like Haskell and Lisp, where functions are first-class citizens and can be treated like any other value. While some developers see functional programming as the best way to write software, others prefer object-oriented or procedural programming paradigms.

As a data scientist, I believe it’s important to choose the best approach for the task at hand. While you may not be a fan of functional programming as a paradigm, you can still incorporate functional programming techniques like functools.reduce when they make sense for your input data, data flow, and outputs. By taking a pragmatic approach and combining different programming paradigms, you can write efficient and readable code that meets your project goals.

Now that you’ve seen how to use NumPy’s dot function chaining and functools.reduce to streamline your code, why not try it out in some of your code? Whether you’re working on a data analysis project or a machine learning model, these techniques can help you write more efficient and readable code. So go ahead and give it a try!

<br>