import json
import string
from dataclasses import dataclass
from pathlib import Path

import gradio as gr
from khmernltk import word_tokenize as khmer_word_tokenize

BASE_DIR = Path(__file__).resolve().parent
DICT_PATH = BASE_DIR / "khmer_lemma_dictionary.json"

KHMER_PUNCTUATION = {
    "។", "៕", "៚", "៖", "៘", "៙", "៛", "៝",
    "ៗ", "៑", "៓", "។", "៘", "ៜ",
}
ZERO_WIDTH_CHARS = {"\u200b", "\u200c", "\u200d"}
PUNCTUATION_CHARS = set(string.punctuation) | KHMER_PUNCTUATION

SAMPLE_TEXT = ("យើងត្រូវតែផ្គាប់ចិត្តខ្លួនឯងដោយការខ្ជាប់ខ្ជួននូវច្បាប់សីលធម៌ល្អ។ កុំផ្តឹងផ្តល់ ឬផ្តេកផ្តិតទៅលើកំហុសអតីតកាល។ ជីវិតប្រៀបដូចជាការរៀបចំរនាបនិងរនាស់ដើម្បីបណ្ដុះផលល្អ។ ត្រូវកកាយរកនូវចំណេះដឹងថ្មីៗ មិនមែនកកូរចលាចលនោះទេ។ ចេះចចឹករៀនសូត្រពីអ្នកដទៃ មិនមែនសសារឬសសិតរឿងឥតប្រយោជន៍ឡើយ។ ត្រូវជ្រើសរើសដោយឈ្លាសវៃ កុំឲ្យឱកាសល្អៗខ្ចាត់បាត់ ព្រោះយើងខ្ទាស់ចិត្តនឹងសេចក្តីស្អប់ ឬក្បង់យករបស់អាក្រក់។ គំនិតក្លាយជាល្អឬខ្មៅ គឺអាស្រ័យលើយើង ហើយយើងមិនគួរគ្មានមហិច្ឆតាឡើយ។ កុំឆ្កឹះរឿងអ្នកដទៃ កុំធ្វើអ្វីឲ្យឆ្គង។ ត្រូវរៀនសូត្រពីច្បងៗ ធ្វើការងារដោយច្បូតច្បាស់លាស់ ហើយឆ្លាក់ស្នាដៃល្អទុក។ ពេលជួបការលំបាក ត្រូវជ្រុះចោលនូវទុក្ខកង្វល់ ធ្វើចិត្តឲ្យជ្រះថ្លា ឲ្យការយល់ដឹងជ្រាបចូលក្នុងខ្លួន ហើយត្រៀបរៀបចំផែនការដើម្បីត្រងយកតែភាពជោគជ័យ។ ត្រូវផ្ចង់ស្មារតី ទាំងចិត្តផ្កូរឿងល្អ និងផ្ដល់ឲ្យអ្នកដទៃដោយចិត្តបរិសុទ្ធ។ កុំផ្ដាច់ទំនាក់ទំនងល្អ ត្រូវធ្វើអ្វីៗដោយផ្ទាល់ដៃ ហ៊ានផ្ទុកបន្ទុក ហើយប្រឹងប្រែងស្ទាក់ចាប់គោលដៅ ហើយស្រាយបំភ្លឺរាល់បញ្ហាដោយតម្លាភាព។"
)

DEFAULT_STATS = {
    "ពាក្យសរុប": "0",
    "ពាក្យកម្លាយ": "0",
}

EMPTY_TABLE = [["-", "—", "—", "—"]]


@dataclass
class LemmaRow:
    token: str
    lemma: str
    changed: bool


def load_dictionary(path=DICT_PATH):
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Dictionary file not found at {path}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Dictionary JSON is invalid: {e}")
    if not isinstance(data, dict):
        raise RuntimeError("Dictionary must be a JSON object.")
    return data


def _normalize_token(token):
    return "".join(ch for ch in token if ch not in ZERO_WIDTH_CHARS).strip()


def _is_special_token(token):
    normalized = _normalize_token(token)
    return not normalized or all(ch in PUNCTUATION_CHARS for ch in normalized)


def tokenize(text):
    if not text:
        return []
    return [tok for tok in khmer_word_tokenize(text) if tok.strip()]


def lemmatize_tokens(tokens, dictionary):
    rows = []
    for token in tokens:
        lemma = dictionary.get(token, token)
        rows.append(LemmaRow(token=token, lemma=lemma, changed=lemma != token))
    return rows


def format_stats(rows):
    return {
        "ពាក្យសរុប": f"{len(rows):,}",
        "ពាក្យកម្លាយ": f"{sum(1 for r in rows if r.changed):,}",
    }


def render_stats_cards(stats):
    cards = "".join(
        f"""
        <div class="kpi-card">
            <span class="kpi-label">{label}</span>
            <span class="kpi-value">{value}</span>
        </div>
        """
        for label, value in stats.items()
    )
    return f"""
    <style>
      .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        width: 100%;
      }}
      .kpi-card {{
        border-radius: 16px;
        padding: 18px 20px;
        border: 1px solid var(--border-color-primary, rgba(148, 163, 184, 0.35));
        background: var(--block-background-fill, var(--background-fill-secondary, #fff));
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
      }}
      .kpi-label {{
        font-size: 0.8rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--body-text-color-subdued, #64748b);
      }}
      .kpi-value {{
        display: block;
        margin-top: 8px;
        font-size: 2rem;
        font-weight: 700;
        color: var(--body-text-color, #0f172a);
      }}
      @media (prefers-color-scheme: dark) {{
        .kpi-card {{
          box-shadow: none;
        }}
      }}
    </style>
    <div class="kpi-grid">{cards}</div>
    """


def run_pipeline(text):
    tokens = [t for t in tokenize(text or "") if not _is_special_token(t)]
    rows = lemmatize_tokens(tokens, LEMMA_DICT)
    combined_text = "".join(r.lemma for r in rows)
    table = [[i + 1, r.token, r.lemma, "បាន" if r.changed else "មិនបាន"] for i, r in enumerate(rows)]
    if not table:
        table = EMPTY_TABLE
    return table, render_stats_cards(format_stats(rows)), combined_text


def clear_inputs():
    return "", gr.update(value=None), render_stats_cards(DEFAULT_STATS), ""


def build_interface():
    with gr.Blocks(title="Khmer Lemmatization Studio", theme=gr.themes.Default()) as demo:
        gr.HTML(
            """
            <link href="https://fonts.googleapis.com/css2?family=Kantumruy+Pro:ital,wght@0,100..700;1,100..700&display=swap" rel="stylesheet">
            <style>
              * { font-family: 'Kantumruy Pro', sans-serif !important; }
            </style>
            <div style="text-align: center; margin-bottom: 1.5rem;">
              <h1>Khmer Lemmatization Studio</h1>
              <p>ជួយសិស្សស្វែងរក <strong>ពាក្យឫស</strong> នៃ <strong>ពាក្យកម្លាយ</strong> ក្នុងភាសាខ្មែរបានយ៉ាងងាយស្រួល</p>
            </div>
            """
        )

        with gr.Row():
            with gr.Column(scale=3):
                text_input = gr.Textbox(
                    label="បំពេញអត្ថបទ",
                    placeholder="វាយ ឬបិទភ្ជាប់អត្ថបទខ្មែរនៅទីនេះ...",
                    lines=10,
                    autofocus=True,
                )
                with gr.Row():
                    process_btn = gr.Button("រកពាក្យឫស", variant="primary")
                    sample_btn = gr.Button("យកអត្ថបទគំរូ")
                    clear_btn = gr.Button("លុបចោល")
                gr.Markdown(
                    """
                    **របៀបប្រើ**
                    1. វាយ ឬបិទភ្ជាប់អត្ថបទខ្មែរ
                    2. ចុចប៊ូតុង **រកពាក្យឫស**
                    3. មើលតារាងពាក្យកម្លាយ និងពាក្យឫស នៅខាងស្តាំ
                    """
                )
            with gr.Column(scale=4):
                stats_panel = gr.HTML(render_stats_cards(DEFAULT_STATS))
                combined_output = gr.Textbox(
                    label="អត្ថបទបន្ទាប់ពីរកពាក្យឫស",
                    lines=5,
                    interactive=False,
                    show_copy_button=True,
                    placeholder="ដំណើរការអត្ថបទដើម្បីមើលលទ្ធផលនៅទីនេះ...",
                )
                results_table = gr.Dataframe(
                    headers=["#", "ពាក្យ", "ពាក្យឫស", "ប្តូរ?"],
                    datatype=["number", "str", "str", "str"],
                    value=None,
                    interactive=False,
                    wrap=True,
                    label="លទ្ធផល",
                    elem_id="results_table"
                )

        process_btn.click(fn=run_pipeline, inputs=text_input, outputs=[results_table, stats_panel, combined_output])
        sample_btn.click(
            fn=lambda: (SAMPLE_TEXT, *run_pipeline(SAMPLE_TEXT)),
            inputs=None,
            outputs=[text_input, results_table, stats_panel, combined_output],
        )
        clear_btn.click(
            fn=clear_inputs,
            inputs=None,
            outputs=[text_input, results_table, stats_panel, combined_output],
            js="() => { const table = document.getElementById('results_table'); if (table) { const inputs = table.querySelectorAll('input[type=\"text\"]'); inputs.forEach(input => input.value = ''); } }"
        )

        gr.Markdown("---")
        gr.HTML(
            f"""
            <div style="margin-top: 2rem; padding: 20px; background: var(--background-fill-secondary); border-radius: 12px;">
              <h2 style="margin-top: 0;">ប្រភពវចនានុក្រម</h2>
              <p style="font-size: 1rem; margin: 12px 0;">
                <strong>ប្រភព:</strong> Teacher Vatha -
                <a href="https://youtu.be/mfWl3fV7oMo?si=OuR45gnDqeml2oXw" target="_blank" style="color: var(--link-text-color); text-decoration: underline;">
                  ១០០០ពាក្យកម្លាយដោយផ្នត់ដើម (YouTube)
                </a>
              </p>
              <p style="font-size: 1rem; margin: 12px 0;">
                <strong>ចំនួនពាក្យក្នុងប្រព័ន្ធបច្ចុប្បន្ន:</strong> {len(LEMMA_DICT):,} ពាក្យ
              </p>
            </div>
            """
        )

        dict_entries = [[i + 1, derived, root] for i, (derived, root) in enumerate(sorted(LEMMA_DICT.items()))]
        gr.Dataframe(
            headers=["#", "ពាក្យកម្លាយ", "ពាក្យឫស"],
            value=dict_entries,
            datatype=["number", "str", "str"],
            interactive=False,
            wrap=True,
            label="វចនានុក្រមពាក្យកម្លាយ និងពាក្យឫស",
        )

        gr.Markdown("---")
        gr.HTML(
            """
            <div style="text-align: center; padding: 20px; margin-top: 1rem;">
              <p style="font-size: 0.9rem; color: var(--body-text-color-subdued, #64748b);">
                <strong>រចនាដោយ:</strong>
                <a href="https://phorknorak.vercel.app/" target="_blank" style="color: var(--link-text-color); text-decoration: none; font-weight: 500;">Phork Norak</a>,
                <a href="https://povketya.github.io/ketyanhor/" target="_blank" style="color: var(--link-text-color); text-decoration: none; font-weight: 500;">Nhor Povketya</a>,
                <a href="https://final-portfolio-kappa-rust.vercel.app/" target="_blank" style="color: var(--link-text-color); text-decoration: none; font-weight: 500;">Ly Hor</a>
                <br><strong>ទីប្រឹក្សា:</strong>
                <a href="https://cadt.edu.kh/team/chamroeun-khim-phd/" target="_blank" style="color: var(--link-text-color); text-decoration: none; font-weight: 500;">Dr. Khim Chomrouen</a>,
                <a href="https://www.researchgate.net/profile/Makara-Mao" target="_blank" style="color: var(--link-text-color); text-decoration: none; font-weight: 500;">Dr. Mao Makara</a>
              </p>
            </div>
            """
        )

    return demo


LEMMA_DICT = load_dictionary()
demo = build_interface()

if __name__ == "__main__":
    demo.launch()
