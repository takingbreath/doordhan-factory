# Adding a model provider

models.json knows a provider only if it is listed under "providers" with `enabled` and `ledgered` both true; otherwise
models.py skips its candidates, however good they are. That is deliberate: every paid call must be priced and written to
the ledger before it is sent (hard rule 2), and today only Higgsfield has that (hooks/spend_guard.py, spend.py).

To bring a second vendor in:
1. Ask Akhilesh. A new paid vendor changes where money is spent.
2. Write its client beside higgsfield_api.py (request(), error_text(), key from .env, never printed).
3. Give it a spend hook the way Higgsfield has one: price each call before it goes, write it to the ledger, block over
   budget and unknown prices (fail closed). Add its units to prices.json, or a sibling price table.
4. Add its candidates to a role in models.json with the same `shape` as the model they stand in for, or write the
   request translation in the caller (a Wan 2.7 request is not a Wan 3.0 request, so a different vendor's is not either).
5. Put `"<name>": {"enabled": true, "ledgered": true}` under "providers". `models.py check` and the self-test then cover it.
6. Let QC decide: add `"models": {"<role>": "<model>"}` to the reel's qc manifest so model_scores.py learns how it does.
