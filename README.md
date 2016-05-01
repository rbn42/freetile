This is a window tiling and navigation tool based on [stiler](//github.com/TheWanderer/stiler). It tries to imitate the very basic functions of i3-wm.

![](https//raw.githubusercontent.com/wiki/rbn42/stiler/show2.gif)

Dependency
=
```bash
sudo apt install xdotool wmctrl python-docopt -y
sudo apt install xprop -y
```

Usage
=

See
```bash
python main.py -h
```

Recommended Keyboard Mapping
=

| Keys      | Command   |
| ------------- |-------------| 
|`<Super> <Space>`    |  `python main.py layout next` |
|`<Super> <Shift> <Space>`    |  `python main.py layout prev` |
|`<Super> h`    |  `python main.py focus left` |
|`<Super> <Shift> h`    |  `python main.py swap left` |
|`<Super> <Ctrl> h`    |  `python main.py move left` |
|`<Super> <Shift> <Ctrl> h`    |  `python main.py shrink width` |
|`<Super> j`    |  `python main.py focus down` |
|`<Super> <Shift> j`    |  `python main.py swap down` |
|`<Super> <Ctrl> j`    |  `python main.py move down` |
|`<Super> <Shift> <Ctrl> j`    |  `python main.py grow height ` |
|`<Super> k`    |  `python main.py focus up` |
|`<Super> <Shift> k`    |  `python main.py swap up` |
|`<Super> <Ctrl> k`    |  `python main.py move up` |
|`<Super> <Shift> <Ctrl> k`    |  `python main.py shrink height ` |
|`<Super> l`    |  `python main.py focus right` |
|`<Super> <Shift> l`    |  `python main.py swap right` |
|`<Super> <Ctrl> l`    |  `python main.py move right` |
|`<Super> <Shift> <Ctrl> l`    |  `python main.py grow width ` |


