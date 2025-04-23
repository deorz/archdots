from ignis.widgets import Widget
from ignis.services.niri import NiriService, NiriWindow, NiriWorkspace

niri = NiriService.get_default()


def handle(
    workspaces: list[NiriWorkspace],
    windows: list[NiriWindow],
    active_window: NiriWindow,
) -> list[Widget.Box]:
    """"""
    bubbles = []
    workspaces.sort(key=lambda ws: ws.id)
    windows.sort(key=lambda w: w.id)
    for ws_id, workspace in enumerate(workspaces, start=1):
        wigdet = Widget.Box(
            css_classes=[
                "bubble-group",
                f"ws_{ws_id}",
            ],
            orientation="horizontal",
            spacing=4,
            child=[
                Widget.Label(
                    css_classes=[
                        "bubble",
                        f"ws_{ws_id}",
                        *(["active"] if window.id == active_window.id else []),
                    ],
                )
                for window in windows
                if window.workspace_id == workspace.id
            ],
        )
        if wigdet.child:
            bubbles.append(wigdet)

    return bubbles


def scroll_workspaces(direction: str) -> None:
    current = list(filter(lambda w: w.is_active, niri.workspaces))[0].idx
    if direction == "up":
        target = current + 1
        niri.switch_to_workspace(target)
    else:
        target = current - 1
        niri.switch_to_workspace(target)


class Workspaces(Widget.Box):
    def __init__(self):
        child = []
        if niri.is_available:
            child.append(
                Widget.EventBox(
                    on_scroll_up=lambda x: scroll_workspaces("up"),
                    on_scroll_down=lambda x: scroll_workspaces("down"),
                    css_classes=["workspaces"],
                    spacing=5,
                    child=niri.bind_many(
                        ["workspaces", "windows", "active_window"],
                        transform=handle,
                    ),
                )
            )
        super().__init__(child=child)
