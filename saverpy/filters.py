def with_predicates(*preds):
    return lambda srcs: [src for src in srcs if all(pred(src) for pred in preds)]