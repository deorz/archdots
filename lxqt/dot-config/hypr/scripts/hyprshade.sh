#!/bin/bash
#  _   _                      _               _
# | | | |_   _ _ __  _ __ ___| |__   __ _  __| | ___
# | |_| | | | | '_ \| '__/ __| '_ \ / _` |/ _` |/ _ \
# |  _  | |_| | |_) | |  \__ \ | | | (_| | (_| |  __/
# |_| |_|\__, | .__/|_|  |___/_| |_|\__,_|\__,_|\___|
#        |___/|_|
#

# Toggle Hyprshade based on the selected filter
hyprshade_filter="blue-light-filter-50"

# Toggle Hyprshade
if [ -z $(hyprshade current) ]; then
    echo ":: hyprshade is not running"
    hyprshade on $hyprshade_filter
    notify-send "Hyprshade activated" "with $(hyprshade current)"
    echo ":: hyprshade started with $(hyprshade current)"
else
    notify-send "Hyprshade deactivated"
    echo ":: Current hyprshade $(hyprshade current)"
    echo ":: Switching hyprshade off"
    hyprshade off
fi
