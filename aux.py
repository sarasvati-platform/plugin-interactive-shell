def get_thought_path(thought):
    if not thought:
        return []

    visited = []
    tcurrent = thought
    tnext = None
    path = [thought.title]

    while tcurrent != None:
        if tcurrent in visited:
            tnext = None  # circular link
        elif len(tcurrent.links.parents) == 1:
            parent = tcurrent.links.parents[0]
            path.append(parent.title)
            tnext = parent
        elif len(tcurrent.links.parents) > 1:
            parents = tcurrent.links.parents
            parent_titles = list(map(lambda t: t.title, parents))
            parent_titles = ", ".join(parent_titles)
            path.append(f"[{parent_titles}]")
            tnext = None  # stop iterating
        elif len(tcurrent.links.references) == 1:
            reference = tcurrent.links.references[0]
            path.append(reference.title)
            tnext = reference

        visited.append(tcurrent)
        tcurrent = tnext
    
    return path