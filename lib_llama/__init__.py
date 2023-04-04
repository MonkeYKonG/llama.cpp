import ctypes

from .c_types import LLaMAContextParams, to_c_array
from .lib_llama import c_lib


class ModelContext:
    def __init__(self, model_context_ptr):
        self._model_context_ptr = model_context_ptr

    @staticmethod
    def init_from_file(file_path: str, params: LLaMAContextParams):
        model_context_ptr = c_lib.llama_init_from_file(file_path.encode(), params)
        return ModelContext(model_context_ptr)

    @staticmethod
    def eof_token():
        return c_lib.llama_token_eos()
    
    def free(self):
        c_lib.llama_free(self._model_context_ptr)

    def tokenize(self, text: str, new_line: bool = True):
        n_ctx = c_lib.llama_n_ctx(self._model_context_ptr)
        buffer = (ctypes.c_int * n_ctx)()
        size = c_lib.llama_tokenize(
            self._model_context_ptr,
            text.encode(),
            buffer,
            n_ctx,
            new_line,
        )
        return buffer[:size]

    def token_to_str(self, token_id: int):
        return c_lib.llama_token_to_str(self._model_context_ptr, token_id).decode('utf-8')

    def eval(self, tokens: list, n_past: int, n_thread: int):
        c_array_tokens = to_c_array(tokens, ctypes.c_int)
        eval_result = c_lib.llama_eval(
            self._model_context_ptr,
            c_array_tokens,
            len(tokens),
            n_past,
            n_thread,
        )
        if eval_result != 0:
            raise ValueError('Eval fail')

    def get_predicted_token(self, last_n_tokens: list):
        c_array_tokens = to_c_array(last_n_tokens, ctypes.c_int)
        return c_lib.llama_sample_top_p_top_k(
            self._model_context_ptr,
            c_array_tokens,
            len(last_n_tokens),
            40,
            0.95,
            0.8,
            1.1,
        )

    def get_logits(self):
        return c_lib.llama_get_logits(self._model_context_ptr)
    
    def get_n_ctx(self):
        return c_lib.llama_n_ctx(self._model_context_ptr)
