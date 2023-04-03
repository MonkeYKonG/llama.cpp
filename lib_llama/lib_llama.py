import ctypes
import pathlib

from .c_types import LLaMAContextParams

libname = pathlib.Path().absolute() / 'libllama.so'
c_lib = ctypes.CDLL(libname)

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

c_lib.llama_token_eos.restype = ctypes.c_int
c_lib.llama_token_eos.argtypes = []
