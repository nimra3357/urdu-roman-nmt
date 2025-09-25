import json
import sentencepiece as spm
from pathlib import Path


def build_corpus(train_path, save_dir):
    with open(train_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    corpus_file = Path(save_dir) / "corpus.txt"
    with open(corpus_file, "w", encoding="utf-8") as f:
        for ur, ro in data:
            ro_norm = ro.lower().replace("-", " ").strip()
            f.write(ur.strip() + "\n")
            f.write(ro_norm + "\n")
    return corpus_file


def train_sentencepiece(corpus_file, save_dir, vocab_size=8000):
    save_dir = Path(save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    spm.SentencePieceTrainer.Train(
        input=str(corpus_file),
        model_prefix=str(save_dir / "urdu_roman"),
        vocab_size=vocab_size,
        model_type="bpe",
        character_coverage=1.0,
        bos_id=1, eos_id=2, unk_id=3, pad_id=0
    )
    print(f"[done] SentencePiece model saved to {save_dir}")

def encode_dataset(sp, data_path, out_path):
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    encoded = []
    for ur, ro in data:
        ro_norm = ro.lower().replace("-", " ").strip()

        # Tokens (human-readable)
        ur_tokens = sp.encode(ur, out_type=str)
        ro_tokens = sp.encode(ro_norm, out_type=str)

        # IDs (for model training)
        ur_ids = sp.encode(ur, out_type=int) + [sp.eos_id()]
        ro_ids = [sp.bos_id()] + sp.encode(ro_norm, out_type=int) + [sp.eos_id()]

        encoded.append({
            "urdu_tokens": ur_tokens,
            "roman_tokens": ro_tokens,
            "urdu_ids": ur_ids,
            "roman_ids": ro_ids
        })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(encoded, f, ensure_ascii=False, indent=2)

    print(f"[done] Encoded dataset saved → {out_path}")


if __name__ == "__main__":
    data_dir = Path("data")
    bpe_dir = Path("bpe")
    bpe_dir.mkdir(exist_ok=True)

    corpus_file = build_corpus(data_dir / "train.json", bpe_dir)
    train_sentencepiece(corpus_file, bpe_dir, vocab_size=16000)

    sp = spm.SentencePieceProcessor(model_file=str(bpe_dir / "urdu_roman.model"))

    encode_dataset(sp, data_dir / "train.json", data_dir / "train_bpe.json")
    encode_dataset(sp, data_dir / "val.json", data_dir / "val_bpe.json")
    encode_dataset(sp, data_dir / "test.json", data_dir / "test_bpe.json")
