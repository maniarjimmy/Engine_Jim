import sys
import os
import site

print("Python Executable:", sys.executable)
print("System Path:")
for p in sys.path:
    print(f"  {p}")

print("\nAttempting imports:")

try:
    import ORE
    print("SUCCESS: import ORE")
    print("ORE file:", ORE.__file__)
except ImportError as e:
    print("FAILURE: import ORE")
    print(e)
    
try:
    import QuantLib
    print("SUCCESS: import QuantLib")
    print("QuantLib file:", QuantLib.__file__)
except ImportError as e:
    print("FAILURE: import QuantLib")
    print(e)

print("\nSite Packages:")
for sp in site.getsitepackages():
    print(f"  {sp}")
    try:
        if os.path.exists(sp):
            print(f"  Listing {sp} matching 'ORE' or 'open_source':")
            for f in os.listdir(sp):
                if 'ORE' in f or 'open_source' in f or 'quantlib' in f.lower():
                    print(f"    {f}")
    except Exception as e:
        print(f"    Error listing {sp}: {e}")
