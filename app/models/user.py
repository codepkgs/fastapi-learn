from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from . import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    full_name = Column(String(100), nullable=True, comment="全名")
    email = Column(String(255), unique=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(256), nullable=False, comment="密码")
    mobile = Column(String(11), nullable=True, comment="手机号")
    is_disabled = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="是否禁用, False: 正常, True: 禁用",
    )
    created_at = Column(
        DateTime, default=datetime.now, nullable=False, comment="创建时间"
    )
    updated_at = Column(
        DateTime, default=datetime.now, nullable=False, comment="更新时间"
    )
