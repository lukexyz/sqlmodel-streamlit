from typing import Optional
import pandas as pd
import streamlit as st
import os
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Hero(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}  # required for streamlit refreshing
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


sqlite_file_name = 'database.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    hero_1 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=36)
    hero_2 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=26)
    hero_3 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=33)
    with Session(engine) as session:
        session.add(hero_1)
        session.add(hero_2)
        session.add(hero_3)
        session.commit()


def get_db_size():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
    return len(heroes)


def select_heros():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.age <= 35)
        results = session.exec(statement)
        for hero in results:
            st.text(hero)
        #st.text(len(results))


def show_table():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        st.table(pd.DataFrame([s.dict() for s in heroes[-5:]]))


def delete_db():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        for hero in heroes:
            session.delete(hero)  
        session.commit()  
    st.text("Deleted all rows")  


def write_new_row():

    with st.form('new_row'):
        name_input = st.text_input('Name', value="Don Johnson")
        secret_name = st.text_input('Secret alias', value="Dr. Jon")

        submitted = st.form_submit_button("Submit")
        if submitted:
            hero = Hero(name=name_input, secret_name=secret_name, age=23)
            st.write('submitted')
            with Session(engine) as session:
                session.add(hero)
                session.commit()
    st.write("Outside the form")


# ====================================== main ====================================== #

def main():
        
    st.title('🦄 SQLModel Demo')



    b1, b2, b3, b4= st.columns(4)
    #if b1.button('Add Filter'):
    #    pass
        #select_heros()  # todo
    if b4.button("♻️ Empty db"):
        delete_db()
    #if b2.button('Create db'): 
    #    create_db_and_tables()
    if b3.button('+ Add 3 rows'): 
        create_heroes()

    if st.button("➡️ Insert Row"):
        write_new_row()

    show_table()
    col0, col1, col2 = st.columns(3)
    file_size = os.path.getsize('database.db')
    col1.metric("💾 database.db", f"{get_db_size()}", "total rows")
    col2.metric("filesize", f"{file_size/1000:0.1f}", 'kb')






if __name__ == '__main__':
    st.set_page_config(
        page_title="SQLModel Demo",
        page_icon="🦄",
        layout="centered",
        initial_sidebar_state="auto")
    main()
