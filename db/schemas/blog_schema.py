from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    email = Column(String, nullable=False)

    sections = relationship("Section", back_populates="blog", cascade="all, delete")

class Section(Base):
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # text, image, video
    content = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)

    blog_id = Column(Integer, ForeignKey('blogs.id'))
    blog = relationship("Blog", back_populates="sections")