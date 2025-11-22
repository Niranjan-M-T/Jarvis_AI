import os
import subprocess
import platform

class CommandExecutor:
    def __init__(self, config):
        self.config = config
        self.allowed_commands = config.get("allowed_commands", [])

    def execute(self, command_data):
        """
        Execute the command based on the structured data.
        """
        intent = command_data.get("intent")

        print(f"Executing intent: {intent}")

        if intent == "open_application":
            app_name = command_data.get("application")
            return self._open_application(app_name)
        elif intent == "system_control":
            action = command_data.get("action")
            # Implement system control
            pass
        elif intent == "chat":
            return command_data.get("response")

        return "Command executed."

    def _open_application(self, app_name):
        if platform.system() == "Windows":
            # Simple example mapping or direct start
            try:
                os.startfile(app_name) # Windows only
                return f"Opening {app_name}"
            except Exception as e:
                return f"Failed to open {app_name}: {e}"
        else:
            return f"Opening applications is only supported on Windows. (Tried to open {app_name})"
