import os
import subprocess
import platform
import psutil
import webbrowser
import shutil
from pathlib import Path

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

        elif intent == "system_stats":
            return self._get_system_stats()

        elif intent == "system_control":
            action = command_data.get("action")
            return self._system_control(action)

        elif intent == "file_operation":
            operation = command_data.get("operation")
            path = command_data.get("path")
            name = command_data.get("name")
            return self._file_operation(operation, path, name)

        elif intent == "search_web":
            query = command_data.get("query")
            return self._search_web(query)

        elif intent == "chat":
            return command_data.get("response")

        return "Command executed."

    def _open_application(self, app_name):
        if platform.system() == "Windows":
            try:
                # Basic normalization for common apps could go here
                os.startfile(app_name)
                return f"Opening {app_name}"
            except Exception as e:
                return f"Failed to open {app_name}: {e}"
        else:
            return f"Opening applications is only supported on Windows. (Tried to open {app_name})"

    def _get_system_stats(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        return f"CPU usage is at {cpu_usage} percent. RAM usage is at {ram_usage} percent."

    def _system_control(self, action):
        if platform.system() != "Windows":
             return "System control commands are designed for Windows."

        if action == "shutdown":
            # os.system("shutdown /s /t 1")
            return "Shutting down the system..." # logic commented out for safety in dev
        elif action == "restart":
            # os.system("shutdown /r /t 1")
            return "Restarting the system..."
        else:
            return f"Unknown system action: {action}"

    def _file_operation(self, operation, path_str, name):
        # Default to desktop if path not provided, or handle specific paths
        if not path_str:
            # Get user's desktop path
            path_str = os.path.join(os.path.expanduser("~"), "Desktop")

        target_path = Path(path_str) / name

        try:
            if operation == "create_folder":
                target_path.mkdir(parents=True, exist_ok=True)
                return f"Created folder {name} at {path_str}"

            elif operation == "delete_file":
                # Safety check: Only allow deleting from specific user directories to avoid system damage
                safe_dirs = [
                    os.path.join(os.path.expanduser("~"), "Desktop"),
                    os.path.join(os.path.expanduser("~"), "Documents"),
                    os.path.join(os.path.expanduser("~"), "Downloads")
                ]

                is_safe = any(str(target_path).startswith(safe_dir) for safe_dir in safe_dirs)

                if not is_safe:
                    return f"Security alert: Deletion denied for path {target_path}. Only Desktop, Documents, and Downloads are allowed."

                if target_path.exists():
                    if target_path.is_dir():
                        shutil.rmtree(target_path)
                    else:
                        target_path.unlink()
                    return f"Deleted {name} from {path_str}"
                else:
                    return f"File or folder {name} not found at {path_str}"

            else:
                return f"Unknown file operation: {operation}"

        except Exception as e:
            return f"Error performing file operation: {e}"

    def _search_web(self, query):
        if not query:
            return "What would you like me to search for?"

        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching for {query}"
