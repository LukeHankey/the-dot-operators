# The-dot-opertator's submission

## Our solution
It's a jigsaw game. The goal is simple, you simply have to put the pieces together to form the image.

## Features
- You can choose the difficulty of the puzzle (choose "Quick" for a 16 pieces jig-saw puzzle, "Secret code"[¹](#m) for a 36 pieces puzzle).
- ~~You can choose the image you want to play with~~
- ~~You can set the game fullscreen~~
- ~~You can change the tile snapping sensitivity~~
- ~~You can use an image api to get random images~~

Why are most features crossed out? Because we didn't have time to **fully** implement them. We had a lot of ideas, but we didn't have enough time to implement them all.
We had to make choices, and we decided to focus on the core gameplay and forgot to remove these features from the setting panel. 
Also, a lot of these features were almost ready to shipped and as a result pieces of code are still present in the codebase. This paragraph is an explanation of why there so much unused code in the codebase.


## How to play

#### Creating the environment
Create a virtual environment in the folder `.venv`.
```shell
$ python -m venv .venv
```

#### Enter the environment
It will change based on your operating system and shell.
```shell
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
```

#### Installing the Dependencies
Once the environment is created and activated, use this command to install the game's dependencies.
```shell
$ pip install -r requirements.txt
$ pip install pygame_gui==0.6.9
```

#### Exiting the environment

```shell
$ deactivate
```


#### Running the game
```shell
$ python main.py
```

## Has the theme been respected?
No, unfortunately we didn't have enough time to implement secret code it should have been added in the **secret code** difficulty.
But as I said earlier, this difficulty only changes the number of pieces. On the other side, **image processing** is the core of the app
