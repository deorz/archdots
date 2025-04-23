from ignis.widgets import Widget
from ignis.services.niri import NiriService, NiriWindow

niri = NiriService.get_default()


def handle(active_window: NiriWindow) -> list[Widget.Label]:
    """"""
    return [
        Widget.Label(
            css_classes=["window_app"],
            label=active_window.app_id,
            justify="left",
        ),
        Widget.Label(
            css_classes=["window_title"],
            label=active_window.title,
            justify="left",
        ),
    ]


class ActiveWindow(Widget.Box):
    def __init__(self):
        child = []
        if niri.is_available:
            child.append(
                Widget.Box(
                    css_classes=["active_window"],
                    orientation="vertical",
                    spacing=2,
                    child=niri.bind_many(
                        ["active_window"],
                        transform=handle,
                    ),
                )
            )
        super().__init__(child=child)
