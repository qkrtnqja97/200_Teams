export default function RulDonut({ value }: { value: number }) {
  const valueColor =
    value > 50 ? '#22c55e' : value > 20 ? '#eab308' : '#ef4444';
  const valueText = value > 50 ? '안정적' : value > 20 ? '주의' : '위험';
  return (
    <div className='relative w-30 h-30'>
      <svg viewBox='0 0 36 36' className='-rotate-y-180'>
        <path
          d='M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32'
          fill='none'
          stroke='#0b1a12'
          strokeWidth='4'
        />
        <path
          d='M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32'
          fill='none'
          stroke={valueColor}
          strokeWidth='3'
          strokeDasharray={`${value}, 100`}
        />
      </svg>
      <div className='absolute inset-0 flex flex-col items-center justify-center'>
        <span className='text-lg font-bold'>{valueText}</span>
        <span className='text-xs text-zinc-300'>RUL</span>
      </div>
    </div>
  );
}
