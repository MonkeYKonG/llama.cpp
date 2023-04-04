from PyLLaMA.PyLLaMA import PyLLaMA

header = "Transcript of a dialog, where the User interacts with an Assistant named Bob. Bob is helpful, kind, honest, good at writing, and never fails to answer the User's requests immediately and with precision."

prefix = """User: Hello, Bob.
Bob: Hello. How may I help you today?
User: Please tell me how to declare a string variable in python
Bob:"""

if __name__ == "__main__":
    llama = PyLLaMA(
        # model_path='models/13B/ggml-model-q4_0.bin',
        model_path='models/GPT4All/gpt4all-lora-quantized-new.bin',
        n_ctx=256,
        header_text=header,
        prefix=prefix,
    )
    n_remains = 128
    print(llama.header_text)
    print(llama.prefix)
    while n_remains > 0:
        next_str = llama.predict_next()
        if next_str is None:
            break
        print(next_str, end='', flush=True)
        n_remains -= 1
