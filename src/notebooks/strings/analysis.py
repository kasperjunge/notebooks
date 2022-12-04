def string_analyzer(string: str, include_string: bool = False) -> dict:
    analysis = {"ints": 0, "alphas": 0, "dots": 0, "spaces": 0}
    for c in string:
        if c.isalpha():
            analysis["alphas"] += 1
        if c.isnumeric():
            analysis["ints"] += 1
        if c == ".":
            analysis["dots"] += 1
        if c.isspace():
            analysis["spaces"] += 1
    if include_string:
        analysis["string"] = string
    analysis["ia_ratio"] = analysis["alphas"] / (analysis["ints"] + 1)
    return analysis
