# How to contribute

## How to start

Once you have cloned the repository you should then create a virtual environment to seperate this project from affecting any projects you are currently working on, on your system.  To create and start the virtual environment

    $ python -m venv .venv
    #
    # Linux, Bash
    $ source .venv/bin/activate
    # Linux, Fish
    $ source .venv/bin/activate.fish
    # Linux, Csh
    $ source .venv/bin/activate.csh
    # Linux, PowerShell Core
    $ .venv/bin/Activate.ps1
    # Windows, cmd.exe
    > .venv\Scripts\activate.bat
    # Windows, PowerShell
    > .venv\Scripts\Activate.ps1
    # Then we want to install our dependacies
    $ pip install -r requirements.txt

    # The install pre-commit
    $ pre-commit install

This next step can be done anywhen before committing/submitting which is to make a branch.  What are yo going to work on?

    $ git checkout [available_branch_name]
    # or create a new branch
    $ git checkout -b [branch_name]

## Formatting and Styling

So you have added `print("Hello, World!)` to a file well done, now let us check if you have maintained to our style guide and formatting

    $ git add . # to stage it
    $ pre-commit run --all-files
    # this will do all the checks if you want to do a smaller subset
    $ autoflake8 -i .  # is a quicker check

## Testing

So your code is correctly formatted. does it affect performance, test if this change breaks anything by doing the following

    $ python -m unittest tests/*
    # then it will output results from each test

## Submitting changes

You start by staging

    $ git add .

Then you commit with a message either by `-m` flag like this

    $ git commit -m "A brief summary of the commit
    >
    > A paragraph describing what changed and its impact."

But you can do without the flag and your system default text editor should open

you've made the change locally, but the final `push` is to:

    $ git push

## Finishing your session

Finished for the day want to do something else on your computer

    $ mischief managed
    # just kidding
    $ deactivate
    # that will now return you out of the virtual environment
