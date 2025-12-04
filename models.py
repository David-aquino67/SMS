from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, Date, DateTime, Boolean, ForeignKey
import datetime

class Lug(db.Model):
    __tablename__ = 'lug'
    IDELUG: Mapped[int] = mapped_column(Integer, primary_key=True)
    NOMLUG: Mapped[str] = mapped_column(String(100))
    reportes = relationship("Rep", back_populates="lugar")

class Emp(db.Model):
    __tablename__ = 'emp'
    IDEEMP: Mapped[int] = mapped_column(Integer, primary_key=True)
    APPEMP: Mapped[str] = mapped_column(String(20))
    APMEMP: Mapped[str] = mapped_column(String(20))
    NOMEMP: Mapped[str] = mapped_column(String(25))
    perfiles = relationship("Per", back_populates="empleado")

class Per(db.Model):
    __tablename__ = 'per'
    IDEPER: Mapped[int] = mapped_column(Integer, primary_key=True)
    EMPPER: Mapped[int] = mapped_column(ForeignKey('emp.IDEEMP'))
    CARPER: Mapped[int] = mapped_column(
        Integer)
    empleado = relationship("Emp", back_populates="perfiles")
    reportes_hechos = relationship("Rep", back_populates="reportante")

class Rep(db.Model):
    __tablename__ = 'rep'
    IDEREP: Mapped[int] = mapped_column(Integer, primary_key=True)
    CONREP: Mapped[bool] = mapped_column(Boolean)
    FECEVE: Mapped[datetime.date] = mapped_column(Date)
    FECREP: Mapped[datetime.datetime] = mapped_column(DateTime)
    FREREP: Mapped[str] = mapped_column(String(25))
    OBSREP: Mapped[str] = mapped_column(String(300), nullable=True)
    CANREP: Mapped[int] = mapped_column(Integer)
    LUGREP: Mapped[int] = mapped_column(ForeignKey('lug.IDELUG'))
    PERREP: Mapped[int] = mapped_column(ForeignKey('per.IDEPER'))

    lugar = relationship("Lug", back_populates="reportes")
    reportante = relationship("Per", back_populates="reportes_hechos")

class Accesos(db.Model):
    __tablename__ = 'accesos'
    IDEACC: Mapped[int] = mapped_column(Integer, primary_key=True)
    DIRACC: Mapped[str] = mapped_column(String(16))
    FECACC: Mapped[datetime.datetime] = mapped_column(DateTime)
    BROACC: Mapped[str] = mapped_column(String(254))
    USEACC: Mapped[int] = mapped_column(Integer, nullable=True)