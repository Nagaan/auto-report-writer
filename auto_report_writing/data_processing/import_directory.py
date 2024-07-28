import importlib.util
import os


def import_directory(directory):
    """
    Import all modules in the specified directory.
    """
    modules = {}
    for filename in os.listdir(directory):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            file_path = os.path.join(directory, filename)
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    modules[module_name] = module
                    print(f"Successfully loaded module: {module_name} from {file_path}")
                else:
                    print(f"Failed to load module: {module_name} from {file_path}")
            except Exception as e:
                print(f"Error loading module {module_name}: {e}")
    return modules
