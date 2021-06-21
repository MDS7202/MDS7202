

def benchmark_sum(n):
    """Funcion de referencia que suma n elementos transformados
    """
    ac = []

    for i in range(n):
        to_sum = [(i // 2) ** n + (i - n) ** (n // 3) for i in range(n)]
        sum_ = sum(to_sum)
        ac.append(sum_)

    return ac
