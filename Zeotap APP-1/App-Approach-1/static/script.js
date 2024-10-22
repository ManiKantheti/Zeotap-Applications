document.getElementById('ruleForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const ruleString = document.getElementById('rule_string').value;

    // Send the rule string to the server to create a new rule
    fetch('/create_rule', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rule_string: ruleString })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Alert the user that the rule was created
        document.getElementById('rule_string').value = ''; // Clear the input field
    })
    .catch(error => {
        console.error('Error:', error); // Log any errors
    });
});

// Event listener for combining rules
document.getElementById('combineButton').addEventListener('click', function() {
    fetch('/combine_rules', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('combinedRule').innerText = data.combined_rule; // Display the combined rule
        document.getElementById('evaluateForm').style.display = 'block'; // Show the evaluation form
    })
    .catch(error => {
        console.error('Error:', error); // Log any errors
    });
});

// Event listener for evaluating the combined rule
document.getElementById('evaluateForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const combinedRule = document.getElementById('combinedRule').innerText;
    const contextInput = document.getElementById('context').value;

    // Convert the context input to a JSON string
    let contextString;
    try {
        const context = JSON.parse(contextInput);
        contextString = JSON.stringify(context);
    } catch (e) {
        alert('Invalid JSON format for context. Please correct it.'); // Alert the user
        return;
    }

    // Send the combined rule and context to the server for evaluation
    fetch('/evaluate_rules', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            combined_rule: combinedRule,
            context: contextString
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error); // Alert the user if there's an error
        } else {
            window.location.href = `/result?result=${data.result}`; // Redirect to result page
        }
    })
    .catch(error => {
        console.error('Error:', error); // Log any errors
    });
});