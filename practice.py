# def print_strings(items):
#     count = 0

#     for item in items:
#         if isinstance(item, str):
#             print(item)
#             count += 1

#     return count

# num_strings = print_strings(["hello", 42, "world", None, 3.14])
# print(f"Total strings: {num_strings}")

# def print_long_strings(items):
#     for item in items:
#         if isinstance(item, str):
#             if len(item) >= 5:
#                 print(item)

# print_long_strings(["hi", "elephant", "chunk", 42, "moon", "monkey", None])

# def collect_long_strings(items):
#     long_strings = []
#     count = 0

#     for item in items:
#         if not isinstance(item, str):
#             print(f"Skipping non-string: {item}")
#             continue
#         if len(item) > 5:
#             print(f"Skipping short strings: '{item}'")
#             continue

#         long_strings.append(item)
#         count += 1

#     print(f"Found {count} long strings.")
#     return sorted(long_strings)

# result = collect_long_strings(["hi", "sunshine", 42, "moon", "avalanche", None])
# print(result)

# def calculator(x, op, y):
#     if op == '+':
#         return x + y
#     elif op == '-':
#         return x - y
#     elif op == '*':
#         return x * y
#     elif op == '/':
#         return x / y
#     elif op == '**':
#         return x ** y
#     elif op == '%':
#         if y == 0:
#             return "Cannot divide by zero!"
#         return x % y
#     else:
#         return "Unknown"
    
# print("Python Calculator: Type 'q' to quit.\n")

# while True:
#     x_input = input("First number: ")
#     if x_input.lower() in ['q', 'quit']:
#         break

#     op = input("Choose operation: ")
#     if op.lower() in ['q', 'quit']:
#         break

#     y_input = input("Second number: ")
#     if y_input.lower() in ['q', 'quit']:
#         break

#     try:
#         x = float(x_input)
#         y = float(y_input)
#         result = calculator(x, op, y)

#         if isinstance(result, float):
#             print(f"Result: {result:.2f}")
#         else:
#             print(result)

#     except ValueError:
#         print("Invalid number. Try again.\n")

# print("Thanks for using the calculator!")

def print_student_averages(grades):
    for name, scores in grades.items():
        average = sum(scores) / len(scores)
        print(f"{name}'s average: {average:.2f}")

grades = {
    "Alice": [90, 85, 88],
    "Bob": [72, 70, 68],
    "Charlie": [100, 100, 95]
}

print_student_averages(grades)


