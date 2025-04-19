#!/bin/bash
#  _      __     ____                      
# | | /| / /__ _/ / /__  ___ ____  ___ ____
# | |/ |/ / _ `/ / / _ \/ _ `/ _ \/ -_) __/
# |__/|__/\_,_/_/_/ .__/\_,_/ .__/\__/_/   
#                /_/       /_/             
# -----------------------------------------------------
# Set defaults
# -----------------------------------------------------

force_generate=0
generatedversions="$HOME/.config/hypr/cache/wallpaper-generated"
cachefile="$HOME/.config/hypr/cache/current_wallpaper"
blurredwallpaper="$HOME/.config/hypr/cache/blurred_wallpaper.png"
squarewallpaper="$HOME/.config/hypr/cache/square_wallpaper.png"
rasifile="$HOME/.config/hypr/cache/current_wallpaper.rasi"
defaultwallpaper="$HOME/wallpaper/default.jpg"
blur="50x30"

# Create folder with generated versions of wallpaper if not exists
if [ ! -d $generatedversions ]; then
    mkdir $generatedversions
fi

# -----------------------------------------------------
# Get selected wallpaper
# -----------------------------------------------------

if [ -z $1 ]; then
    if [ -f $cachefile ]; then
        wallpaper=$(cat $cachefile)
    else
        wallpaper=$defaultwallpaper
    fi
else
    wallpaper=$1
fi
used_wallpaper=$wallpaper
echo ":: Setting wallpaper with source image $wallpaper"
tmpwallpaper=$wallpaper

# -----------------------------------------------------
# Copy path of current wallpaper to cache file
# -----------------------------------------------------

if [ ! -f $cachefile ]; then
    touch $cachefile
fi
echo "$wallpaper" > $cachefile
echo ":: Path of current wallpaper copied to $cachefile"

# -----------------------------------------------------
# Get wallpaper filename
# -----------------------------------------------------
wallpaperfilename=$(basename $wallpaper)
echo ":: Wallpaper Filename: $wallpaperfilename"

# -----------------------------------------------------
# Execute pywal
# -----------------------------------------------------
echo ":: Execute pywal with $used_wallpaper"
wal -q -i "$used_wallpaper"
source "$HOME/.cache/wal/colors.sh"

# -----------------------------------------------------
# Execute matugen
# -----------------------------------------------------
matugen -v image "$used_wallpaper"

# -----------------------------------------------------
# Walcord
# -----------------------------------------------------
if type walcord >/dev/null 2>&1; then
    walcord
fi

# -----------------------------------------------------
# Reload Waybar
# -----------------------------------------------------
killall -SIGUSR2 waybar

# -----------------------------------------------------
# Update Pywalfox
# -----------------------------------------------------
if type pywalfox >/dev/null 2>&1; then
    pywalfox update
fi

# -----------------------------------------------------
# Update Walogram
# -----------------------------------------------------
walogram -i "$used_wallpaper"

# -----------------------------------------------------
# Update SwayNC
# -----------------------------------------------------
sleep 0.1
swaync-client -rs

# -----------------------------------------------------
# Created blurred wallpaper
# -----------------------------------------------------
if [ -f $generatedversions/blur-$blur-$effect-$wallpaperfilename.png ] && [ "$force_generate" == "0" ] && [ "$use_cache" == "1" ]; then
    echo ":: Use cached wallpaper blur-$blur-$effect-$wallpaperfilename"
else
    echo ":: Generate new cached wallpaper blur-$blur-$effect-$wallpaperfilename with blur $blur"
    # notify-send --replace-id=1 "Generate new blurred version" "with blur $blur" -h int:value:66
    magick $used_wallpaper -resize 75% $blurredwallpaper
    echo ":: Resized to 75%"
    if [ ! "$blur" == "0x0" ]; then
        magick $blurredwallpaper -blur $blur $blurredwallpaper
        cp $blurredwallpaper $generatedversions/blur-$blur-$effect-$wallpaperfilename.png
        echo ":: Blurred"
    fi
fi
cp $generatedversions/blur-$blur-$effect-$wallpaperfilename.png $blurredwallpaper

# -----------------------------------------------------
# Create rasi file
# -----------------------------------------------------
if [ ! -f $rasifile ]; then
    touch $rasifile
fi
echo "* { current-image: url(\"$blurredwallpaper\", height); }" >"$rasifile"

# -----------------------------------------------------
# Created square wallpaper
# -----------------------------------------------------
echo ":: Generate new cached wallpaper square-$wallpaperfilename"
magick $tmpwallpaper -gravity Center -extent 1:1 $squarewallpaper
cp $squarewallpaper $generatedversions/square-$wallpaperfilename.png
