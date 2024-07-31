import os
import importlib.util
from types import ModuleType
from auto_report_writer.utils.custom_logger import logger


def import_directory(directory: str) -> dict[str, ModuleType]:
    """
    Imports all Python modules in the specified directory and returns them as a dictionary.

    :param directory: (str) Path to the directory containing Python modules to import.
    :return: (dict) Dictionary of module names and their corresponding imported modules.
    """
    modules = {}  # Initialising an empty dictionary to hold the imported modules.

    # Loops through each file in the specified directory.
    for filename in os.listdir(directory):
        # Checks if the file is a Python file and not an __init__.py file.
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Removes the '.py' from the file name to determine the module name.
            file_path = os.path.join(directory, filename)  # Constructs the full file path for the module.

            try:
                # Creates a module specification for the given module file.
                spec = importlib.util.spec_from_file_location(module_name, file_path)

                # Checks if the specification and loader are valid.
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)  # Creates a module based on the specification.
                    spec.loader.exec_module(module)  # Execute the module in its own namespace.
                    modules[module_name] = module  # Store the successfully imported module in the dictionary.
                    logger.info(f"Successfully loaded module: {module_name} from report_templates")

                else:
                    # Logs a warning if the module specification or loader is invalid.
                    logger.warning(f"Failed to load module: {module_name} from report_templates")

            except Exception as e:
                # Logs an error if an exception occurs during module loading.
                logger.error(f"Error loading module {module_name}: {e}")

    return modules
