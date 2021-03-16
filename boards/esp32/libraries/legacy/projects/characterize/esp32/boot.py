import micropython, sys

micropython.alloc_emergency_exception_buf(100)
sys.path.append('/flash/lib')
