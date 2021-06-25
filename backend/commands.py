from concurrent.futures import ThreadPoolExecutor, as_completed


def load_klines(pairs, callback=None, workers=5):
    with ThreadPoolExecutor(max_workers=workers) as e:
        futures = {e.submit(pair.get_klines): pair for pair in pairs}
        for i, future in enumerate(as_completed(futures)):
            if callback:
                callback(i, futures[future])
