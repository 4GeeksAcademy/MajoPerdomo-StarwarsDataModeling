import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)

class Faction(Base):
    __tablename__ = 'faction'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    alignment = Column(String(20))  # 'Light', 'Dark', 'Neutral'
    characters = relationship("Character", back_populates="faction")

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    species = Column(String(50))
    home_planet = Column(Integer, ForeignKey('planet.id'))
    faction_id = Column(Integer, ForeignKey('faction.id'))
    description = Column(Text)
    
    faction = relationship("Faction", back_populates="characters")
    planet = relationship("Planet", back_populates="characters")
    appearances = relationship("MediaAppearance", secondary="character_media")

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    sector = Column(String(50))
    climate = Column(String(50))
    terrain = Column(String(50))
    characters = relationship("Character", back_populates="planet")

class MediaAppearance(Base):
    __tablename__ = 'media_appearance'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    type = Column(String(50))  # 'Movie', 'TV Series', 'Book', 'Comic', etc.
    release_year = Column(Integer)
    characters = relationship("Character", secondary="character_media")

class CharacterMedia(Base):
    __tablename__ = 'character_media'
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)
    media_id = Column(Integer, ForeignKey('media_appearance.id'), primary_key=True)

class FavoriteCharacter(Base):
    __tablename__ = 'favorite_character'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    character_id = Column(Integer, ForeignKey('character.id'))
    added_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {}

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    favorite_characters = relationship("FavoriteCharacter")

# Draw from SQLAlchemy base
render_er(Base, 'diagram.png')

