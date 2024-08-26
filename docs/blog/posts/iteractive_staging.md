---
title: Using iteractive staging to split a commit 
description: Exploring a powerful technique from git tools to split a commit by the patches added in a file. 
time: 2024-8-26
---

# Using iteractive staging to split a commit

I'm generally very curious about my work. However, in recent days, I had an pending task with Git. So I picked up the <a href="https://git-scm.com/book/en/v2" target="_blank">Git Book</a> written by Scott Chacon and Ben Straub, and I started reading it assiduously during this vacation. 

I thought I already knew and applied many things in my workflow, but the more I read through the pages of this book, the more I realized how far I was from using some of the powerful strategies and tools that Git makes available to improve my experience as a programmer.

Today, I want to talk about a common problem we sometimes face when reviewing or publishing commits in our repository: how to split a commit that adds several independent lines of code, but which are added in a single commit. This is what we're going to describe in detail in the following blog post.

# Create initial python file. 

The first thing we do is to create a file called math_operations.py. I am in a linux environment using <a href="https://github.com/features/codespaces" target="_blank">coding spaces</a>, so I create the file using the touch command.

```bash
@rogeralmengor ➜ /workspaces/geospatial-analysis.io/docs/blog (main) $ touch math_operations.py
```

# Create basic arithmethic functions and commit

Now we want to create the 4 functions for basic arithmetic operations (add, subtract, multiply and divide) in the math_opeartions.py file.

```python
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b

def multiply(a: float, b: float) -> float:
    """Multiply a and b."""
    return a * b
```

We commit the changes:

```bash
@rogeralmengor ➜ /workspaces/geospatial-analysis.io/docs/blog (main) $ git add math_operations.py
@rogeralmengor ➜ /workspaces/geospatial-analysis.io/docs/blog (main) $ git commit -m "feat: adding module basic arithmetic operations." 
```