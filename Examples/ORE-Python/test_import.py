import sys
import os

print("Python executable:", sys.executable)
print("sys.path:", sys.path)

try:
    import ORE
    print("Successfully imported ORE")
    print("ORE module location:", ORE.__file__)
except ImportError as e:
    print("Failed to import ORE:", e)
except Exception as e:
    print(f"An error occurred: {e}")
