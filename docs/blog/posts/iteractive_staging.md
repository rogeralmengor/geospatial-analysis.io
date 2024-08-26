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
$ touch math_operations.py
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
$ git add math_operations.py
$ git commit -m "feat: adding module basic arithmetic operations." 
```

# Creating factorial function

To create a bit of complexity in our rebasing, we add the factorial function to the math_operations.py file.

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

def factorial(n: int) -> int:
    """Calculate the factorial of n."""
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n-1)
```

We add and commit the changes: 

```bash
$ git add math_operations.py
$ git commit -m "feat: add factorial function.
```

We visualize our commit's tree by running:

```bash
git log --oneline --graph main
```
The output looks like this:

```bash
36710a0 (HEAD -> main, origin/main, origin/HEAD) feat: add factorial function.
* 2c3a6ae feat: adding module basic arithmetic operations.
```

# Starting the interactive rebasing/staging.

Now we'll use the interactive rebasing to start our split of the first commit we did in this tutorial (This commit is the second commit going from top-down in our commit's tree):

```bash 
$ git rebase -i HEAD~2
hint: Waiting for your editor to close the file...
```

A text editor, (normaly VIM will open... if you set another text editor then, the latter will open), opens, and asks you to change the actions of the commit list, from which you are doing the rebasing. We change the <b>pick</b> keyword for the <b>edit</b> keyword.

```bash
edit 2c3a6ae feat: adding module basic arithmetic operations.
pick 36710a0 feat: add factorial function.

# Rebase 8cca62b..36710a0 onto 8cca62b (2 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup [-C | -c] <commit> = like "squash" but keep only the previous
#                    commit's log message, unless -C is used, in which case
#                    keep only this commit's message; -c is same as -C but
#                    opens the editor
# x, exec <command> = run command (the rest of the line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop <commit> = remove commit
# l, label <label> = label current HEAD with a name
# t, reset <label> = reset HEAD to a label
# m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
#         create a merge commit using the original merge commit's
#         message (or the oneline, if no original merge commit was
#         specified); use -c <commit> to reword the commit message
# u, update-ref <ref> = track a placeholder for the <ref> to be updated
#                       to this position in the new commits. The <ref> is
#                       updated at the end of the rebase
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
```

If you are in vim, you can close the file by pressing ```:wq```. Once closed you can make a reset of the HEAD, because we are at the level of the commit we want to split.

```bash
$ git reset HEAD^
```

The output should be similar to this: 
```bash
Unstaged changes after reset:
M       docs/blog/math_operations.py
```

As you can see the the math_opeartions.py file has gone to a unstaged status. And we can start doing our modifications of the commits.

For that sake run the following git command: 

```bash 
git add -i
```

The output should look like that: 

```bash
staged     unstaged path
 1:    unchanged        +8/-1 docs/blog/math_operations.py

*** Commands ***
  1: status       2: update       3: revert       4: add untracked
  5: patch        6: diff         7: quit         8: help

What now>5
```

By entering <b>5 or p</b>, you will tell git to start the updating of the file you want to edit. Now, you can add the file number you want to edit:

```bash
What now> p 
           staged     unstaged path
  1:    unchanged        +8/-1 docs/blog/math_operations.py

Patch update>>1
```

```bash
Patch update>> 1
           staged     unstaged path
* 1:    unchanged        +8/-1 docs/blog/math_operations.py
```

Important: the * next to each file means the file is to be staged.


