# classification_app

## Setup

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Run the Streamlit app:

```bash
streamlit run app.py
```

## Notes

- The app entrypoint is `app.py`, which imports `index.py`.
- `index.py` contains the current UI and uses `data_handling.py` / `request_db.py` for future DB integration.