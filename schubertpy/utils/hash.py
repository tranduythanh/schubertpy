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

def hashable_lru_cache_method(maxsize=128, typed=False):
    def decorator(method):
        # Create a cached version of the original method with lru_cache
        cached_method = lru_cache(maxsize=maxsize, typed=typed)(method)
        
        @wraps(method)
        def wrapper(*args, **kwargs):
            # For methods, the first argument is 'self', so we skip it when converting to hashable
            if args:
                # Keep 'self' as is, convert the rest of the arguments
                self_arg = args[0]
                other_args = args[1:]
                hashable_other_args = tuple(tuple(arg) if isinstance(arg, list) else arg for arg in other_args)
                hashable_args = (self_arg,) + hashable_other_args
            else:
                hashable_args = args
                
            hashable_kwargs = {k: tuple(v) if isinstance(v, list) else v for k, v in kwargs.items()}
            # Call the cached method with the hashable arguments
            return cached_method(*hashable_args, **hashable_kwargs)
        
        return wrapper
    return decorator