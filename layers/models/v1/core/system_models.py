from sqlalchemy import Index, String, DateTime,ForeignKey,Text
import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from layers.models.v1.core.db_handler import Base

class CompaniesTable(Base):
    __tablename__ = "companies"

    ID: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(320))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))
    users = relationship("UsersTable", back_populates="company")

Index("idx_creation", CompaniesTable.created_at)

class ProjectsMembershipsTable(Base):
    __tablename__ = "projects_memberships"

    ID: Mapped[int] = mapped_column(primary_key=True)
    ID_company: Mapped[int] = mapped_column(ForeignKey("companies.ID", ondelete="CASCADE"))
    ID_user: Mapped[int] = mapped_column(ForeignKey("users.ID", ondelete="CASCADE"))
    ID_project: Mapped[int] = mapped_column(ForeignKey("projects.ID", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))
    projects = relationship("ProjectsTable", back_populates="projects_memberships")

Index(
    "idx_company_user_project_creation", 
    ProjectsMembershipsTable.ID_company, 
    ProjectsMembershipsTable.ID_user, 
    ProjectsMembershipsTable.ID_project, 
    ProjectsMembershipsTable.created_at
)

class ProjectsTable(Base):
    __tablename__ = "projects"

    ID: Mapped[int] = mapped_column(primary_key=True)
    ID_company: Mapped[int] = mapped_column(ForeignKey("companies.ID", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text())
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))
    projects_memberships = relationship("ProjectsMembershipsTable", back_populates="projects")

class UsersTable(Base):
    __tablename__ = "users"

    ID: Mapped[int] = mapped_column(primary_key=True)
    ID_company: Mapped[int] = mapped_column(ForeignKey("companies.ID", ondelete="CASCADE"))
    username: Mapped[str] = mapped_column(String(320))
    email: Mapped[str] = mapped_column(String(320))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False))
    company = relationship("CompaniesTable", back_populates="users")

Index("idx_company_creation", UsersTable.ID_company, UsersTable.created_at)