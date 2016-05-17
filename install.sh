
sudo apt install xdotool wmctrl python-docopt -y

dconf load /org/gnome/settings-daemon/plugins/media-keys/ < ./dconf/org.gnome.settings-daemon.plugins.media-keys              
dconf load /org/compiz/profiles/unity/plugins/unityshell/ < ./dconf/unityshell 
gsettings set  org.gnome.desktop.lockdown disable-lock-screen true
gsettings set org.gnome.desktop.wm.keybindings close "['<Shift><Super>q']"
gsettings set org.gnome.desktop.wm.keybindings switch-input-source "['disabled']"
gsettings set org.gnome.desktop.wm.keybindings switch-input-source-backward "['disabled']"
