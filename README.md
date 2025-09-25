# Urdu → Roman Urdu NMT (Seq2Seq, BiLSTM→LSTM)

**Authors:** Nimra Haq & Ayesha Asad  

## 📌 Overview
We built a Neural Machine Translation system that converts Urdu poetry (from Rekhta ghazals) into Roman Urdu using:
- Preprocessing + cleaning  
- SentencePiece BPE tokenization  
- Seq2Seq with BiLSTM encoder & LSTM decoder  

## 📊 Dataset
- Source: Rekhta ghazals (30 poets)  
- Final aligned pairs: **21,003**  
  - Train: 10,501  
  - Val: 5,251  
  - Test: 5,251  

## 🔤 Tokenization
- SentencePiece BPE  
- Vocab size: 16,000  
- Urdu uses `<EOS>`; Roman uses `<SOS>` + `<EOS>`  

## 🧠 Model
- Encoder: 2-layer BiLSTM  
- Decoder: 4-layer LSTM  
- Optimizer: Adam  
- Loss: CrossEntropy (ignore `<PAD>`)  

## 🚀 Usage
```bash
# Preprocess data
python preprocess.py

# Train BPE & encode
python bpe_tokenizer.py

# Verify
python verify_dataset.py
python verify_bpe_size.py
python verify_bpe_lengths.py

# Train model
python train_seq2seq.py --epochs 10 --emb 256 --hid 512 --batch 64
