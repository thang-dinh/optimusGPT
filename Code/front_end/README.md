## Getting Started

Follow the steps below to run the app locally.

### 1. Clone the repository

```bash
git clone https://github.com/thang-dinh/optimusGPT.git
cd optimusGPT/Code/front_end
```

### 2. Install dependencies

Make sure you have **Node.js (v18 or higher)** and **npm** installed. Then run:

```bash
npm install
```

This will install all required dependencies from `package.json`, including:

* `react`
* `react-dom`
* `react-router-dom`
* `@reduxjs/toolkit`
* `react-redux`
* `tailwindcss`
* `autoprefixer`
* `postcss`
* `vite`
* `typescript`
* `clsx`
* `lucide-react`
* `@headlessui/react`

If Tailwind hasn’t been initialized yet:

```bash
npx tailwindcss init -p
```

Then to update backend dpendencies into the Poetry enviornment

```bash
poetry install
``

To run the **front end** run the following commands to get everything set up properly

```bash
cd Code
poetry install 
$env:PYTHONPATH = "."
poetry run uvicorn api.app:app --reload --host 127.0.0.1 --port 8000
```

Now open a new terminal and run this after you see the 

***INFO:     Application startup complete. ***
message:

```bash
npm install
npm run dev
```
You will see a few info packages installed after install
Then after the run dev command you...

Now click on the link next to local to access the site!!


To close and exit the local server type 
ctrl + C 