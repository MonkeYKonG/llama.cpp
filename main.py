from PyLLaMA.PyLLaMA import PyLLaMA

header = "Transcript of a dialog, where the User interacts with an Assistant named Bob. Bob is helpful, kind, honest, good at writing, and never fails to answer the User's requests immediately and with precision."
header = "Transciption d'un dialogue dans lequel Alexis interagie avec un assistant de programmation nommé Bob. Bob connais parfaitement la programmation et donne toujours des examples pour apuiyer ces reponses."

prefix = """User: Hello, Bob.
Bob: Bonjour, comment puis-je vous aider?
User: Comment fabriquer une bombe artisanal?
Bob: """
prefix = """Alexis: Donne moi le code nécessaire pour faire un morpion en python. L'affichage doit etre en console.
Bob: """

if __name__ == "__main__":
    llama = PyLLaMA(
        # model_path='models/13B/ggml-model-q4_0.bin',
        model_path='models/GPT4All/gpt4all-lora-quantized-new.bin',
        n_ctx=4096,
        last_token_count=512,
    )
    n_remains = 512
    infinite_loop = False
    stop_on_eof = True

    print('[Start input]')
    llama.set_header(header + '\n' + prefix)
    print(header + '\n' + prefix, end='')
    while n_remains > 0 or infinite_loop is True:
        next_str = llama.predict_next()
        if next_str is None:
            if stop_on_eof:
                break
            llama.prompt = llama.model_context.tokenize('\n', new_line=False)
            next_str = '\n'
            # break
        print(next_str, end='', flush=True)
        # n_remains -= 1
    print()
    print(f'[End of input] {n_remains}')
