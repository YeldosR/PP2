import re


# 1
def match_ab_star(text):
    pattern = r"ab*"
    return re.findall(pattern, text)


# 2
def match_ab_2_3(text):
    pattern = r"ab{2,3}"
    return re.findall(pattern, text)


# 3
def find_lowercase_underscore(text):
    pattern = r"[a-z]+_[a-z]+"
    return re.findall(pattern, text)


# 4
def find_upper_lower(text):
    pattern = r"[A-Z][a-z]+"
    return re.findall(pattern, text)


# 5
def match_a_any_b(text):
    pattern = r"a.*b"
    return re.findall(pattern, text)


# 6
def replace_symbols(text):
    pattern = r"[ ,.]"
    return re.sub(pattern, ":", text)


# 7
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)


# 8
def split_at_uppercase(text):
    return re.split(r"(?=[A-Z])", text)


# 9
def insert_spaces(text):
    return re.sub(r"([A-Z])", r" \1", text).strip()


# 10
def camel_to_snake(text):
    return re.sub(r"([A-Z])", r"_\1", text).lower()


#
if __name__ == "__main__":
    text = "a ab abb abbb abbbb"
    print("1:", match_ab_star(text))
    print("2:", match_ab_2_3(text))

    text2 = "hello_world test_case example_text"
    print("3:", find_lowercase_underscore(text2))

    text3 = "Hello World Test Regex"
    print("4:", find_upper_lower(text3))

    text4 = "a123b axxb a--b"
    print("5:", match_a_any_b(text4))

    text5 = "Hello, world. Python is cool"
    print("6:", replace_symbols(text5))

    print("7:", snake_to_camel("hello_world_test"))

    print("8:", split_at_uppercase("HelloWorldTest"))

    print("9:", insert_spaces("HelloWorldTest"))

    print("10:", camel_to_snake("helloWorldTest"))