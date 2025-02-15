import os

import cv2
import cvzone  # type: ignore
import psutil  # type: ignore
import pyautogui  # type: ignore
from rich import print


def openFile(fl_path: str) -> bool:
    try:
        os.startfile(fl_path)
        pyautogui.sleep(2)
        pyautogui.hotkey("f5")
        toggleAction(option="laser")
        return True
    except OSError:
        return False


def is_ppt_open():
    """Checks if PowerPoint is already open."""
    for process in psutil.process_iter(["name"]):
        if process.info["name"] and "POWERPNT" in process.info["name"].upper():
            return True
    return False


def open_presentation():
    """Handles opening a PowerPoint presentation."""
    if is_ppt_open():
        print(
            "[green]PowerPoint is already open. Please navigate to the desired presentation manually.[/green]"
        )
    else:
        ppt_path = input("Enter the full path of the PowerPoint file: ")
        if os.path.exists(ppt_path) and ppt_path.endswith((".ppt", ".pptx")):
            openFile(ppt_path)
        else:
            print("[red]Invalid file path. Please open the PowerPoint manually.[/red]")


def toggleAction(option: str):
    """
    Toggles the action based on the given option.

    This function maps the provided option to a corresponding hotkey
    and triggers the hotkey using pyautogui. The available options are:
    - "pen": Selects the pen tool.
    - "laser": Selects the laser pointer tool.
    - "eraser": Selects the eraser tool.
    - "highlighter": Selects the highlighter tool.

    If an invalid option is provided, it prints a warning message.

    Args:
        option (str): The tool option to select. Valid options are "pen",
                      "laser", "eraser", and "highlighter".

    Returns:
        None
    """
    fns = {"pen": "p", "laser": "l", "eraser": "e", "highlighter": "i"}
    fn = fns.get(option, None)
    if fn:
        pyautogui.hotkey("ctrl", fn)
        print(f"[green]Tool selected: {option}[green]")
    else:
        print(f"[yellow]Invalid option: {option}[yellow]")
    return option


def displayText(text: str, img: cv2.typing.MatLike) -> cv2.typing.MatLike:
    processedImg, _ = cvzone.putTextRect(
        img, text, (10, 100), scale=2, thickness=2, offset=7
    )
    return processedImg


def swipe(direction: str) -> None:
    pyautogui.press(direction)
    print("Swiped:", direction)


def mouseAction(x: int, y: int, type: str) -> None:
    w, h = pyautogui.size()
    if ((x <= w) or (y <= h)) or ((x > 0) or (y > 0)):
        if type == "move":
            # print(f"[green]Moving to: ({x}, {y})[green]")
            pyautogui.moveTo(x, y)
        elif type == "drag":
            # print(f"[green]Dragging to: ({x}, {y})[green]")
            pyautogui.dragTo(x, y)
        else:
            print(f"[yellow]Invalid type: {type}[yellow]")
    else:
        pass
