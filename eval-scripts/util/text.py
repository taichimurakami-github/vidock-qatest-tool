remove_non_ascii = lambda text: "".join(
    char for char in text if 31 < ord(char) & ord(char) < 127
)

remove_cp932 = lambda text: text.encode("cp932", "ignore").decode("cp932")
