def read_file(filename: str) -> str:
    with open(filename) as file:
        return "\n".join(file.readlines())