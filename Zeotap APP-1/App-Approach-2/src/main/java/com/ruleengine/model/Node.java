package com.ruleengine.model;

public class Node {
    private String type; // "operator" or "operand"
    private Node left;
    private Node right;
    private String value; // Value for operands (e.g., comparison values)

    // Getters and Setters

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Node getLeft() {
        return left;
    }

    public void setLeft(Node left) {
        this.left = left;
    }

    public Node getRight() {
        return right;
    }

    public void setRight(Node right) {
        this.right = right;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public Node(String type, Node left, Node right) {
        this.type = type;
        this.left = left;
        this.right = right;
    }

    // Constructor for operand nodes
    public Node(String value) {
        this.type = "operand";
        this.value = value;
    }
}
