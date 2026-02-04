# backend/app/battery/router.py

from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.db.models import (
    Battery,
    BatteryCycle,
    BatteryFileUpload,
    User,
)
from app.auth.dependencies import get_current_user
from app.battery.schemas import (
    BatteryCreateRequest,
    BatteryResponse,
    BatteryCycleCreate,
    BatteryCycleResponse,
    BatteryFileUploadResponse,
    RULCheckResponse,
)
from app.utils.storage import ensure_battery_dir, build_filename
from app.utils.ml_client import predict_rul
from app.battery.service import calc_rul_status

router = APIRouter(tags=["Battery"])


# ====================
# Battery
# ====================
@router.post("", response_model=BatteryResponse, status_code=201)
def create_battery(
    data: BatteryCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    battery = Battery(
        user_id=current_user.id,
        battery_name=data.battery_name,
        has_data=False,
    )
    db.add(battery)
    db.commit()
    db.refresh(battery)
    return battery


@router.get("", response_model=List[BatteryResponse])
def list_batteries(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Battery)
        .filter(Battery.user_id == current_user.id)
        .order_by(Battery.created_at.desc())
        .all()
    )


# ====================
# Battery Cycle
# ====================
@router.post(
    "/{battery_id}/cycles",
    response_model=BatteryCycleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_battery_cycle(
    battery_id: int,
    data: BatteryCycleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    battery = (
        db.query(Battery)
        .filter(
            Battery.id == battery_id,
            Battery.user_id == current_user.id,
        )
        .first()
    )
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    cycle = BatteryCycle(
        battery_id=battery.id,
        cycle_index=data.cycle_index,
        features=data.features,
    )
    db.add(cycle)

    if not battery.has_data:
        battery.has_data = True

    db.commit()
    db.refresh(cycle)
    return cycle


@router.get(
    "/{battery_id}/cycles",
    response_model=List[BatteryCycleResponse],
)
def list_battery_cycles(
    battery_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    battery = (
        db.query(Battery)
        .filter(
            Battery.id == battery_id,
            Battery.user_id == current_user.id,
        )
        .first()
    )
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    return (
        db.query(BatteryCycle)
        .filter(BatteryCycle.battery_id == battery_id)
        .order_by(BatteryCycle.cycle_index)
        .all()
    )


# ====================
# CSV Upload
# ====================
@router.post(
    "/uploads",
    response_model=BatteryFileUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_battery_file(
    battery_name: str = Form(...),
    battery_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    battery = get_or_create_battery(db, current_user.id, battery_name)

    raw_dir = ensure_battery_dir(current_user.id, battery_name)
    filename, ext = build_filename(battery_file.filename or "upload.csv")
    save_path = raw_dir / filename

    total = 0
    try:
        with open(save_path, "wb") as f:
            while True:
                chunk = await battery_file.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                total += len(chunk)
    finally:
        await battery_file.close()

    upload = BatteryFileUpload(
        battery_id=battery.id,
        user_id=current_user.id,
        original_filename=battery_file.filename or "unknown",
        stored_path=str(save_path),
        file_ext=ext,
        file_size=total,
    )
    db.add(upload)

    if not battery.has_data:
        battery.has_data = True

    db.commit()
    db.refresh(upload)
    return upload


# ====================
# RUL Prediction (TEMPORARY)
# ====================
@router.post(
    "/{battery_id}/rul",
    response_model=RULCheckResponse,
)
def predict_battery_rul(
    battery_id: int,
    csv_path: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    NOTE:
    - CSV 경로 기반 RUL 예측은 임시 API
    - 추후 cycle / feature 기반 예측으로 대체 예정
    """

    battery = (
        db.query(Battery)
        .filter(
            Battery.id == battery_id,
            Battery.user_id == current_user.id,
        )
        .first()
    )
    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    if not csv_path.startswith("/backendWorkspace/data"):
        raise HTTPException(
            status_code=400,
            detail="Invalid csv_path",
        )

    ml_csv_path = csv_path.replace(
        "/backendWorkspace/data",
        "/mlWorkspace/data",
        1,
    )

    result = predict_rul(ml_csv_path)

    if "rul" not in result:
        raise HTTPException(
            status_code=500,
            detail="Invalid ML response",
        )

    rul = float(result["rul"])
    rul_status = calc_rul_status(rul)

    return {
        "battery_id": battery_id,
        "rul": rul,
        "rul_status": rul_status,
    }


# ====================
# Internal Utils
# ====================
def get_or_create_battery(
    db: Session,
    user_id: int,
    battery_name: str,
) -> Battery:
    battery = (
        db.query(Battery)
        .filter(
            Battery.user_id == user_id,
            Battery.battery_name == battery_name,
        )
        .first()
    )
    if battery:
        return battery

    battery = Battery(
        user_id=user_id,
        battery_name=battery_name,
        has_data=False,
    )
    db.add(battery)
    db.commit()
    db.refresh(battery)
    return battery
