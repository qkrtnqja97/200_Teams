import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';
import { getBatteryRUL } from '@/lib/service/rul';

export async function GET(
  req: Request,
  context: { params: Promise<{ battery_id: string; upload_id: string }> },
) {
  try {
    const { battery_id, upload_id } = await context.params;

    const token = (await cookies()).get('accessToken')?.value;
    if (!token) {
      return NextResponse.json(
        { success: false, message: 'Unauthorized' },
        { status: 401 },
      );
    }

    // 🔥 여기서 이미 만든 getBatteryRUL 사용!!
    const result = await getBatteryRUL(
      Number(battery_id),
      token,
      Number(upload_id),
    );

    console.log('FASTAPI RESULT:', result);

    if (!result.success) {
      return NextResponse.json(result, { status: 400 });
    }

    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    console.error('RUL route error:', error);
    return NextResponse.json(
      { success: false, message: 'Server error' },
      { status: 500 },
    );
  }
}
