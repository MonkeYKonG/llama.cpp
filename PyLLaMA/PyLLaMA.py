import ctypes

import lib_llama


class PyLLaMA:
    def __init__(self, model_path):
        self._model_path = model_path
        self.model_context = lib_llama.ModelContext.init_from_file(
            self._model_path,
            lib_llama.c_types.get_default_llama_context()
        )

    def predict(self, max_token, default_prompt=' '):
        last_tokens = [0] * 64
        prompt = self.model_context.tokenize(default_prompt, new_line=True)
        n_past = 0
        n_remains = max_token
        generated = ''
        print('default prompt:', default_prompt)
        for p in prompt:
            token_str = self.model_context.token_to_str(p)
            generated += token_str
            print(f'{p:>5} -> \'{token_str}\'')
            last_tokens.pop()
            last_tokens.append(p)

        token_eof = self.model_context.eof_token()
        print('EOF Token', token_eof)

        print(generated, end='')


        while n_remains > 0:
            self.model_context.eval(prompt, n_past, 4)
            token_id = self.model_context.get_predicted_token(last_tokens)

            last_tokens.pop()
            last_tokens.append(token_id)
            prompt = [token_id]
            n_past += 1
            n_remains -= 1

            if token_id == token_eof:
                print('[End of File]')
                return

            token_str = self.model_context.token_to_str(token_id)
            print(token_str, end='')
