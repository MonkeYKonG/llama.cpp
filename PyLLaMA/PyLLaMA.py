import ctypes

import lib_llama


class PyLLaMA:
    def __init__(
            self, 
            model_path, 
            n_ctx=512, 
            last_token_count=64,
            max_generation=512,
            eval_thread_count=4,
            header_text=None,
            prefix=None,
        ):
        self._model_path = model_path
        self.model_context = lib_llama.ModelContext.init_from_file(
            self._model_path,
            lib_llama.c_types.get_default_llama_context(n_ctx=n_ctx)
        )
        self.n_ctx = self.model_context.get_n_ctx()
        self.eof_token = self.model_context.eof_token()

        self.last_token_count = last_token_count
        self.last_token = [0] * self.last_token_count
        self.n_past = 0
        self.n_keep = 0
        self.max_generation = max_generation
        self.eval_thread_count = eval_thread_count
        self.header_text = header_text
        self.prefix = prefix
        self.prompt = None
        self.text = ''

        self._initialize_header()
        self._initialize_prefix()

    def __del__(self):
        self.model_context.free()

    def _prepare_initial_prompt(self):
        initial_text = self.header_text + '\n' + self.prefix
        self.prompt = self.model_context.tokenize(initial_text, new_line=True)

    def _evaluate(self):
        self.model_context.eval(
            self.prompt, 
            self.n_past, 
            self.eval_thread_count,
        )
        prompt_size = len(self.prompt)
        self.n_past += prompt_size
        self.last_token[:] = self.last_token[prompt_size:] + self.prompt
        self.prompt = None

    def _generate(self):
        return self.model_context.get_predicted_token(
            self.last_token,
        )
    
    def _initialize_header(self):
        self.prompt = self.model_context.tokenize(self.header_text or ' ')
        self.n_keep = len(self.prompt)
        self._evaluate()

    def _initialize_prefix(self):
        if self.prefix:
            prefix = self.prefix if self.header_text is None else f'\n\n{self.prefix}'
            self.prompt = self.model_context.tokenize(prefix,new_line=False)
            self._evaluate()
            self.text += prefix

    def predict_next(self):
        self.prompt and self._evaluate()
        token_id = self._generate()
        if token_id == self.eof_token:
            return None
        self.prompt = [token_id]
        next_str = self.model_context.token_to_str(token_id)
        self.text += next_str
        return next_str
