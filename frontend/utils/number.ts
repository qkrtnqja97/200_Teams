/**
 * 0~1 사이의 값을 백분율로 변환하고 소수점 자리수까지 숫자로 반환
 * @param value 0~1 범위의 숫자
 * @param decimals 소수점 자리수 (기본 2)
 * @returns 12.34 같은 숫자
 */
export function toPercent(value: number, decimals = 2): number {
  const factor = Math.pow(10, decimals);
  return Math.round(value * 100 * factor) / factor;
}
