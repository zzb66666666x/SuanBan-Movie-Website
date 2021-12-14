USE todo_list;

CREATE TABLE tasks(
    id INT PRIMARY KEY,
    task VARCHAR(255),
    status VARCHAR(255)
);

INSERT INTO tasks VALUES(22, "finish cs411 hw", "Todo");

SELECT * from tasks;
