import streamlit as st
from detoxify import Detoxify
from transformers.pipelines import pipeline
import subprocess
import torch
# Initialize Detoxify model and rewriter (acts as discriminator)
detox_model = Detoxify('original', device='cpu')


#discriminator_model = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_ollama(prompt):
    result = subprocess.run(
        ['ollama', 'run', 'my-model', prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    if result.returncode != 0:
        raise RuntimeError(f"Ollama CLI error: {result.stderr}")
    return result.stdout.strip()

def is_toxic(text, threshold=0.001):
    scores = detox_model.predict(text)
    toxic_flags = (
        scores['toxicity'] > threshold or
        scores['severe_toxicity'] > threshold or
        scores['obscene'] > threshold or
        scores['insult'] > threshold or
        scores['identity_attack'] > threshold
    )
    return toxic_flags

def is_refusal(text):
    refusal_phrases = [ "I can't provide", "I'm not able", "as an AI", "I'm sorry", "not appropriate","I can't complete"
    ]
    return any(phrase.lower() in text.lower() for phrase in refusal_phrases)

def prompt_rewrites(original_prompt):
    discriminator_prompt = (
        f"Please revise the following input to ensure it avoids stereotypes or bias, and reframe it as an open-ended, respectful question that encourages inclusive and fact-based discussion where bias can be decreased in the discussion:\n"
        f"{original_prompt}\n Only provide one revised version.and just mention the prompt don't need any explanation"
    )

    result = generate_ollama(discriminator_prompt)
    return result

def apply_reward_policy(original_output, rewritten_output):
    if is_toxic(original_output):
        if is_toxic(rewritten_output):
            return -2.0
        elif is_refusal(rewritten_output):
            return -1.0
        else:
            return 0.0
    elif is_refusal(original_output):
        if is_toxic(rewritten_output):
            return -1.0
        elif is_refusal(rewritten_output):
            return 0.0
        else:
            return 1.0
    else:
        return 2.0
        

def debias_ollama_output(prompt):
    raw_output = generate_ollama(prompt)
    toxicity = detox_model.predict(raw_output)
    if is_toxic(raw_output) or is_refusal(raw_output) :
        print("LLLLL")
        rewritten_prompt = prompt_rewrites(prompt)
        clean_output = generate_ollama(rewritten_prompt)
        reward = apply_reward_policy(raw_output, clean_output)
        debiased_toxicity = detox_model.predict(clean_output)
        return clean_output, reward, rewritten_prompt, raw_output, debiased_toxicity, toxicity
    else:
        return raw_output, 2.0, None, None, toxicity,None


# Streamlit UI
st.title("Bias and Toxicity Mitigation for LLM Outputs")
user_prompt = st.text_area("Enter your prompt below:")

if st.button("Generate Debiased Output"):
    if user_prompt.strip() == "":
        st.warning("Please enter a prompt first.")
    else:
        with st.spinner("Processing..."):
            try:
                output, reward, rewritten_prompt, raw_output, debiased_toxicity, biased_toxicity = debias_ollama_output(user_prompt)
                st.subheader("Debiased Output:")
                st.success(output)
                st.markdown(f"**Reward Score:** `{reward}`")
                if biased_toxicity:
                    st.markdown(f"**Toxicity Scores for Biased Output:** `{biased_toxicity}`")
                st.markdown(f"**Toxicity Scores for Debiased Output:** `{debiased_toxicity}`")
                if rewritten_prompt:
                    st.markdown("---")
                    st.subheader("Detected Toxic Content")
                    st.text_area("Original Output", raw_output, height=100)
                    st.subheader("Rewritten Prompt")
                    st.text_area("Rewritten Prompt", rewritten_prompt, height=100)
            except Exception as e:
                st.error(f"Error: {str(e)}")
