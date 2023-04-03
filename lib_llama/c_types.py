import ctypes
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


def to_c_array(entry, c_type):
    return (c_type * len(entry))(*entry)
