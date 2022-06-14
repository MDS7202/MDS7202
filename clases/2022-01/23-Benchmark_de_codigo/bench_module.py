

def benchmark_sum(n):
    """Funcion de referencia que suma n elementos transformados"""
    ac = []

    for i in range(n):
        to_sum = [(j // 2) ** n + (j - n) ** (n // 3) for j in range(n)]
        sum_ = sum(to_sum)
        ac.append(sum_)

    return ac
