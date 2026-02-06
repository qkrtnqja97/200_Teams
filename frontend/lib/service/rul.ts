import { apiRequest, ApiResponse } from '../request';

export type BatteryRULResponse = {
  battery_id: number;
  battery_rul_id: number;
  upload_id: number;
  rul: number;
  model?: string;
  model_version?: string;
  sequence_length?: number;
  feature_count?: number;
  latency_ms?: number;
  inference_time?: number;
  rul_status: string;
  created_at: string;
};

export async function getBatteryRUL(
  battery_id: number,
  token: string,
  upload_id: number,
): Promise<ApiResponse<BatteryRULResponse[]>> {
  return apiRequest<BatteryRULResponse[]>(
    `/batteries/${battery_id}/uploads/${upload_id}/rul`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    },
  );
}
