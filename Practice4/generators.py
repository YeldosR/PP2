def squares_up_to(n):
    for i in range(n + 1):
        yield i * i



def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i



def divisible_by_3_and_4(n):
    for i in range(0, n + 1, 12):
        yield i


def squares(a, b):
    for i in range(a, b + 1):
        yield i * i



def countdown(n):
    for i in range(n, -1, -1):
        yield i


# tests
if __name__ == "__main__":
    n = 10
    print("Squares up to:", list(squares_up_to(n)))
    print("Even:", ",".join(map(str, even_numbers(n))))
    print("Divisible:", list(divisible_by_3_and_4(n)))
    print("Squares 3..6:", list(squares(3, 6)))
    print("Countdown:", list(countdown(5)))