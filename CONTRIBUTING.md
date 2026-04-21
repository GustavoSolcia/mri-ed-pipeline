# How to contribute

You are welcome to contribute with the project. However, there are
a few housekeeping rules that everyone needs to follow.

## Testing

This repository contains mainly scripts that unifies two frameworks. Our
tests should focus in critical points that builds the pipeline.

## Submitting changes

Before start solving a really cool issue that you identified in the project, pay
attention to the issue number. The issue number will be essential for creating a branch
to work before asking for the pull request. Therefore, to open a new branch from
issue number "XX" that solves "problem" you should type:

```
git checkout -b IXX-problem 
```

After making some change or adding new code, you will need to make a commit. 
Your commit should contain the hashtag following a short but informative message
in the following way: 

```
git commit -m "Issue #XX: Added X to solve problem"
```

To push your local changes to this remote repository, in the first time you do it,
you need to type:

```
git push origin --set-upstream IXX-problem
```

You can always check how we are working in our branches and how we keep everything
organized. Also, don't feel afraid to send an e-mail to
[solcia.gustavo@outlook.com](mailto:solcia.gustavo@outlook.com).

## Coding conventions

By reading the code you will get an idea of the code convention. We mainly follow
[PEP-8](https://peps.python.org/pep-0008/) and [Google style](https://google.github.io/styleguide/pyguide.html)
docstrings.
