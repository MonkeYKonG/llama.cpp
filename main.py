import ctypes
import pathlib
import time


class LLaMAContextParams(ctypes.Structure):
    pass


LLaMAContextParams._fields_ = [
    ('n_ctx', ctypes.c_int),
    ('n_parts', ctypes.c_int),
    ('seed', ctypes.c_int),
    ('f16_kv', ctypes.c_bool),
    ('logits_all', ctypes.c_bool),
    ('vocab_only', ctypes.c_bool),
    ('use_mlock', ctypes.c_bool),
    ('embedding', ctypes.c_bool),
    ('progress_callback', ctypes.POINTER(ctypes.CFUNCTYPE(None, ctypes.c_float, ctypes.c_void_p))),
    ('progress_callback_user_data', ctypes.c_void_p),
]


def get_default_llama_context():
    return LLaMAContextParams(
        n_ctx=512,
        n_parts=-1,
        seed=int(time.time()),
        f16_kv=True,
        logits_all=False,
        vocab_only=False,
        use_mlock=False,
        embedding=False,
        progres_callback=None,
        progress_callback_user_data=None,
    )


if __name__ == "__main__":
    a = (ctypes.c_int * 100)(*range(100))

    print(a[0])
    print(a[1])

    print(id(a[0]))
    print(id(a[1]))
    print(id(a[2]))

    exit(0)

    # Load shared library from ctypes
    libname = pathlib.Path().absolute() / 'libllama.so'
    models_path = 'models/7B/ggml-model-q4_0.bin'.encode()
    c_lib = ctypes.CDLL(libname)
    prompt = ' '
    n_keep = len(prompt) + 1

    c_lib.llama_init_from_file.restype = ctypes.c_void_p
    c_lib.llama_init_from_file.argtypes = [ctypes.c_char_p, LLaMAContextParams]

    c_lib.llama_tokenize.restype = ctypes.c_int
    c_lib.llama_tokenize.argtypes = [
        ctypes.c_void_p,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
        ctypes.c_bool,
    ]

    c_lib.llama_eval.restype = ctypes.c_int
    c_lib.llama_eval.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_int,
    ]

    c_lib.llama_n_ctx.restype = ctypes.c_int
    c_lib.llama_n_ctx.argtypes = [ctypes.c_void_p]

    c_lib.llama_token_to_str.restype = ctypes.c_char_p
    c_lib.llama_token_to_str.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int
    ]

    c_lib.llama_get_logits.restype = ctypes.POINTER(ctypes.c_float)
    c_lib.llama_get_logits.argtypes = [ctypes.c_void_p]

    c_lib.llama_sample_top_p_top_k.restype = ctypes.c_int
    c_lib.llama_sample_top_p_top_k.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_int),
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_float,
        ctypes.c_float,
        ctypes.c_float,
    ]

    model_context = c_lib.llama_init_from_file(models_path, get_default_llama_context())

    prompt_res = (ctypes.c_int * (len(prompt) + 1))()
    input_size = c_lib.llama_tokenize(model_context, prompt.encode(), prompt_res, 2, True)

    n_ctx = c_lib.llama_n_ctx(model_context)

    if input_size > n_ctx - 4:
        raise Exception('Prompt too long')

    prefix = '\n\n### Instruction:\n\n'
    suffix = '\n\n### Response:\n\n'
    input_prefix = (ctypes.c_int * (len(prefix) + 1))()
    input_suffix = (ctypes.c_int * len(suffix))()
    input_prefix_size = c_lib.llama_tokenize(model_context, prefix.encode(), input_prefix, len(prefix) + 1, True)
    input_suffix_size = c_lib.llama_tokenize(model_context, suffix.encode(), input_suffix, len(suffix), False)

    n_past = 0
    n_remains = 128
    n_consume = 0

    buffer = (ctypes.c_int * 256)(*prompt_res)
    buffer_size = 2

    py_last_n_token = [0] * 512

    is_interacting = False

    while n_remains > 0:
        last_n_token = (ctypes.c_int * 512)(*py_last_n_token)
        result = c_lib.llama_eval(model_context, buffer, buffer_size, n_past, 2)
        print('Eval ok', result)
        if result != 0:
            raise Exception('Eval fail')

        # logits = c_lib.llama_get_logits(model_context)
        token_id = c_lib.llama_sample_top_p_top_k(
            model_context,
            # ctypes.POINTER(ctypes.c_int)(ctypes.c_int(id(last_n_token[n_ctx - 64]))),
            # ctypes.POINTER(ctypes.c_int)(ctypes.c_int(id(last_n_token[n_ctx - 64]))),
            ctypes.addressof(last_n_token[n_ctx - 64]),
            64,
            40,
            0.95,
            0.8,
            1.1,
        )

        py_last_n_token.pop()
        py_last_n_token.append(token_id)

        buffer[0] = token_id
        buffer_size = 1

        token_bytes = c_lib.llama_token_to_str(model_context, token_id)

        print(f'{token_id} => {token_bytes} - {token_bytes.decode("utf-8")}')

        n_remains -= 1
