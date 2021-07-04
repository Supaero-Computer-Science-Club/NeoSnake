# snake

gsettings set org.gnome.desktop.interface monospace-font-name 'Ubuntu Mono 13'
gsettings set org.gnome.desktop.interface monospace-font-name 'square 13'
gsettings set org.gnome.desktop.interface monospace-font-name 'square 13' && python src/main.py && gsettings set org.gnome.desktop.interface monospace-font-name 'Ubuntu Mono 13'


Dowload font [here](https://strlen.com/square/).

Put it inside `/usr/share/fonts`, `/usr/local/share/fonts` or `~/.fonts`. The latter does not require `sudo`.

Run the code with `./run`