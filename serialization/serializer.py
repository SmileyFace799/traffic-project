# ---
# Possible future work, for now, dumping json as string is sufficient
# ---

class SerializationError(IOError):
    pass

class UnknownVersionError(SerializationError):
    def __init__(self, version_major: int, version_minor: int, version_patch: int) -> None:
        super().__init__(f"No serializer found for version {version_major}.{version_minor}.{version_patch}")

class UndefinedOperationError(IOError):
    def __init__(self, operation: str, version_major: int, version_minor: int, version_patch: int) -> None:
        super().__init__(f"Operation \"{operation}\" is not defined for version {version_major}.{version_minor}.{version_patch}")

class _Serializer:
    def __init__(self, version_major: int, version_minor: int, version_patch: int):
        self.version_major = version_major
        self.version_minor = version_minor
        self.version_patch = version_patch

class _Serializer_0_0_0(_Serializer):
    def __init__(self):
        super().__init__(0, 0, 0)

serializer_map: dict[int, dict[int, dict[int, _Serializer]]] = {
    0: {
        0: {
            0: _Serializer_0_0_0()
        }
    }
}

def serializer(version_major: int, version_minor: int, version_patch: int):
    if (version_major not in serializer_map or version_minor not in serializer_map[version_major] or version_patch not in serializer_map[version_major][version_minor]):
        raise UnknownVersionError(version_major, version_minor, version_patch)
    return serializer_map[version_major][version_minor][version_patch]