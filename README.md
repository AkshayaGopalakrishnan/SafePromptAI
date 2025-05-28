````bash
# 💬 LLM-BiasGuard  
### A Local Framework for Bias Detection, Prompt Rewriting, and Ethical Language Generation in LLMs

**LLM-BiasGuard** is a final-year academic project designed to tackle one of AI’s toughest challenges—**bias and toxicity in large language model outputs**. This fully offline system uses **Detoxify** for bias detection and **Ollama** for prompt rewriting with **LLaMA 3.2**, offering a practical and ethical solution for safe AI deployment.

Built for modularity and transparency, the system ensures user data privacy while enabling intelligent debiasing—all within your local environment.

---

## 📌 Project Highlights

- 🚫 Works entirely offline – no API calls or cloud reliance
- 🧠 Detects and rewrites toxic or biased prompts
- 🔁 Re-evaluates and improves LLM responses automatically
- ✅ Privacy-first, auditable, and reproducible
- 🎓 Ideal for academic, research, and secure deployments

---

## 🛠 Tech Stack

| Component         | Purpose                                           |
|------------------|---------------------------------------------------|
| **Python 3.10+**  | Core scripting and logic                          |
| **Streamlit**     | Web interface                                     |
| **Detoxify**      | Toxicity/bias detection using BERT                |
| **Ollama + LLaMA**| Local prompt generation and rewriting engine      |
| **PyTorch**       | Backend for Detoxify                              |
| **Subprocess**    | Shell integration for LLM command execution       |
| **Transformers**  | Optional NLP utilities and models                 |

---

## 📥 Installation Guide

### ✅ Step 1: Set Environment & Install Dependencies

```bash
# Clone the project
git clone https://github.com/AkshayaGopalakrishnan/SafePromptAI.git
cd LLM-BiasGuard

# Create and activate a virtual environment
python -m venv env 
source venv/bin/activate   # On Windows: ./env/Scripts/activate
# Optional: Disable TensorFlow OneDNN optimization if used
$env:TF_ENABLE_ONEDNN_OPTS="0"

# Install dependencies
pip install requirements.txt
````

---

## 🦙 Step 2: Install and Configure Ollama + LLaMA

Ollama allows you to run LLMs locally with minimal setup.

```bash
# Pull the LLaMA 3.2 model from Ollama’s model registry
ollama pull llama3.2

# (Optional) Clone or backup the model with a custom name
ollama cp llama3.2 my-model

# Start the model (either llama3.2 or your custom copy)
ollama run my-model
```

> Replace `my-model` in `app.py` if you rename your model.

---

## 🚀 Step 3: Launch the Streamlit App

```bash
streamlit run app.py
```

Use the input box to enter a prompt. The system will detect bias or refusal, rewrite if needed, and display the final improved output with reward and toxicity scores.

---

## 🖼 UI Screenshots

### 📌 Interface

![UI1](assets/ui1.png)

### 📊 Output with Scores

![UI2](assets/ui2.png)

---

## 📈 Reward Evaluation Logic

| Original Output | Rewritten Output | Reward |
| --------------- | ---------------- | ------ |
| Toxic           | Toxic            | -2.0   |
| Toxic           | Refusal          | -1.0   |
| Toxic           | Neutral          | 0.0    |
| Refusal         | Toxic            | -1.0   |
| Refusal         | Refusal          | 0.0    |
| Refusal         | Neutral          | +1.0   |
| Neutral         | —                | +2.0   |

---

## 📚 Project Documentation

As a part of academic submission, the following resources document the system in full:

* 📘 [Final Report (PDF)](./finalised%20report.pdf)
* 📊 [Presentation Slides (PPTX)](./FINAL%20PROJ.pptx)

---

## 🙌 Acknowledgements

* 🧠 [Detoxify – Unitary AI](https://github.com/unitaryai/detoxify)
* 🛠 [Ollama – Local LLM Runtime](https://ollama.com)
* 📚 [Meta – LLaMA Models](https://ai.meta.com/llama/)
* 🌐 [Streamlit – UI Framework](https://streamlit.io)

---

