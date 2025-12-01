def breadth_first_search(
    next,
    found,
    state_filter=lambda a: True,
    serialize=lambda a: a,
    optimize_visited=True,
    optimize_queued=False,
    keep_history=False
):
    def search(
        init,
        limit=None,
    ):
        queue = [(0, init, [] if keep_history else None)]
        visited = set()
        queued = set()
        while len(queue) > 0:
            state = queue.pop(0)

            ln, inner, history = state
            if limit is not None and ln > limit:
                return None, None, None
            visited.add(serialize(inner))

            next_states = [
                (ln + 1, v, history + [inner] if keep_history else None)
                for v in next(inner)
                if state_filter(v)
                and (not optimize_visited or not serialize(v) in visited)
                and (not optimize_queued or not serialize(v) in queued)
            ]

            for next_state in next_states:
                nln, inner, history = next_state
                if found(inner):
                    return inner, nln, history
                queue.append(next_state)
                if optimize_queued:
                    queued.add(serialize(inner))
        return None, None, None
    return search