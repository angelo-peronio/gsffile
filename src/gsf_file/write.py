def write_gsf(data, file_name, metadata={}):
    """Write a 2D array to a Gwyddion Simple Field 1.0 file format
    http://gwyddion.net/documentation/user-guide-en/gsf.html

    Args:
        file_name (string): the name of the output (any extension will be replaced)
        data (2darray): an arbitrary sized 2D array of arbitrary numeric type
        metadata (dict): additional metadata to be included in the file

    Returns:
        nothing
    """

    XRes = data.shape[0]
    YRes = data.shape[1]

    data = data.astype("float32")

    if file_name.rpartition(".")[1] == ".":
        file_name = file_name[0 : file_name.rfind(".")]

    gsfFile = open(file_name + ".gsf", "wb")

    s = ""
    s += "Gwyddion Simple Field 1.0" + "\n"
    s += "XRes = {0:d}".format(XRes) + "\n"
    s += "YRes = {0:d}".format(YRes) + "\n"

    for i in metadata.keys():
        try:
            s += i + " = " + "{0:G}".format(metadata[i]) + "\n"
        except ValueError:
            s += i + " = " + str(metadata[i]) + "\n"

    gsfFile.write(bytes(s, "UTF-8"))

    gsfFile.write(b"\x00" * (4 - len(s) % 4))

    gsfFile.write(data.tobytes(None))

    gsfFile.close()
