---
title: Khmer Lemmatization Studio
emoji: 👁
colorFrom: red
colorTo: pink
sdk: gradio
sdk_version: 6.8.0
app_file: app.py
pinned: false
license: mit
short_description: lemmatizing Khmer words to their root (base) form.
---

# Khmer Lemmatization Studio

A web-based tool for lemmatizing Khmer text reducing inflected or derived words to their root (base) form.

## Demo

> Paste any Khmer text, click **Lemmatization**, and instantly see each token alongside its root form.

## Features

- **CRF-based tokenization** via [khmer-nltk](https://github.com/VietHoang1512/khmer-nltk) for accurate Khmer word segmentation
- **Dictionary lookup** — maps derived/inflected words to their root forms
- **Token-level results table** — shows every token, its lemma, and whether it changed
- **Summary statistics** — total token count and number of lemmatized tokens
- **Sample text** — one-click load of example Khmer sentences
- **Full dictionary view** — browse all 60 entries directly in the UI

## Project Structure

```
khmer_lemmatization/
├── app.py                       # Main Gradio application
├── khmer_lemma_dictionary.json  # Lemma dictionary (derived → root)
├── requirements.txt             # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/PhorkNorak/Khmer-Lemmatization.git
cd Khmer-Lemmatization

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
python app.py
```

Then open your browser at `http://127.0.0.1:7860`.

## Dictionary

The lemma dictionary (`khmer_lemma_dictionary.json`) contains **60 entries** mapping derived Khmer words to their root forms. It was compiled from:

> **Teacher Vatha** — [១០០០ពាក្យកម្លាយដោយផ្នត់ដើម (YouTube)](https://youtu.be/mfWl3fV7oMo?si=OuR45gnDqeml2oXw)

Contributions to expand the dictionary are welcome — see [Contributing](#contributing).

## Deployment

This app is deployed on [Hugging Face Spaces](https://huggingface.co/spaces/Norak007/Khmer-Lemmatization-Studio).

## Contributing

Contributions are welcome! To add words to the dictionary:

1. Fork the repository
2. Edit `khmer_lemma_dictionary.json` — add entries as `"derived_form": "root_form"`
3. Open a pull request with a brief description

For code contributions, please open an issue first to discuss your proposed change.

## License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 Phork Norak, Nhor Povketya, Ly Hor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Developers

| Name | Role | Portfolio |
|------|------|-----------|
| Phork Norak | Full-Stack Developer | [phorknorak.vercel.app](https://phorknorak.vercel.app/) |
| Nhor Povketya | Data Analyst | [povketya.github.io/ketyanhor](https://povketya.github.io/ketyanhor/) |
| Ly Hor | Data Analyst | [final-portfolio-kappa-rust.vercel.app](https://final-portfolio-kappa-rust.vercel.app/) |

---

*Royal University of Phnom Penh — Data Science & Engineering Program*
