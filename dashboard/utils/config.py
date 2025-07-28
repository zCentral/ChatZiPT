import os
try:
    import tomllib  # Python 3.11+
except ImportError:
    import toml

def load_config(path="config.toml"):
    if os.path.exists(path):
        try:
            if "tomllib" in globals():
                with open(path, "rb") as f:
                    return tomllib.load(f)
            else:
                with open(path, "r") as f:
                    return toml.load(f)
        except Exception as e:
            print(f"Error loading TOML config: {e}")
            return {}
    else:
        return {}

config = load_config()