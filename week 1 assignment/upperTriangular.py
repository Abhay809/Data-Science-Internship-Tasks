def upper_triangle(rows):
    for i in range(1, rows+1):
        spaces = rows - i
        stars = i
        print(" " * spaces + "*" * stars)

upper_triangle(7)