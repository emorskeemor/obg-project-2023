try:
    import django
    import rest_framework
except ImportError:
    raise ImportError(
        "using the contrib.django module requires django and the drf to be installed"
    )