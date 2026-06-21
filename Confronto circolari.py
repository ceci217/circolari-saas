def compare(old, new):
    diff = {
        "nuovi_obblighi": list(set(new["obblighi"]) - set(old["obblighi"])),
        "nuove_scadenze": list(set(new["scadenze"]) - set(old["scadenze"])),
        "modifiche_sanzioni": list(set(new["sanzioni"]) - set(old["sanzioni"]))
    }
    return diff
