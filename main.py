"""Алгоритмическая обработка числового ряда дебитов скважины (вариант А)."""
WINDOW_SIZE = 3 # ширина окна скользящей средней (суток)
def generate_rate_series(student_n: int) -> list[float]:
    """Формирует индивидуальный ряд из 10 суточных замеров дебита по номеру N."""
    base = 40.0 + 2.0 * student_n
    step = float((student_n % 5) + 1)
    offsets = [0.0, 2.0, -1.0, 3.0, 0.0, 1.0, 4.0, 2.0, -2.0, 5.0]
    series: list[float] = []
    for k in offsets:
        series.append(round(base + k * step, 2))
    return series
def calc_mean(series: list[float]) -> float:
    """Вычисляет среднее арифметическое числового ряда."""
    if len(series) == 0:
        raise ValueError("Нельзя вычислить среднее для пустого списка")
    total = 0.0
    for val in series:
        total += val
    return total / len(series)
def calc_median(series: list[float]) -> float:
    """Вычисляет медиану ряда (работает для чётной и нечётной длины)."""
    n = len(series)
    if n == 0:
        raise ValueError("Нельзя вычислить медиану для пустого списка")
    ordered = sorted(series) # создаём отсортированную копию, не ломая хронологию!
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    else:
        return (ordered[mid - 1] + ordered[mid]) / 2.0
def calc_range(series: list[float]) -> tuple[float, float, float]:
    """Возвращает кортеж (минимум, максимум, размах вариации) без встроенных min/max."""
    if len(series) == 0:
        raise ValueError("Пустой список")
    min_val = series[0]
    max_val = series[0]
    for val in series[1:]:
        if val < min_val:
            min_val = val
        if val > max_val:
            max_val = val
    return min_val, max_val, max_val - min_val
def calc_moving_average(series: list[float], window: int) -> list[float]:
    """Вычисляет простую скользящую среднюю (SMA) с окном window."""
    if window <= 0 or window > len(series):
        raise ValueError(f"Некорректный размер окна: {window}")
    sma_values: list[float] = []
    # Количество положений окна равно len(series) - window + 1
    for i in range(len(series) - window + 1):
        window_slice = series[i : i + window]
        avg = calc_mean(window_slice)
        sma_values.append(round(avg, 2))
    return sma_values
def main() -> None:
    print("АЛГОРИТМИЧЕСКАЯ ОБРАБОТКА РЯДА ДЕБИТОВ СКВАЖИНЫ")
    print("=" * 54)
    raw_n = input("Введите ваш номер по журналу N: ").strip()
    student_n = int(raw_n) if raw_n.isdigit() and int(raw_n) > 0 else 5
    rates = generate_rate_series(student_n)
    mean_val = calc_mean(rates)
    median_val = calc_median(rates)
    min_v, max_v, range_v = calc_range(rates)
    sma_list = calc_moving_average(rates, WINDOW_SIZE)
    print(f"\nИсходный ряд (10 суток): {rates}")
    print(f"Отсортированный ряд: {sorted(rates)}")
    print("\nСТАТИСТИЧЕСКИЕ ПОКАЗАТЕЛИ РЯДА")
    print("-" * 54)
    print(f"Среднее арифметическое: {mean_val:8.2f} м³/сут")
    print(f"Медиана ряда: {median_val:8.2f} м³/сут")
    print(f"Минимум / Максимум: {min_v:8.2f} / {max_v:.2f} м³/сут")
    print(f"Размах вариации R: {range_v:8.2f} м³/сут")
    print(f"\nТАБЛИЦА СГЛАЖИВАНИЯ (Скользящая средняя SMA, окно k = {WINDOW_SIZE})")
    print("-" * 54)
    print(f"{'Сутки':<8}{'Факт Q, м³/сут':>16}{'Окно среза':>16}{'SMA(3), м³/сут':>14}")
    print("-" * 54)
    for idx, q_val in enumerate(rates):
        day = idx + 1
    if day < WINDOW_SIZE:
        print(f"{day:<8}{q_val:>16.2f}{'—':>16}{'— (накопление)':>14}")
    else:
        sma_idx = idx - WINDOW_SIZE + 1
        win_str = f"[{day - 2}..{day}]"
        print(f"{day:<8}{q_val:>16.2f}{win_str:>16}{sma_list[sma_idx]:>14.2f}")
if __name__ == "__main__":
    main()
