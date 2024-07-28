import importlib.util
import os


def import_directory(directory):
    """
    Imports all Python modules in the specified directory and returns them as a dictionary.

    :param directory: (str) Path to the directory containing Python modules to import.
    :return: (dict) Dictionary of module names and their corresponding imported modules.
    """
    modules = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Removes the '.py' from the file name to determine the module name.
            file_path = os.path.join(directory, filename)

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    modules[module_name] = module
                    print(f"Successfully loaded module: {module_name} from report_templates")

                else:
                    print(f"Failed to load module: {module_name} from report_templates")

            except Exception as e:
                print(f"Error loading module {module_name}: {e}")

    return modules
