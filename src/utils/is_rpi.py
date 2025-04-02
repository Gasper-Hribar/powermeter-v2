def is_raspberry_pi():
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "Raspberry Pi" in line:
                    return True
    except Exception:
        pass
    return False