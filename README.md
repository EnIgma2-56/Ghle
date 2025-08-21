# SecureVote (Fixed Layout)

This archive applies these fixes:
- Proper package layout with `app/` as the root package.
- `__init__.py` files added.
- All API routers consolidated under `app/routers/` (remove/ignore any duplicate nested `app/core/app` from your old repo).
- Render start command corrected.

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Deploy on Render
Set the **Start Command** to:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
(Ensure `requirements.txt` and `runtime.txt` are present.)
