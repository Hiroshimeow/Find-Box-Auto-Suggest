from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
import threading

class HotkeyListener(QObject):
    # Signal to be emitted when hotkey is pressed
    activated = pyqtSignal()
    escape_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.hotkeys = None
        self.listener = None
        self.running = False

    def start(self):
        """Starts the global hotkey listener."""
        if self.running:
            return

        self.running = True
        # Define the hotkey combination
        # <ctrl>+<alt>+f
        self.hotkeys = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+f': self.on_activate
        })
        
        # Start the listener for ESC
        self.listener = keyboard.Listener(on_press=self.on_press)
        
        # Start the listeners in non-blocking way
        self.hotkeys.start()
        self.listener.start()

    def stop(self):
        """Stops the listener."""
        if self.hotkeys:
            self.hotkeys.stop()
        if self.listener:
            self.listener.stop()
        self.running = False

    def on_activate(self):
        """Callback when hotkey is pressed."""
        # Emit signal to main thread
        self.activated.emit()

    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.escape_pressed.emit()
