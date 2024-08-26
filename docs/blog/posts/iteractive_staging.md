---
title: Using iteractive staging to split a commit 
description: Exploring a powerful technique from git tools to split a commit by the patches added in a file. 
time: 2024-8-26
---

# Using iteractive staging to split a commit

I'm generally very curious about my work. However, in recent days, I had an pending task with Git. So I picked up the Git book written by Scott Chacon and Ben Straub, and I started reading it assiduously during this vacation. I thought I already knew and applied many things in my workflow, but the more I read through the pages of this book, the more I realized how far I was from using some of the powerful strategies and tools that Git makes available to improve my experience as a programmer.

Today, I want to talk about a common problem we sometimes face when reviewing or publishing commits in our repository: how to split a commit that adds several independent lines of code, but which are added in a single commit. This is what we're going to describe in detail in the following blog post.
