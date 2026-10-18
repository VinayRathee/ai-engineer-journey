def formatOutput(items):
    out = []
    for idx, item in enumerate(items):
        st = "DONE" if item.status else "PENDING"
        out.append(f"{idx}: {item.title} [{st}]")
    return "\n".join(out)
