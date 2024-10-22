CREATE TABLE rules (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       rule_string VARCHAR(255) NOT NULL
);

CREATE TABLE rule_metadata (
                               rule_id INT,
                               attribute_name VARCHAR(255),
                               attribute_value VARCHAR(255),
                               FOREIGN KEY (rule_id) REFERENCES rules(id)
);
