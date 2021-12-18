CREATE TABLE Users (
    user_id SERIAL,
    username TEXT UNIQUE,
    password TEXT,
    isadmin BOOLEAN,
    PRIMARY KEY (user_id)
);

CREATE TABLE Categories (
    category_id SERIAL,
    category_name TEXT,
    category_description TEXT,
    PRIMARY KEY (category_id)
);

CREATE TABLE Events (
    event_id SERIAL,
    event_name TEXT,
    creator_id INTEGER,
    isprivate BOOLEAN,
    event_description TEXT,
    place TEXT,
    event_date DATE,
    start_time TIME,
    end_time TIME,
    category_id INTEGER,
    PRIMARY KEY (event_id),
    FOREIGN KEY (creator_id) REFERENCES Users(user_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Invitees (
    event_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Attendance (
    event_id INTEGER,
    user_id INTEGER,
    attending BOOLEAN,
    PRIMARY KEY (event_id, user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Groups (
    group_id SERIAL,
    group_name TEXT,
    group_description TEXT,
    PRIMARY KEY (group_id)
);

CREATE TABLE Members (
    group_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES Groups(group_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Comments (
    comment_id SERIAL,
    comment TEXT,
    event_id INTEGER,
    author_id INTEGER,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (author_id) REFERENCES Users(user_id),
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE
);