# Neo-snake

## 1. Installation
### a. The game font.
**Neo-snake** uses a special font that allows the terminal to display squares characters.  
One can download the *square* font [here](https://strlen.com/square/).  
Once the .ttf file in dowloaded, simply move it inside one of the system fonts directory.  
On Ubuntu 20.04 LTS, such directories are under `/usr/share/fonts`, `/usr/local/share/fonts` or `~/.fonts`. The latter does not require `sudo` rights as it is only local.

### b. Python modules
No particular dependencies (?).

### c. Dependencies.
Appears that the game only runs for `python>=3.8`. At least the game font does not load when not working with recent distributions of python.

## 2. Run the code.
Run the code by running the `./run` command in the shell from the root directory  
Or, one can create an alias of the game, to play it from anywhere.  
Simply append to either `~/.basrc` or `~/.bash_aliases` `alias <name>='<path/to/run>'`.
Then, run `source ~/.bashrc` or restart the terminal to apply the changes.
