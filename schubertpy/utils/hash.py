from functools import lru_cache, wraps

def hashable_lru_cache(maxsize=128, typed=False):
    def decorator(func):
        # Create a cached version of the original function with lru_cache
        cached_func = lru_cache(maxsize=maxsize, typed=typed)(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Convert all list arguments to tuples so they are hashable
            hashable_args = tuple(tuple(arg) if isinstance(arg, list) else arg for arg in args)
            hashable_kwargs = {k: tuple(v) if isinstance(v, list) else v for k, v in kwargs.items()}
            # Call the cached function with the hashable arguments
            return cached_func(*hashable_args, **hashable_kwargs)
        
        return wrapper
    return decorator