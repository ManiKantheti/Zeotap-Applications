package com.ruleengine.service;

import com.ruleengine.model.Node;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class RuleService {

    public Node createRule(String ruleString) {
        return parseExpression(ruleString);
    }

    // Helper function to recursively parse an expression and handle parentheses

    // Helper function to parse conditions like "age > 30", "department = 'Sales'"
    private static Node parseCondition(String condition) {
        // Regular expression for matching conditions like "age > 30", "salary = 50000"
        Pattern pattern = Pattern.compile("(\\w+)\\s*(=|>|<|>=|<=)\\s*(\\S+)");
        Matcher matcher = pattern.matcher(condition);

        if (matcher.find()) {
            String leftOperand = matcher.group(1);  // e.g., "age"
            String operator = matcher.group(2);     // e.g., ">", "="
            String rightOperand = matcher.group(3); // e.g., "30", "'Sales'"

            // Create the condition as a single operand node
            String value = leftOperand + " " + operator + " " + rightOperand;
            return new Node(value);  // Create operand node
        }

        // If no match, throw an error (invalid condition)
        throw new IllegalArgumentException("Invalid condition: " + condition);
    }

    public Node combineRules(Node... rules) {
        if (rules == null || rules.length == 0) {
            throw new IllegalArgumentException("No rules provided to combine.");
        }

        // Edge case: Only one rule, return it directly
        if (rules.length == 1) {
            return rules[0];
        }

        // Count occurrences of AND and OR operators in the rules
        int andCount = 0;
        int orCount = 0;
        for (Node rule : rules) {
            andCount += countOperators(rule, "AND");
            orCount += countOperators(rule, "OR");
        }

        // Choose the most frequent operator (AND/OR)
        String operator = andCount >= orCount ? "AND" : "OR";

        // Combine the rules with the chosen operator
        return combineWithOperator(rules, operator);
    }

    // Helper function to count the occurrences of a specific operator in the AST
    private static int countOperators(Node rule, String operator) {
        if (rule == null) return 0;

        int count = 0;

        // If the current node is an operator, check its type
        if (rule.getType().equals("operator") && rule.getValue().equals(operator)) {
            count++;
        }

        // Recursively count operators in left and right children
        count += countOperators(rule.getLeft(), operator);
        count += countOperators(rule.getRight(), operator);

        return count;
    }

    // Helper function to combine multiple rules with the given operator
    private static Node combineWithOperator(Node[] rules, String operator) {
        // Base case: If there's only one rule, return it
        if (rules.length == 1) {
            return rules[0];
        }

        // Start with the first rule as the left node
        Node left = rules[0];

        // Recursively combine the rest of the rules with the chosen operator
        for (int i = 1; i < rules.length; i++) {
            // Create an operator node that connects the left and right part of the combined tree
            Node right = rules[i];
            left = new Node(operator, left, right);
        }

        // Return the root of the combined AST
        return left;
    }

    // Helper function to recursively parse an expression and handle parentheses
    private static Node parseExpression(String expr) {
        expr = expr.trim();
        if (expr.startsWith("(") && expr.endsWith(")")) {
            expr = expr.substring(1, expr.length() - 1);
        }

        Pattern pattern = Pattern.compile("^(.*?)( AND | OR )(.*)$");
        Matcher matcher = pattern.matcher(expr);

        if (matcher.find()) {
            String leftExpr = matcher.group(1).trim();
            String operator = matcher.group(2).trim();
            String rightExpr = matcher.group(3).trim();

            Node leftNode = parseExpression(leftExpr);
            Node rightNode = parseExpression(rightExpr);

            return new Node(operator, leftNode, rightNode);
        }

        return parseCondition(expr);
    }

    public boolean evaluateRule(Node rule, Object userAttributes) {
        if (rule == null) {
            return false; // If the rule is null, return false
        }

        // Check the type of the node (operator or operand)
        if (rule.getType().equals("operator")) {
            // If the node is an operator (AND, OR), evaluate the left and right subtrees
            if (rule.getValue().equals("AND")) {
                return evaluateRule(rule.getLeft(), userAttributes) && evaluateRule(rule.getRight(), userAttributes);
            } else if (rule.getValue().equals("OR")) {
                return evaluateRule(rule.getLeft(), userAttributes) || evaluateRule(rule.getRight(), userAttributes);
            }
        } else if (rule.getType().equals("operand")) {
            // If the node is an operand (a condition), evaluate it
            return evaluateCondition(rule, (Map<String, Object>) userAttributes);
        }

        return false; // Default case (should not be reached)
    }

    // Helper method to evaluate individual conditions (e.g., age > 30)
    private boolean evaluateCondition(Node rule, Map<String, Object> userAttributes) {
        // The 'value' field contains a condition like "age > 30"
        String condition = rule.getValue().trim();

        // Split the condition into parts (e.g., "age", ">", "30")
        String[] parts = condition.split(" ");

        if (parts.length != 3) {
            throw new IllegalArgumentException("Invalid condition format: " + condition);
        }

        String fieldName = parts[0]; // e.g., "age"
        String operator = parts[1];  // e.g., ">", "<", "=", etc.
        String valueStr = parts[2];  // e.g., "30"

        // Retrieve the user attribute for this field
        Object fieldValue = userAttributes.get(fieldName);
        if (fieldValue == null) {
            throw new IllegalArgumentException("Field not found in userAttributes: " + fieldName);
        }

        // Convert the value from the condition (e.g., "30") to the appropriate type
        Object value = parseValue(valueStr, fieldValue.getClass());

        // Evaluate the condition based on the operator
        switch (operator) {
            case "=":
                return fieldValue.equals(value);
            case ">":
                return compareValues(fieldValue, value) > 0;
            case "<":
                return compareValues(fieldValue, value) < 0;
            case ">=":
                return compareValues(fieldValue, value) >= 0;
            case "<=":
                return compareValues(fieldValue, value) <= 0;
            default:
                throw new IllegalArgumentException("Unsupported operator: " + operator);
        }
    }

    // Helper method to parse the value from the condition (e.g., "30" -> Integer or Double)
    private Object parseValue(String valueStr, Class<?> fieldType) {
        if (fieldType == Integer.class || fieldType == int.class) {
            return Integer.parseInt(valueStr);
        } else if (fieldType == Double.class || fieldType == double.class) {
            return Double.parseDouble(valueStr);
        } else if (fieldType == String.class) {
            return valueStr.replace("'", ""); // Remove quotes for string values
        } else {
            throw new IllegalArgumentException("Unsupported field type: " + fieldType);
        }
    }

    // Helper method to compare two values (for >, <, >=, <= operators)
    private int compareValues(Object value1, Object value2) {
        if (value1 instanceof Comparable && value2 instanceof Comparable) {
            return ((Comparable) value1).compareTo(value2);
        }
        throw new IllegalArgumentException("Cannot compare values: " + value1 + " and " + value2);
    }
}
