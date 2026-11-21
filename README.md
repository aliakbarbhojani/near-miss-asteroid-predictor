# Near Miss

Finds the asteroids passing close to Earth, using NASA's free
[Near Earth Object API](https://api.nasa.gov/).

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install the packages:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and put your NASA API key in it.
   Get a free key at https://api.nasa.gov/.

## Run

```powershell
python fetch.py
```

## Files

| File               | What it is                                              |
| ------------------ | ------------------------------------------------------- |
| `fetch.py`         | Calls the NASA API and prints what comes back           |
| `.env`             | Your API key (private, ignored by git)                  |
| `.env.example`     | Shows what `.env` should look like, without a real key  |
| `requirements.txt` | The packages this project needs                         |
| `.gitignore`       | Files git should never track                            |
