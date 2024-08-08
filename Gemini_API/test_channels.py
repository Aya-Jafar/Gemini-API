# test_imports.py
try:
    import channels
    from channels.auth import AuthMiddlewareStack
    print("Channels module is available")
except ImportError as e:
    print(f"ImportError: {e}")
