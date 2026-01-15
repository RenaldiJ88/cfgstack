# cfgstack

Layered configuration resolution with explicit override semantics.

`cfgstack` resolves a key against an ordered stack of layers, highest
priority first. Each layer either sets the key or leaves it unset, and the
effective value is the highest-priority layer that sets it. Layers are
ordinary Python values, so a stack can come from environment variables, a
config file, a database row, a dataclass, or any combination.

## The two kinds

Every key is resolved with one of two kinds:

- **`KIND_SCALAR`** — booleans, numbers, strings, and arbitrary objects.
  A layer sets the key when its value is not `None`. `False`, `0`, `""`, and
  empty collections are ordinary values; a layer that wants to leave the key
  unset passes `None`.

- **`KIND_SEQUENCE`** — tuples, lists, and other sized collections.
  A layer sets the key when it provides a non-empty collection. An empty
  collection reads as "no entries to contribute at this layer", so
  resolution falls through to the next layer.

The distinction exists because a scalar carries no separate notion of
"empty": `False` is a value, not the absence of one. A sequence does: `()`
reads naturally as "nothing to add here".

## Status

`cfgstack` is pre-1.0. The public surface is `resolve`, `KIND_SCALAR`, and
`KIND_SEQUENCE`.

## License

MIT.
