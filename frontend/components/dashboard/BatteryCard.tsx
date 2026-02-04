import Link from 'next/link';

export default function BatteryCard({
  id,
  title,
  checked,
  rul,
}: {
  id: number;
  title: string;
  checked: string;
  rul: number;
}) {
  return (
    <div className='bg-green-900/20 rounded-3xl p-5 flex justify-between items-center shadow'>
      <div>
        <h3 className='font-bold text-lg flex items-center gap-2'>
          <span className='w-2 h-2 bg-green-400 rounded-full' />
          {title}
        </h3>
        <p className='text-xs text-zinc-300 mt-1'>최근 점검 {checked}</p>
      </div>

      <div className='flex flex-col items-center gap-4'>
        {/* TODO: get/batteries 에서 RUL 값 받아올 경우 표시 */}
        {/* <Circle value={rul} /> */}
        <Link href={`/analysis/${id}`}>
          <button className='bg-green-400 text-black px-5 py-2 rounded-full text-sm font-bold cursor-pointer'>
            상세 분석
          </button>
        </Link>
      </div>
    </div>
  );
}

function Circle({ value }: { value: number }) {
  const valueColor =
    value > 50 ? '#22c55e' : value > 20 ? '#eab308' : '#ef4444';
  return (
    <div className='relative w-20 h-20'>
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
        <span className='text-lg font-bold'>{value}%</span>
        <span className='text-xs text-zinc-300'>RUL</span>
      </div>
    </div>
  );
}
