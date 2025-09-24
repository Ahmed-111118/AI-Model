import React, { useState } from "react";
import PlanForm from "./components/PlanForm";
import PlanResult from "./components/PlanResult";
import PlanDisplay from "./components/PlanDisplay";
import "./App.css";

function App() {
  const [plan, setPlan] = useState(null);

  return (
    <div className="container">
      <h1>AI Gym Plan Generator 💪</h1>
      <PlanForm setPlan={setPlan} />
      <PlanDisplay plan={plan} />
      {plan && <PlanResult plan={plan} />}
    </div>
  );
}

export default App;
