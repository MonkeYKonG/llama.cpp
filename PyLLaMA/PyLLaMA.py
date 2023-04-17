import lib_llama


class PyLLaMA:
    def __init__(
        self,
        model_path,
        n_ctx=512,
        last_token_count=64,
        max_generation=512,
        eval_thread_count=4,
    ):
        self._model_path = model_path
        self.model_context = lib_llama.ModelContext.init_from_file(
            self._model_path,
            lib_llama.c_types.get_default_llama_context(n_ctx=n_ctx)
        )
        self.n_ctx = self.model_context.get_n_ctx()
        self.eof_token = self.model_context.eof_token()

        self.last_token_count = last_token_count
        self.last_token = self._get_default_last_tokens()
        self.n_past = 0
        self.n_keep = 0
        self.max_generation = max_generation
        self.eval_thread_count = eval_thread_count
        self.prompt = None

        self.header = None
        self.instruction_prefix = None
        self.instruction_tokens = None
        self.answer_prefix = None
        self.answer_tokens = None

    def __del__(self):
        self.model_context.free()

    def _evaluate(self):
        prompt_size = len(self.prompt)

        if self.n_past + prompt_size >= self.n_ctx:
            self.prompt = self.last_token + self.prompt
            self.n_past = self.n_keep
            prompt_size = len(self.prompt)

        self.model_context.eval(
            self.prompt,
            self.n_past,
            self.eval_thread_count,
        )
        self.n_past += prompt_size
        self.last_token[:] = self.last_token[prompt_size:] + \
            self.prompt[-self.last_token_count:]
        self.prompt = None

    def _generate(self):
        return self.model_context.get_predicted_token(
            self.last_token,
        )

    def _get_default_last_tokens(self):
        return [0] * self.last_token_count

    def reset(self):
        self.n_past = self.n_keep
        self.last_token = self._get_default_last_tokens()

    def set_header(self, header: str):
        self.header = header
        self.n_past = 0
        self.prompt = self.model_context.tokenize(header)
        self.n_keep = len(self.prompt)
        self._evaluate()

    def set_configs(self, intruction_prefix: str, answer_prefix: str):
        self.instruction_prefix = intruction_prefix
        self.answer_prefix = answer_prefix
        self.instruction_tokens = self.model_context.tokenize(
            self.instruction_prefix, new_line=False)
        self.answer_tokens = self.model_context.tokenize(
            self.answer_prefix, new_line=False)

    def send_input(self, input: str):
        self.prompt = self.model_context.tokenize(
            f'\n\n{self.instruction_prefix}\n{input}\n\n{self.answer_prefix}\n',
            new_line=False,
        )
        self._evaluate()

    def predict_next(self):
        self.prompt and self._evaluate()
        token_id = self._generate()
        if token_id == self.eof_token:
            return None
        self.prompt = [token_id]
        next_str = self.model_context.token_to_str(token_id)
        return next_str
