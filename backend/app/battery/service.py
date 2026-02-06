# backend/app/battery/service.py

THRESHOLDS = [
    (0.1, 3),  # danger
    (0.2, 2),  # warning
    (0.3, 1),  # notice
]


def calc_rul_status(rul: float) -> int:
    """
    RUL 값에 따라 상태 코드를 계산한다.

    0: 정상
    1: 주의
    2: 경고
    3: 위험
    """
    for threshold, status in THRESHOLDS:
        if rul <= threshold:
            return status
    return 0
