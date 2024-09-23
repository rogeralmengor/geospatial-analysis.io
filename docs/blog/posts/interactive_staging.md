---
title: Using git add -N and git add -patch to split a single's file commit into several commits 
description: Exploring a powerful technique from git tools to split a commit by the patches added in a file. 
time: 2024-8-26
---

"We've all been there." You're making changes to one or more files, with a clear goal: implement a logging system. But as you tweak lines of code, you also end up improving a function here, removing some comments, adding a new function, getting rid of a few print statements… all unrelated to the logging system. Now, you're stuck with a bunch of mixed changes, and it's time to git add. Imagine you've already committed everything under the message "changes to the logging system"—sound familiar? Frustrating, right?

Fortunately, Git provides a great tool called interactive staging. While it’s typically used for organizing changes from the working directory to the staging area, you can also apply it to older commits. This lets you cleanly organize your commits by theme, so each commit truly reflects the purpose of the changes.

In this tutorial, we'll explore how to do that and answer this key question:

!!! question
    How to split a commit that adds several independent lines of code, in a commit down the tree?

## Create initial python file. 

The first thing we do is to create a file called math_operations.py. I am in a linux environment using <a href="https://github.com/features/codespaces" target="_blank">coding spaces</a>, so I create the file using the touch command.

!!! warning "Creating initial file"
    ```bash
    $ touch math_operations.py
    ```

## Create basic arithmethic functions and commit

Now we want to create the 4 functions for basic arithmetic operations (add, subtract, multiply and divide) in the math_opeartions.py file.

!!! abstract "math_operations.py"
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

!!! warning "Adding and commiting changes in initial file"
    ```bash
    $ git add math_operations.py
    $ git commit -m "feat: add module basic arithmetic operations."
    ```

## Creating factorial function

To create a bit of complexity in our rebasing, we add the factorial function to the math_operations.py file.

!!! abstract "math_operations.py"
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

!!! warning "Adding and commiting new changes"
    ```bash
    $ git add math_operations.py
    $ git commit -m 'feat: add factorial function.
    ```

We visualize our commit's tree by running:

!!! warning "git log --oneline --graph main"
    ```bash
    * c291adb (HEAD -> main) feat: add factorial function.
    * fd18571 feat: add module basic arithmetic operations.
    ```

## Starting the interactive rebasing/staging.

Now we'll use the interactive rebasing to start our split of the first commit we did in this tutorial (This commit is the second commit going from top-down in our commit's tree):

!!! warning "Starting interactive rebasing to second commit down the tree"
    ```bash 
    $ git rebase -i HEAD~2
    hint: Waiting for your editor to close the file...
    ```

A text editor, (normaly VIM will open... if you set another text editor then, the latter will open), opens, and asks you to change the actions of the commit list, from which you are doing the rebasing. We change the <b>pick</b> keyword for the <b>edit</b> keyword.

!!! warning "Editing the git todo file"
    ```bash
    edit fd18571 feat: adding module basic arithmetic operations.
    pick c291adb feat: add factorial function.

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

!!! warning "Resetting the last changes"
    ```bash
    $ git reset HEAD^
    Unstaged changes after reset:
    M       docs/blog/math_operations.py
    ```

As you can see the the math_opeartions.py file has gone to a unstaged status. And we can start doing our modifications of the commits.

This is an important concept to bear in mind when doing this specific modification of the git history. There is the staging area in a git repository, which contains a copy of the files being changed in the next commits. However since the math_operations.py file does not exists in the previous commit, in order to add changes in this file, we have to create a file which will be patched against. The following command will do that for us, which basically adds an empty `math_operations.py` file in the index to start the interactive staging.

!!! warning "Adding file to index"
    ```bash
    $ git add -N math_operations.py
    ```

Once we do that, we can start adding the patches.

!!! warning "Start adding patches"
    ```bash
    $ git add -p match_operations.py
    diff --git a/math_operations.py b/math_operations.py
    new file mode 100644
    index 0000000..615a19b
    --- /dev/null
    +++ b/math_operations.py
    @@ -0,0 +1,15 @@
    +def add(a: float, b: float) -> float:
    +    """Add two numbers."""
    +    return a + b
    +
    +def subtract(a: float, b: float) -> float:
    +    """Subtract b from a."""
    +    return a - b
    +
    +def divide(a: float, b: float) -> float:
    +    """Divide a by b."""
    +    return a / b
    +
    +def multiply(a: float, b: float) -> float:
    +    """Multiply a and b."""
    +    return a * b
    \ No newline at end of file
    (1/1) Stage addition [y,n,q,a,d,e,p,?]? 
    ```

As you can see, since all the changes were introduced in the same commit at once, the patches, which are called hunks in this tool, appear as the entire file. That is not very usefull, since we want to create single commits for every function we are introducing.
For that, lets type the option e, which stands for editing. And we'll start adding the changes one by one, in single commits.

When typing `e`, a file named addp-hunk-edit.diff will be opened in your text editor, with the following contents:

!!! warning "Manual editing of hunks"
    ```bash
    # Manual hunk edit mode -- see bottom for a quick guide.
    @@ -0,0 +1,15 @@
    +def add(a: float, b: float) -> float:
    +    """Add two numbers."""
    +    return a + b
    +
    +def subtract(a: float, b: float) -> float:
    +    """Subtract b from a."""
    +    return a - b
    +
    +def divide(a: float, b: float) -> float:
    +    """Divide a by b."""
    +    return a / b
    +
    +def multiply(a: float, b: float) -> float:
    +    """Multiply a and b."""
    +    return a * b
    \ No newline at end of file
    # ---
    # To remove '-' lines, make them ' ' lines (context).
    # To remove '+' lines, delete them.
    # Lines starting with # will be removed.
    # If the patch applies cleanly, the edited hunk will immediately be marked for staging.
    # If it does not apply cleanly, you will be given an opportunity to
    # edit again.  If all lines of the hunk are removed, then the edit is
    # aborted and the hunk is left unchanged.
    ```

As you can see all the lines with the four functions we want to add individually are listed as an entire patch.

!!! danger "Important!"
    If you're using Git with VSCode and the editor doesn't open when you press 'e' during interactive staging (git add -p), there are a few steps you can take to resolve this issue:

    Check your Git configuration:
        Make sure Git is configured to use VSCode as your default editor. 
        You can do this by running:
            ```git config --global core.editor "code --wait"```
        This sets VSCode as the default editor and tells Git to wait for the file to be closed before proceeding.

Let's just manually delete the functions subtract, divide and multiply, and save and close the changes. It should look like that: 

!!! warning "Leaving only the lines we are going to first commit"
    ```bash
    # Manual hunk edit mode -- see bottom for a quick guide.
    @@ -0,0 +1,15 @@
    +def add(a: float, b: float) -> float:
    +    """Add two numbers."""
    +    return a + b
    +
    \ No newline at end of file
    # ---
    # To remove '-' lines, make them ' ' lines (context).
    # To remove '+' lines, delete them.
    # Lines starting with # will be removed.
    # If the patch applies cleanly, the edited hunk will immediately be marked for staging.
    # If it does not apply cleanly, you will be given an opportunity to
    # edit again.  If all lines of the hunk are removed, then the edit is
    # aborted and the hunk is left unchanged.
    ```

After that being done, we can check out the status and the following should appear:

!!! warning "Checking out status"
    ```bash
    $ git status
    interactive rebase in progress; onto 6d5b423
    Last command done (1 command done):
    edit fd18571 feat: add module basic arithmetic operations.
    Next command to do (1 remaining command):
    pick 03413b7 feat: add factorial function.
    (use "git rebase --edit-todo" to view and edit)
    You are currently splitting a commit while rebasing branch 'main' on '6d5b423'.
    (Once your working directory is clean, run "git rebase --continue")

    Changes to be committed:
    (use "git restore --staged <file>..." to unstage)
            new file:   math_operations.py

    Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git restore <file>..." to discard changes in working directory)
            modified:   math_operations.py
    ```

As you can see there are in the same file, changes that are ready to be commited (the step where we only left the function add, and remove all others), and changes to be staged (all the changes from the original hunk, or patch).

Now just create a commit for the first function.

!!! warning "Commiting first changes"
    ```bash
    $ git commit -m feat: add add function.
    [detached HEAD f78a69a] feat: add add function.
    1 file changed, 3 insertions(+)
    create mode 100644 math_operations.py
    ```

Now we can again start the addition of the next patches.

!!! warning "Adding second patches (subtract function)"
    ```bash
    $ git add -p math_operations.py
    diff --git a/math_operations.py b/math_operations.py
    index 81d2d3b..615a19b 100644
    --- a/math_operations.py
    +++ b/math_operations.py
    @@ -1,3 +1,15 @@
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    +
    +def subtract(a: float, b: float) -> float:
    +    """Subtract b from a."""
    +    return a - b
    +
    +def divide(a: float, b: float) -> float:
    +    """Divide a by b."""
    +    return a / b
    +
    +def multiply(a: float, b: float) -> float:
    +    """Multiply a and b."""
    +    return a * b
    \ No newline at end of file
    (1/1) Stage this hunk [y,n,q,a,d,e,p,?]? 
    ```

As we can see now, the only patches to be added, are the lines where the subtract, divide and multiply function were added. We have to repeat the process, by deleting the lines we don't need by the next commit which is the addition of the subtract function. We have to start again the edit mode, by typing e, and then leaving only the lines which add the subtract function:

!!! warning "Manual editing of patches"
    ```bash
    $ e
    # Manual hunk edit mode -- see bottom for a quick guide.
    @@ -1,3 +1,15 @@
    def add(a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    +
    +def subtract(a: float, b: float) -> float:
    +    """Subtract b from a."""
    +    return a - b
    +
    \ No newline at end of file
    # ---
    # To remove '-' lines, make them ' ' lines (context).
    # To remove '+' lines, delete them.
    # Lines starting with # will be removed.
    # If the patch applies cleanly, the edited hunk will immediately be marked for staging.
    # If it does not apply cleanly, you will be given an opportunity to
    # edit again.  If all lines of the hunk are removed, then the edit is
    # aborted and the hunk is left unchanged.
    ```

Now we add and commit the subtract function.

!!! warning "Commiting second patch"
    ```bash
    $ git commit -m "feat: add subtract func.
    ```

We have to repeat the same sequence for the functions remaining: divide and multiply. For sake of simplicity we won't add these steps in this tutorial, you surely at this point know how to do so for the remaning code. The message is clear: just type `git add -p <file_name>`, type `e` for the manual editing, delete the lines which don't belong to this commit, then `git commit -m <message>`, and repeat until the last commit.

Now we can continue with the interactive rebasing, since the next commit is only to add the factorial function, and it should apply without complains.

!!! success "$ git rebase --continue"
    ```bash
    Successfully rebased and updated refs/heads/main
    ```

Let's see our commit's tree:

!!! success "$ git log --oneline"
    ```bash
    c291adb (HEAD -> main) feat: add factorial function.
    92e7ccb feat: add multiply func.
    2c08167 feat: add divide func.
    2d5b8d7 feat: add subtract func.
    2a3a6c2 feat: add add func.
    ```

Yes!, we just created four commits which comprise the individual changes made in a file, from one commit which had all of the changes as a big chunk. In that way, we can keep our commit history cristal clear, and with individual, incremental changes on the file. If later we want to squeeze those changes or add them as an individual one by using the fix keyword, is our decision.


#### References

Chacon, Scott, and Ben Straub. Pro Git. 2nd ed. Berkeley, CA: Apress, 2014. <a href="https://git-scm.com/book/en/v2." target="_blank">Git Book</a>