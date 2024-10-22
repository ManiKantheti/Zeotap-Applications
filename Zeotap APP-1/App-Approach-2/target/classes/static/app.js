let rules = [];
let combinedRule = null;

document.addEventListener("DOMContentLoaded", function() {
    // Handle form submission for creating rules
    document.getElementById('createRuleForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const ruleString = document.getElementById('ruleString').value;

        if (ruleString) {
            const ruleNode = createRule(ruleString); // Parse rule string into Node
            rules.push(ruleNode);
            updateRuleList();
            document.getElementById('ruleString').value = ""; // Clear the input field
        }
    });

    // Handle form submission for combining all rules
    document.getElementById('combineRulesForm').addEventListener('submit', function (event) {
        event.preventDefault();
        if (rules.length > 1) {
            combinedRule = combineRules(rules);
            displayCombinedRule(combinedRule);
        } else {
            alert("Please create at least two rules to combine.");
        }
    });

    // Handle form submission for evaluating combined rule
    document.getElementById('evaluateRuleForm').addEventListener('submit', function (event) {
        event.preventDefault();

        const userAttributes = JSON.parse(document.getElementById('userAttributes').value);

        if (combinedRule) {
            const result = evaluateRule(combinedRule, userAttributes);
            displayEvaluationResult(result);
        } else {
            alert("No combined rule available for evaluation.");
        }
    });
});

// Function to create a rule (parse the rule string into a simple rule object)
function createRule(ruleString) {
    return {
        id: rules.length,
        ruleString: ruleString,
        type: "rule", // A placeholder for rule type
    };
}

// Update the rule list to display created rules
function updateRuleList() {
    const ruleListContainer = document.getElementById('ruleList');

    ruleListContainer.innerHTML = ''; // Clear current list

    rules.forEach((rule, index) => {
        // Display individual rules
        const ruleDiv = document.createElement('div');
        ruleDiv.textContent = `Rule ${index + 1}: ${rule.ruleString}`;
        ruleListContainer.appendChild(ruleDiv);
    });
}

// Function to combine multiple rules into one (for example, using AND operators)
function combineRules(ruleNodes) {
    if (ruleNodes.length === 1) return ruleNodes[0]; // No combining needed for just one rule

    // For simplicity, we are combining rules with an "AND" operator
    return {
        type: "operator",
        value: "AND", // This could be dynamically set depending on user choice
        left: ruleNodes[0],
        right: combineRules(ruleNodes.slice(1)), // Recursively combine the rest
    };
}

// Function to display the combined rule
function displayCombinedRule(rule) {
    const combinedRuleContainer = document.getElementById('combinedRule');
    combinedRuleContainer.textContent = `Combined Rule: ${JSON.stringify(rule)}`;
}

// Function to evaluate the combined rule against user attributes (simplified version)
function evaluateRule(rule, userAttributes) {
    if (rule.type === "rule") {
        return evaluateCondition(rule.ruleString, userAttributes);
    } else if (rule.type === "operator") {
        const leftResult = evaluateRule(rule.left, userAttributes);
        const rightResult = evaluateRule(rule.right, userAttributes);

        if (rule.value === "AND") {
            return leftResult && rightResult;
        } else if (rule.value === "OR") {
            return leftResult || rightResult;
        }
    }
    return false;
}

// Evaluate individual conditions (for example, "age > 30 AND department = 'Sales'")
function evaluateCondition(condition, userAttributes) {
    const conditionParts = parseCondition(condition);

    if (conditionParts.operator === ">") {
        return userAttributes[conditionParts.attribute] > conditionParts.value;
    } else if (conditionParts.operator === "<") {
        return userAttributes[conditionParts.attribute] < conditionParts.value;
    } else if (conditionParts.operator === "=") {
        return userAttributes[conditionParts.attribute] === conditionParts.value;
    }
    return false;
}

// Helper function to parse conditions like "age > 30"
function parseCondition(condition) {
    const regex = /(\w+)\s*(=|>|<)\s*(\d+|'[^']*')/;
    const match = condition.match(regex);

    if (!match) throw new Error("Invalid condition format.");

    return {
        attribute: match[1],
        operator: match[2],
        value: isNaN(match[3]) ? match[3].replace(/'/g, "") : parseInt(match[3], 10),
    };
}

// Display the evaluation result (pass/fail)
function displayEvaluationResult(result) {
    const evaluationResultContainer = document.getElementById('evaluationResult');
    evaluationResultContainer.textContent = result ? "Rule passed." : "Rule failed.";
}