'use client';

import { useMemo, useState, useEffect } from 'react';
import MetricCard from '@/components/analysis/MetricCard';
import SOHTrendChart from '@/components/analysis/SOHTrendChart';
import UploadSelect from '@/components/analysis/UploadSelect';
import { CyclePoint } from '@/components/analysis/cycle/parseCsv';
import { useBatteryUploadSeries } from '@/hook/useBatteryUploadSeries';
import { toPercent } from '@/utils/number';
import RulDonut from './RulDont';

function computeMetrics(_series: CyclePoint[]) {
  return {
    soh: 92.4,
    sohDelta: +0.2,
    re: '42.8 mΩ',
    rct: '15.2 mΩ',
    capFade: '7.6 %',
    thermal: '1.4 ℃',
    rulMonths: 14, // 기본값
  };
}

export default function AnalysisClient({ batteryId }: { batteryId: number }) {
  const { uploads, selectedUploadId, series, loading, err, loadUpload } =
    useBatteryUploadSeries(batteryId);

  const [rul, setRul] = useState<number | null>(null);

  // 🔥 업로드 선택되면 RUL 불러오기
  useEffect(() => {
    if (!selectedUploadId) return;

    async function fetchRUL() {
      try {
        const res = await fetch(
          `/api/batteries/${batteryId}/uploads/${selectedUploadId}/rul`,
          { method: 'GET' },
        );

        const result = await res.json();
        if (result.success && result.data) {
          setRul(result.data.rul);
        } else {
          setRul(null);
        }
      } catch (e) {
        console.error('RUL fetch 실패:', e);
      }
    }

    fetchRUL();
  }, [selectedUploadId]);

  // 🔥 metrics + rul 조합
  const metrics = useMemo(() => {
    const m = computeMetrics(series);
    return { ...m, rulMonths: rul ?? m.rulMonths };
  }, [series, rul]);

  return (
    <div className='space-y-6 pt-4'>
      <section className='flex flex-row gap-6 items-center'>
        <RulDonut value={toPercent(rul || 0)} />
        <div>
          <p className='text-3xl font-bold text-green-400'>
            {rul !== null ? `${toPercent(rul)}` : '--'}%{' '}
          </p>
          <p className='text-sm text-gray-400'>현재 배터리 성능 상태</p>
        </div>
      </section>

      <UploadSelect
        uploads={uploads}
        selectedUploadId={selectedUploadId}
        loading={loading}
        err={err}
        onPick={loadUpload}
      />

      <SOHTrendChart series={series} />

      <div className='rounded-xl bg-green-900/30 p-4 text-sm'>
        ✨ 현재의 방전 및 열화 패턴을 분석한 결과, 예상 잔여 수명(RUL)은 약{' '}
        <span className='text-green-400 font-semibold'>
          {rul !== null ? `${toPercent(rul)}%` : '--'}
        </span>
        입니다.
      </div>

      <section>
        <h2 className='font-semibold mb-3'>내부 지표 상세</h2>
        <div className='grid grid-cols-2 gap-4'>
          <MetricCard title='내부 저항 (Re)' value={metrics.re} status='정상' />
          <MetricCard
            title='전하 전달 저항 (Rct)'
            value={metrics.rct}
            status='주의'
          />
          <MetricCard
            title='용량 감소율'
            value={metrics.capFade}
            status='안정'
          />
          <MetricCard title='열적 편차' value={metrics.thermal} status='최적' />
        </div>
      </section>
    </div>
  );
}
