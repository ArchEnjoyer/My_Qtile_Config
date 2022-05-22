import os
import subprocess
import re
import psutil
from libqtile import hook, qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import List

mod = "mod4"
terminal = guess_terminal()
myBrowser = "firefox" 

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # My Keys
    Key([mod], "b", lazy.spawn(myBrowser), desc='Firefox'),
]

groups = [Group(i) for i in [
    "WWW", "DEV", "SYS", "DOC", "GAMES", "CHAT", "MUS",
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])


    
def init_layout_theme():
    return {"margin":15,
            "border_width":3,
            "border_focus": "#67fff0", 
            "border_normal": "#ff00ff"         
            }

layout_theme = init_layout_theme()

layouts = [
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    layout.RatioTile(**layout_theme),
    layout.Tile(shift_windows=False, **layout_theme),
    layout.Floating(**layout_theme),
    layout.Max(**layout_theme),
]
colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=12,
    padding=3,
    background=colors[0]
)

#def change_language():
#    subprocess.call('/home/q/.config/qtile/language.py')

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Image(
                       filename = "~/.config/qtile/icons/python.png",
                       scale = "False",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "Ubuntu Bold",
                       fontsize = 9,
                       margin_y = 5,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[7],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[2],
                       background = colors[0],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[0],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),                      
              widget.Systray(
                       background = colors[0],
                       padding = 5
                       ),
              widget.Sep(
                       linewidth = 5,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),                       
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.Prompt(), 
              widget.Sep(
                       linewidth = 5,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = colors[8],
                       padding = -15,
                       fontsize = 42
                       ),
             widget.Net(
                       interface = "enp4s0",
                       format = 'Net: {down} ↓↑ {up}',
                       foreground = colors[1],
                       background = colors[8],
                       padding = 10
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[8],
                       foreground = colors[7],
                       padding = -15,
                       fontsize = 42
                       ),
              widget.ThermalSensor(
                       foreground = colors[1],
                       background = colors[7],
                       threshold = 90,
                       fmt = 'Temp: {}',
                       padding = 10
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[7],
                       foreground = colors[8],
                       padding = -15,
                       fontsize = 42
                       ),
              widget.Memory(
                       foreground = colors[1],
                       background = colors[8],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
                       fmt = 'Mem: {}',
                       padding = 10
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[8],
                       foreground = colors[7],
                       padding = -15,
                       fontsize = 42
                       ),
              widget.Volume(
                       foreground = colors[1],
                       background = colors[7],
                       fmt = 'Vol: {}',
                       padding = 10
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[7],
                       foreground = colors[8],
                       padding = -15,
                       fontsize = 42
                       ),
              widget.KeyboardLayout(
                       foreground = colors[1],
                       background = colors[8],
                       fmt = 'Keyboard: {}',
                       #mouse_callbacks = {'Button1': change_language()}
                       padding = 10
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[8],
                       foreground = colors[7],
                       padding = -15,
                       fontsize = 42
                       ),
              widget.Clock(
                       foreground = colors[1],
                       background = colors[7],
                       format = "%A, %d %B - %H:%M "
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[7],
                       foreground = colors[8],
                       padding = -15,
                       fontsize = 42
                       ),
              widget.Battery(
                       font = "Ubuntu Bold",
                       padding = 10,
                       fontsize = 15,
                       foreground = colors[0],                       
                       background = colors[8],
                       charge_char = '⥣',
                       discharge_char = '⥥',
                       format = "{char} {percent:2.0%} {hour:d}:{min:02d}"
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[8],
                       foreground = colors[3],
                       padding = -15,
                       fontsize = 42
                       ),
              widget.QuickExit(
                       background = colors[3],
                       default_text = '[ Bye! ]',
                       countdown_format='[   {}  ]',
                       font = "Ubuntu Bold",
                       padding = 10,
                       fontsize = 15,
                       foreground = colors[0],
                       ),
              ]
    return widgets_list

screens = [
    Screen(
        top=bar.Bar(
            widgets=init_widgets_list(),
            opacity=0.8,
            size=25,
            #border_width=[0, 0, 0, 0],  
            #border_color=["ff00ff", "ff00ff", "ff00ff", "ff00ff"] 
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call(home + '/.config/qtile/autostart.sh')

wmname = "LG3D"
