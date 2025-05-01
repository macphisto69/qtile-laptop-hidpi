# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from scripts import storage

import os

# import re
# import socket
import subprocess

# from typing import List  # noqa: F401
from libqtile import layout, bar, hook, qtile
from libqtile.lazy import lazy
from libqtile.config import (
    Drag,
    Group,
    Key,
    Match,
    Screen,
    Click,
    ScratchPad,
    DropDown,
)  # Rule,
from libqtile.widget import Spacer
from libqtile.widget import base

# QTILE EXTRAS
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

# From The Linux Cast's dotfiles
import colors
colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.gruvbox()


# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser("~")
home_dir = os.path.expanduser("~")
terminal = f"alacritty --config-file {
    home_dir}/.config/alacritty/alacritty.yml"
# terminal = "alacritty"


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


keys = [
    # Most of our keybindings are in sxhkd file - except these
    # SUPER + FUNCTION KEYS
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    # SUPER + SHIFT KEYS
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    # RESIZE UP, DOWN, LEFT, RIGHT
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),
    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    # Scratchpads
    Key([mod], "m", lazy.group["music"].dropdown_toggle("tunes")),
]


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


keys.extend(
    [
        # MOVE WINDOW TO NEXT SCREEN
        Key(
            [mod, "shift"],
            "Right",
            lazy.function(window_to_next_screen, switch_screen=True),
        ),
        Key(
            [mod, "shift"],
            "Left",
            lazy.function(window_to_previous_screen, switch_screen=True),
        ),
    ]
)

groups = []

# FOR QWERTY KEYBOARDS
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]

# group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
# group_labels = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",]
group_labels = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
# group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = [
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "RATIOTILE",
]
# group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

groups.append(
    ScratchPad(
        "music",
        [
            DropDown(
                "tunes",
                "alacritty -e ncmpcpp",
                x=0.05,
                y=0.02,
                width=0.95,
                height=0.6,
                on_focus_lost_hide=False,
            )
        ],
    )
)

for i in groups:
    if i.name in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
        keys.extend(
            [
                # CHANGE WORKSPACES
                Key([mod], i.name, lazy.group[i.name].toscreen()),
                Key([mod], "Tab", lazy.screen.toggle_group()),
                Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
                Key(["mod1"], "Tab", lazy.screen.next_group()),
                Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
                # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
                # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
                # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name),
                    lazy.group[i.name].toscreen(),
                ),
            ]
        )


def init_layout_theme():
    return {
        "margin": 8,
        "border_width": 2,
        # "border_focus": "#5e81ac",
        "border_focus": colors[5],
        "border_normal": colors[1],
    }


layout_theme = init_layout_theme()


layouts = [
    # layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadWide(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme),
    layout.Spiral(**layout_theme),
]

# COLORS FOR THE BAR
# Theme name : AxylOS


def init_separator():
    return widget.Sep(
        size_percent=60,
        margin=5,
        linewidth=2,
        background=colors[1],
        foreground="#555555",
    )


def nerd_icon(nerdfont_icon, fg_color):
    return widget.TextBox(
        font="Iosevka Nerd Font",
        # font = "SauceCodePro Nerd Font",
        fontsize=16,
        text=nerdfont_icon,
        foreground=fg_color,
        background=colors[1],
    )


def init_edge_spacer():
    return widget.Spacer(length=5, background=colors[1])


# colors = init_colors()
sep = init_separator()
space = init_edge_spacer()


# WIDGETS FOR THE BAR


def init_widgets_defaults():
    return dict(
        font="JetBrains Mono Nerd Font", fontsize=22, padding=7, background=colors[12]
    )


widget_defaults = init_widgets_defaults()

powerline = {
    "decorations": [
        RectDecoration(),
        PowerLineDecoration(path="forward_slash"),
    ]
}


def init_widgets_list():
    # prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        # Left Side of the bar
        space,
        widget.Image(
            filename="/home/michael/.config/qtile/arch_18x18.png",
            background=backgroundColor,
            margin=3,
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(
                    "dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=14'"
                ),
                "Button3": lambda: qtile.cmd_spawn(
                    f"{terminal} -e nvim {home_dir}/.config/qtile/config.py"
                ),
            },
            # **decoration_group
        ),
        widget.GroupBox(
            font="Comic Sans MS",
            fontsize=40,
            foreground=colors[2],
            background=backgroundColor,
            borderwidth=2,
            padding=4,
            highlight_method="text",
            this_current_screen_border=colors[6],
            active=colors[4],
            inactive=colors[11],
        ),
        widget.Spacer(length=bar.STRETCH, background=backgroundColor, **powerline),
        # widget.Spacer(length=bar.STRETCH, background=colors[1]),
        widget.TextBox(fmt="", background=backgroundColor, **powerline),
        widget.Battery(
            background = colors[8],
            **powerline
        ),
        widget.CheckUpdates(
            update_interval=1800,
            distro="Arch_checkupdates",
            display_format="Updates: {updates} ",
            initial_text="Checking...",
            no_update_string="No updates",
            colour_have_updates="#000",
            colour_no_updates="#000",
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(terminal + " -e sudo pacman -Syu")
            },
            padding=5,
            background="#989bbc",
            **powerline,
        ),
        widget.CurrentLayout(
            foreground="#FFF", background="#722a44", **powerline),
        widget.CPU(
            format="{load_percent}%",
            foreground="#FFF",
            background="#2a6872",
            update_interval=2,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(
                f"{terminal} -e gtop")},
            **powerline,
        ),
        widget.Memory(
            format="{MemUsed:.0f}{mm}",
            foreground="#FFF",
            background="#C70039",
            update_interval=2,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(
                f"{terminal} -e gtop")},
            **powerline,
        ),
        widget.GenPollText(
            foreground="#FFF",
            background="#a6b1f7",
            update_interval=5,
            func=lambda: storage.diskspace("FreeSpace"),
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn(
                f"{terminal} -e gtop")},
            **powerline,
        ),
        widget.GenPollText(
            foreground="#101703",
            background="#DAF7A6",
            update_interval=5,
            func=lambda: subprocess.check_output(
                f"{home_dir}/.config/qtile/scripts/num-installed-pkgs"
            ).decode("utf-8"),
            **powerline,
        ),
        widget.Net(
            format="{down:5.2f}{down_suffix} ↓↑ {up:5.2f}{up_suffix}",
            foreground="#FFF",
            background="#5dade2",
            width=160,
            scroll=True,
            scroll_fixed_width=True,
            update_interval=5,
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn("def-nmdmenu")},
            **powerline,
        ),
        widget.Clock(
            format="%d-%h-%Y %H:%M",
            foreground="#FFF",
            background="#3e27aa",
            **powerline,
        ),
        widget.Systray(
            background="#000",
            # foreground = '#000',
            icon_size=30,
            **powerline,
        ),
    ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


# def init_widgets_screen2():
#    widgets_screen2 = init_widgets_list()
#    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
# widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen1(),
                margin=[8, 12, 0, 12],
                opacity=1,
                size=48,
            )
        )
    ]


screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #####################################################################################
#     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#     #####################################################################################
#     d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d[group_names[3]] = ["Gimp", "gimp" ]
#     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d[group_names[5]] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d[group_names[6]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d[group_names[7]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d[group_names[8]] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d[group_names[9]] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ######################################################################################
#
# wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen(toggle=False)

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME


main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Arcolinux-welcome-app.py"),
        Match(wm_class="Arcolinux-calamares-tool.py"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="Galculator"),
        Match(wm_class="archlinux-logout"),
        # Match(wm_class='xfce4-terminal'),
    ],
    fullscreen_border_width=0,
    border_width=0,
)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
