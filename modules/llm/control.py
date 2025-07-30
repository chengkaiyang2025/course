import streamlit as st
from abc import ABC, abstractmethod
from collections import deque

# Command Pattern Interfaces and Implementations
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

# Receiver: The actual device
class ColorLightPanel:
    def __init__(self):
        self.is_on = False
        self.brightness = 100  # Default brightness
        self.color = "white"   # Default color

    def turn_on(self):
        self.is_on = True
        return "Light panel turned ON."

    def turn_off(self):
        self.is_on = False
        return "Light panel turned OFF."

    def set_brightness(self, value):
        old = self.brightness
        self.brightness = value
        return f"Brightness changed from {old} to {value}."

    def set_color(self, color):
        old = self.color
        self.color = color
        return f"Color changed from {old} to {color}."

# Concrete Commands
class OnCommand(Command):
    def __init__(self, panel: ColorLightPanel):
        self.panel = panel
        self.prev_state = panel.is_on

    def execute(self):
        self.prev_state = self.panel.is_on
        return self.panel.turn_on()

    def undo(self):
        if not self.prev_state:
            return self.panel.turn_off()
        else:
            return self.panel.turn_on()

class BrightnessCommand(Command):
    def __init__(self, panel: ColorLightPanel, brightness):
        self.panel = panel
        self.brightness = brightness
        self.prev_brightness = panel.brightness

    def execute(self):
        self.prev_brightness = self.panel.brightness
        return self.panel.set_brightness(self.brightness)

    def undo(self):
        return self.panel.set_brightness(self.prev_brightness)

class ColorCommand(Command):
    def __init__(self, panel: ColorLightPanel, color):
        self.panel = panel
        self.color = color
        self.prev_color = panel.color

    def execute(self):
        self.prev_color = self.panel.color
        return self.panel.set_color(self.color)

    def undo(self):
        return self.panel.set_color(self.prev_color)

# Invoker: RemoteControl
class RemoteControl:
    def __init__(self):
        self.history = deque(maxlen=3)  # Store last 3 commands
        self.output = []

    def press_button(self, command: Command):
        result = command.execute()
        self.history.appendleft(command)
        self.output.append(result)
        return result

    def undo(self):
        if self.history:
            command = self.history.popleft()
            result = command.undo()
            self.output.append(f"Undo: {result}")
            return result
        else:
            self.output.append("Nothing to undo.")
            return "Nothing to undo."

    def get_output(self):
        return self.output

# Streamlit UI
def main():
    st.title("Remote Control for Color Light Panel (Command Pattern Demo)")
    if 'panel' not in st.session_state:
        st.session_state['panel'] = ColorLightPanel()
    if 'remote' not in st.session_state:
        st.session_state['remote'] = RemoteControl()

    panel = st.session_state['panel']
    remote = st.session_state['remote']

    # Display current panel state more prominently
    st.markdown(f"""
    <div style='padding: 1em; border: 2px solid #4A90E2; border-radius: 10px; background: #f0f8ff; margin-bottom: 1em;'>
        <b>Current Panel Status:</b><br>
        <b>Brightness:</b> {panel.brightness}<br>
        <b>Color:</b> {panel.color}<br>
        <b>ON:</b> {panel.is_on}
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Turn ON"):
            cmd = OnCommand(panel)
            remote.press_button(cmd)
    with col2:
        if st.button("Dim (Brightness 10)"):
            cmd = BrightnessCommand(panel, 10)
            remote.press_button(cmd)
    with col3:
        if st.button("Set Color Blue"):
            cmd = ColorCommand(panel, "blue")
            remote.press_button(cmd)
    with col4:
        if st.button("Undo"):
            remote.undo()

    st.subheader("Command Output Log:")
    for line in remote.get_output():
        st.write(line)

if __name__ == "__main__":
    main()
