def add(a: int, b: int) -> int:
    return a+b

def subtract(a: int, b: int) -> int:
    return b-a

def multiply(a: int, b: int) -> int:
    return a*b

def divide(a: int, b: int) -> int:
    return b // a

# 함수들을 테스트할 함수 만들어야 한다.
# assert 키워드는 왼쪽에 있는 값이 오른쪽에 있는 처리 결과와 일치하는지 검증할 때 사용

def test_add() -> None:
    assert add(1,1)==2

def test_subtract() -> None:
    assert subtract(2,5) == 3

def test_multiply() -> None:
    assert multiply(10,10) == 100

def test_divide() -> None:
    assert divide(25,100) == 4