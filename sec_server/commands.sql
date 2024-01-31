-- Create a table for groups
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    created_by_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_by_id INTEGER REFERENCES users(id),
    updated_at TIMESTAMP,
    deleted_by_id INTEGER REFERENCES users(id),
    deleted_at TIMESTAMP,
    name VARCHAR(255) NOT NULL,
    is_public BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_email_validated BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create a table for permissions
CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id),
    role_name VARCHAR(255) NOT NULL,
    role_description TEXT NOT NULL,
    is_default BOOLEAN NOT NULL,
    post_as_group BOOLEAN NOT NULL DEFAULT FALSE,
    manage_members BOOLEAN NOT NULL DEFAULT FALSE,
    manage_content BOOLEAN NOT NULL DEFAULT FALSE,
    manage_metadata BOOLEAN NOT NULL DEFAULT FALSE,
    can_post BOOLEAN NOT NULL DEFAULT TRUE,
    manage_roles BOOLEAN NOT NULL DEFAULT FALSE,
    reply_to_authors BOOLEAN NOT NULL DEFAULT TRUE,
    attach_files BOOLEAN NOT NULL DEFAULT TRUE,
    view_member_email_addresses BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create a table for users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    profile_picture VARCHAR(255) NOT NULL
);

-- TODO: This table is unique for each group. So, we need to create a table for each group.
-- Create a table for group members
CREATE TABLE group_members (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    group_id INTEGER NOT NULL REFERENCES groups(id),
    permission_id INTEGER NOT NULL REFERENCES permissions(id),
    is_banned BOOLEAN NOT NULL DEFAULT FALSE,
    is_pending BOOLEAN NOT NULL DEFAULT FALSE,
    is_invited BOOLEAN NOT NULL DEFAULT FALSE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT unique_group_member UNIQUE (user_id, group_id)
);

-- Create a table for messages
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES groups(id),
    message_id VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    sender_id INTEGER NOT NULL REFERENCES users(id),
    thread_id INTEGER REFERENCES messages(id),
    parent_id INTEGER REFERENCES messages(id),
    children INTEGER[] NOT NULL DEFAULT '{}',
    receiver_id INTEGER NOT NULL REFERENCES users(id),
    level INTEGER NOT NULL DEFAULT 0,
    is_thread_starter BOOLEAN NOT NULL DEFAULT FALSE
);

-- Create a table for message attachments
CREATE TABLE message_attachments (
    id SERIAL PRIMARY KEY,
    message_id INTEGER NOT NULL REFERENCES messages(id),
    attachment_name VARCHAR(255) NOT NULL,
    attachment_type VARCHAR(255) NOT NULL,
    attachment_url TEXT NOT NULL
);

-- Add indexes to frequently used columns
CREATE INDEX group_id_index ON permissions (group_id);
CREATE INDEX group_id_member_index ON group_members (group_id);
CREATE INDEX user_id_index ON group_members (user_id);
CREATE INDEX sender_id_index ON messages (sender_id);
CREATE INDEX receiver_id_index ON messages (receiver_id);
CREATE INDEX message_id_index ON message_attachments (message_id);