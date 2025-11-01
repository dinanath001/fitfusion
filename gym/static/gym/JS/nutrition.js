function filterPlans() {
    var filter = document.getElementById("planFilter").value;
    var plans = document.querySelectorAll(".nutrition-card");

    plans.forEach(function(plan) {
        var planType = plan.dataset.type;  // Use dataset for better compatibility
        
        if (filter === "all" || planType === filter) {
            plan.style.display = "block";
        } else {
            plan.style.display = "none";
        }
    });

    console.log("Selected Plan Type:", filter);  // Debugging: Check selected option
}