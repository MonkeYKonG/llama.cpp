from PyLLaMA.PyLLaMA import PyLLaMA

if __name__ == "__main__":
    llama = PyLLaMA('models/7B/ggml-model-q4_0.bin')
    llama.predict(256, """Building a website can be done in 10 simple steps:""")