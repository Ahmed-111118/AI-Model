import React, { useState } from "react";
import PlanForm from "./components/PlanForm";
import PlanDisplay from "./components/PlanDisplay";
import "./App.css";

function App() {
  const [plan, setPlan] = useState(null);

  return (
    <div className="container">
      <h1>AI Gym Plan Generator 💪</h1>

      {/* Form to collect user data */}
      <PlanForm setPlan={setPlan} />

      {/* Display generated plan */}
      {plan && <PlanDisplay plan={plan} />}
    </div>
  );
}

export default App;
