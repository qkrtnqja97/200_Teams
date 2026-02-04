from sqlalchemy import Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base

class BatteryRUL(Base):
    __tablename__ = "battery_ruls"

    id: Mapped[int] = mapped_column(primary_key=True)

    battery_id: Mapped[int] = mapped_column(
        ForeignKey("batteries.id"),
        nullable=False,
    )

    battery_file_upload_id: Mapped[int] = mapped_column(
        ForeignKey("battery_file_uploads.id"),
        nullable=True,
    )

    rul: Mapped[float]
    rul_status: Mapped[str] = mapped_column(String(50))  # 문자열로 변경, 길이 지정

    model: Mapped[str | None] = mapped_column(String(255))  # 길이 지정
    model_version: Mapped[str | None] = mapped_column(String(50))  # 길이 지정

    sequence_length: Mapped[int | None]
    feature_count: Mapped[int | None]
    latency_ms: Mapped[int | None]

    inference_time: Mapped[datetime | None]
    raw_response: Mapped[dict | None] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
