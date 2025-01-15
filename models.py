from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum, Numeric
from datetime import datetime, timedelta
from faker import Faker
from decimal import Decimal

import enum
import random

TOTAL_NR_OF_USERS = 1000

db = SQLAlchemy()

class UserType(enum.Enum):
    NEWBIE = 1
    REGULAR = 2
    MASTER = 3
    SUPER = 4

class User(db.Model):
    __tablename__ = "Customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    registrated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(70), nullable=False)
    birth_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    user_type: Mapped[UserType] = mapped_column(
        Enum(UserType, native_enum=True, create_constraint=True),
        nullable=False
    )


    def __str__(self):
        return (f"Name: {self.name}\n"
                f"Username: {self.username}\n"
                f"Registration Date: {self.registrated_at}\n"
                f"Address: {self.address}\n"
                f"City: {self.city}\n"
                f"Birth Date: {self.birth_date}\n"
                f"Email: {self.email}")



def seed_users(db:SQLAlchemy):
    list_of_user_type = list(UserType)
    fake = Faker("sv_SE")
    Faker.seed(42)

    current_nr_of_users_in_db = len(User.query.all())

    while current_nr_of_users_in_db < TOTAL_NR_OF_USERS:

        new_user = User()
        new_user.name = fake.name()
        new_user.username = fake.user_name()
        new_user.registrated_at = fake.date_between(start_date='-365d', end_date='today')
        new_user.address = fake.street_address().replace("\n", ", ")
        new_user.city = fake.city()
        new_user.birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime("%Y-%m-%d")
        new_user.email = fake.email()
        new_user.user_type = random.choice(list_of_user_type)

        db.session.add(new_user)
        db.session.commit()
        current_nr_of_users_in_db += 1

    

