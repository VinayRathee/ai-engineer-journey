def formatOutput(items):
    out = []
    for idx, item in enumerate(items):
        st = "DONE" if not item.get("status", False) else "PENDING"
        out.append(f"{idx}: {item.get('title')} [{st}]")
    return "\n".join(out)
