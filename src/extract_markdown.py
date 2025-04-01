def extract_title(markdown):
    title = ""
    title = markdown.split("# ")
    title = title[1].split("\n")
    if title:
        return title[0].strip()
    else:
        raise Exception("Title not found in markdown")
