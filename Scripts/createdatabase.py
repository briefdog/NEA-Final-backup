#sqlite3 was learned from https://www.youtube.com/watch?v=pd-0G0MigUA&t=706s
#to access database, I used this SQLite3 Editor extension: https://marketplace.visualstudio.com/items?itemName=yy0931.vscode-sqlite3-editor
#import sql library
import sqlite3
#creates database
conn = sqlite3.connect("information.db")
cur = conn.cursor()

#create table with login details if it does not exist                  
cur.execute("""
CREATE TABLE IF NOT EXISTS users (                                   
    id INTEGER PRIMARY KEY ,         -- references to all plans and created by user and all the user's information
    username VARCHAR(255) NOT NULL UNIQUE,      -- UNIQUE constraint to prevent duplicate accounts from being created
    password VARCHAR(255) NOT NULL       
)            
""")

#create table to store user's personal information
cur.execute("""
CREATE TABLE IF NOT EXISTS user_personal_info (
    main_id INTEGER PRIMARY KEY,   -- Primary key used so user can discard the information if needed, and used to identify most recent entry into the table
    id INTEGER,       -- Foreign key referencing to plan_identification
    user_fk INTEGER,  -- Foreign key referencing the id column in the users table
    current_weight FLOAT,
    weight_goal FLOAT,
    physical_activity VARCHAR(255),
    allergies BOOLEAN,
    gym_access BOOLEAN,
    FOREIGN KEY(user_fk) REFERENCES users(id) ON DELETE CASCADE,   -- if user deletes account, all of the user's data will also get deleted 
    FOREIGN KEY(id) REFERENCES plan_identification(id) ON DELETE CASCADE   -- if user deletes the fitness plan, all of the information associated with it will get deleted too
)
""")

#create table to store information about what equipment the user has access to
cur.execute("""
CREATE TABLE IF NOT EXISTS equipment_access (
    main_id INTEGER PRIMARY KEY,  -- Primary key used so user can discard the information if needed, and used to identify most recent entry into the table
    id INTEGER,         -- Foreign key referencing to plan_identification
    user_fk INTEGER,    -- Foreign key referencing the id column in the users table
    dumbells BOOLEAN,
    pull_up_bar BOOLEAN,
    barbell BOOLEAN,
    bench BOOLEAN,
    leg_extensions_machine BOOLEAN,
    leg_curl_machine BOOLEAN,
    ez_bar BOOLEAN,
    cables BOOLEAN,
    dip_station BOOLEAN,
    leg_press_machine BOOLEAN,
    pec_fly_machine BOOLEAN,
    skipping_rope BOOLEAN,
    tricep_press_machine BOOLEAN,
    treadmill BOOLEAN,
    stair_climber_machine BOOLEAN,
    exercise_bike BOOLEAN,
    shoulder_press_machine BOOLEAN,
    chest_press_machine BOOLEAN,
    rowing_machine BOOLEAN,
    preacher_curl_bench BOOLEAN,
    lateral_pulldown_machine BOOLEAN,
    FOREIGN KEY(user_fk) REFERENCES users(id) ON DELETE CASCADE,       -- if user deletes account, all of the user's data will also get deleted
    FOREIGN KEY(id) REFERENCES plan_identification(id) ON DELETE CASCADE      -- if user deletes the fitness plan, all of the information associated with it will get deleted too
)
""")

#create table to identify each plan created
cur.execute("""
CREATE TABLE IF NOT EXISTS plan_identification (
    id INTEGER PRIMARY KEY,              -- used to identify most recent entry into the table and to uniquely identify each plan
    user_fk INTEGER,                      -- No unique constraint to allow user to make multiple plans,
    plan_name VARCHAR(255) UNIQUE,        -- cannot have duplicate plan names for the same account 
    start_date DATE,                  
    FOREIGN KEY(user_fk) REFERENCES users(id) ON DELETE CASCADE      -- if user deletes account, all of the user's data will also get deleted
)
""")

#create table to store details/actual content of workout plan
cur.execute("""
CREATE TABLE IF NOT EXISTS workout_plan_details (
    main_id INTEGER PRIMARY KEY,  -- Primary key used so user can discard the information if needed
    id INTEGER,               -- Foreign key referencing to plan_identification      
    user_fk INTEGER,          -- Foreign key referencing the id column in the users table
    push_ex_1 VARCHAR(255),
    push_ex_2 VARCHAR(255),
    push_ex_3 VARCHAR(255),
    push_ex_4 VARCHAR(255),
    push_ex_5 VARCHAR(255),
    push_ex_6 VARCHAR(255),
    pull_ex_1 VARCHAR(255),
    pull_ex_2 VARCHAR(255),
    pull_ex_3 VARCHAR(255),
    pull_ex_4 VARCHAR(255),
    pull_ex_5 VARCHAR(255),
    pull_ex_6 VARCHAR(255),
    legs_ex_1 VARCHAR(255),
    legs_ex_2 VARCHAR(255),
    legs_ex_3 VARCHAR(255),
    legs_ex_4 VARCHAR(255),
    legs_ex_5 VARCHAR(255),
    legs_ex_6 VARCHAR(255),
    FOREIGN KEY(user_fk) REFERENCES users(id) ON DELETE CASCADE,            -- if user deletes account, all of the user's data will also get deleted
    FOREIGN KEY(id) REFERENCES plan_identification(id) ON DELETE CASCADE      -- if user deletes the fitness plan, all of the information associated with it will get deleted too
)
""")

#create table to store information about nutrition plan
cur.execute("""
CREATE TABLE IF NOT EXISTS nutrition_plan_details (
    main_id INTEGER PRIMARY KEY,  -- Primary key used so user can discard the information if needed, and used to identify most recent entry into the table
    id INTEGER,               -- Foreign key referencing to plan_identification      
    user_fk INTEGER,          -- Foreign key referencing the id column in the users table
    breakfast_1 VARCHAR(255),
    lunch_1 VARCHAR(255),
    dinner_1 VARCHAR(255),
    breakfast_2 VARCHAR(255),
    lunch_2 VARCHAR(255),
    dinner_2 VARCHAR(255),
    breakfast_3 VARCHAR(255),
    lunch_3 VARCHAR(255),
    dinner_3 VARCHAR(255),
    FOREIGN KEY(user_fk) REFERENCES users(id) ON DELETE CASCADE,            -- if user deletes account, all of the user's data will also get deleted
    FOREIGN KEY(id) REFERENCES plan_identification(id) ON DELETE CASCADE       -- if user deletes the fitness plan, all of the information associated with it will get deleted too
)
""")

#execute queries
conn.commit()

