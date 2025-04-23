import datetime
from ignis.widgets import Widget
from ignis.utils import Utils
from ignis.app import IgnisApp
from ignis.services.audio import AudioService
from ignis.services.system_tray import SystemTrayService, SystemTrayItem
from ignis.services.niri import NiriService

from widgets.workspaces import Workspaces
from widgets.active_window import ActiveWindow

app = IgnisApp.get_default()

app.apply_css(f"{Utils.get_current_dir()}/style.scss")


audio = AudioService.get_default()
system_tray = SystemTrayService.get_default()
niri = NiriService.get_default()


def clock() -> Widget.Label:
    return Widget.Label(
        css_classes=["clock"],
        label=Utils.Poll(
            1_000,
            lambda _: datetime.datetime.now().strftime("%a %d %b %H:%M"),
        ).bind("output"),
    )


def speaker_volume() -> Widget.Box:
    return Widget.Box(
        child=[
            Widget.Icon(
                image=audio.speaker.bind("icon_name"), style="margin-right: 5px;"
            ),
            Widget.Label(
                label=audio.speaker.bind("volume", transform=lambda value: str(value))
            ),
        ]
    )


def keyboard_layout() -> Widget.EventBox:
    return Widget.EventBox(
        on_click=lambda _: niri.switch_kb_layout(),
        child=[
            Widget.Label(
                label=niri.keyboard_layouts.bind("current_name"),
            )
        ],
    )


def tray_item(item: SystemTrayItem) -> Widget.Button:
    if item.menu:
        menu = item.menu.copy()
    else:
        menu = None

    return Widget.Button(
        css_classes=["tray-item"],
        child=Widget.Box(
            child=[
                Widget.Icon(image=item.bind("icon"), pixel_size=24),
                menu,
            ]
        ),
        setup=lambda self: item.connect("removed", lambda x: self.unparent()),
        tooltip_text=item.bind("tooltip"),
        on_click=lambda x: menu.popup() if menu else None,
        on_right_click=lambda x: menu.popup() if menu else None,
    )


def tray():
    return Widget.Box(
        css_classes=["tray"],
        setup=lambda self: system_tray.connect(
            "added",
            lambda x, item: self.append(tray_item(item)),
        ),
        spacing=10,
    )


def left() -> Widget.Box:
    return Widget.Box(
        child=[
            ActiveWindow(),
        ],
        spacing=10,
    )


def center() -> Widget.Box:
    return Widget.Box(
        child=[
            Workspaces(),
        ],
        spacing=10,
    )


def right() -> Widget.Box:
    return Widget.Box(
        css_classes=["right_widgets"],
        child=[
            tray(),
            keyboard_layout(),
            speaker_volume(),
            clock(),
        ],
        spacing=10,
    )


def bar(monitor_id: int = 0) -> Widget.Window:
    monitor_name = Utils.get_monitor(monitor_id).get_connector()

    return Widget.Window(
        namespace=f"ignis_bar_{monitor_id}",
        monitor=monitor_id,
        anchor=["left", "top", "right"],
        exclusivity="exclusive",
        child=Widget.CenterBox(
            css_classes=["bar"],
            start_widget=left(),
            center_widget=center(),
            end_widget=right(),
        ),
    )


for i in range(Utils.get_n_monitors()):
    bar(i)
