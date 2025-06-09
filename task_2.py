def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound_val = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2
# якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1
# якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            upper_bound_val = arr[mid]
            high = mid - 1
# якщо x присутній на позиції і повертаємо його (це і є верхня межа)
        else:
            upper_bound_val = arr[mid]
        return (iterations, upper_bound_val)

    if low < len(arr):
        upper_bound_val = arr[low]
    else:
        upper_bound_val = None
    return (iterations, upper_bound_val)

# Тестування бінарного пошуку для масиву
arr = [0.9, 2.2, 4.5, 7.7, 9.9, 11.11, 13.13, 16.6, 19.19, 21.21, 23.3]

print("Масив для тестування:", arr)

print("\n--- Тестування для існуючих елементів ---")
for x in arr:
    iterations, upper_bound = binary_search(arr, x)
    print(f"x={x}: Кількість ітерацій {iterations}. Верхня межа {upper_bound}")

print("\n--- Тестування для неіснуючих елементів ---")
x_not_in_arr = [0.5, 6.0, 10.0, 17.0, 24.0, 25.5]
for x in x_not_in_arr:
    iterations, upper_bound = binary_search(arr, x)
    print(f"x={x}: Кількість ітерацій {iterations}. Верхня межа {upper_bound}")

print("\n--- Тестування для порожнього масиву ---")
iterations, upper_bound = binary_search([], 5.0)
print(f"x=5.0 (порожній масив): Кількість ітерацій {iterations}. Верхня межа {upper_bound}")

print("\n--- Тестування для масиву з одним елементом ---")
iterations, upper_bound = binary_search([15.5], 10.0)
print(f"x=10.0 ([15.5]): Кількість ітерацій {iterations}. Верхня межа {upper_bound}")
iterations, upper_bound = binary_search([15.5], 15.5)
print(f"x=15.5 ([15.5]): Кількість ітерацій {iterations}. Верхня межа {upper_bound}")
iterations, upper_bound = binary_search([15.5], 20.0)
print(f"x=20.0 ([15.5]): Кількість ітерацій {iterations}. Верхня межа {upper_bound}")
